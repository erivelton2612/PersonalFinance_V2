# app.py
import streamlit as st
import pandas as pd
from backend.function import *
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import plotly.express as px
import numpy as np


# LandPage.py
st.set_page_config(page_title="Página Inicial", layout="wide")

st.title("Sistema de Classificação")
st.write("Bem-vindo ao sistema de classificação. Selecione uma opção no menu lateral.")
# st.sidebar.markdown("### Opções")
# st.sidebar.markdown("- [Importar Extrato](pages/ImportarExtrato.py)")
# st.sidebar.markdown("- [Classificações](pages/Classificacao.py)")

try:
    if "token" not in st.session_state or not st.session_state.token:
        st.warning("Você precisa estar logado para acessar esta página.")
        st.stop()
except:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

st.sidebar.success(f"Autenticado como {st.session_state.username}")

try:
    df = pd.DataFrame()
    df = carregar_dados(st.session_state.token)
    if df is None or df.empty:
        st.error("Erro ao carregar dados. Tente novamente.")
        # Opcional: tentar novamente automaticamente
        # df = carregar_dados(st.session_state.token)
    else:
        st.success("Dados carregados com sucesso!")
        df["DataDebito"] = pd.to_datetime(df["DataDebito"], format="%Y-%m-%d")
        df["DataLancamento"] = pd.to_datetime(df["DataLancamento"], format="%Y-%m-%d")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    try:
        df = carregar_dados(st.session_state.token)
    except Exception as e2:
        st.error(f"Erro ao tentar novamente: {e2}")
        st.stop()

df["Detalhes"] = "Ver detalhes"
lendf = len(df)
revisaomanual = len(df[(df['Accurace'] > 11) & (df['Classe'].isna())])
semclasse = len(df[df['Classe'].isna()])


a, b ,c = st.columns(3)

a.metric(label="Registros", value=f"{lendf}", border=True)
b.metric(label="Sem Classe", value=f"{semclasse}",  border=True)
c.metric(label="Revisâo Manual", value=f"{revisaomanual}", border=True)

tab1, tab2, tab3 = st.tabs(["Resumo", "Tabela", "Gráficos"])


with tab1:
    #########
    
    st.table(df)
    # # Simulando dados
    # df = pd.DataFrame({
    #     "DataLancamento": pd.date_range(start="2025-01-01", periods=90, freq="D"),
    #     "Classe": ['Alimentacao', 'Transporte', 'Lazer', 'Mercado', 'Delivery'] * 18,
    #     "ValorPrincipal": np.random.randint(10, 200, size=90)
    # })

    # Adiciona coluna de Mês no formato YYYY-MM

    df["Mes"] = df["DataLancamento"].dt.to_period("M").astype(str)
    
    # Pivot: Classe nas linhas, Mes nas colunas
    df_pivot = pd.pivot_table(
        df,
        index="Classe",
        columns="Mes",
        values="ValorPrincipal", 
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Obtem lista de meses ordenada
    meses_disponiveis = df["Mes"].sort_values().unique().tolist()

    # Filtro de meses
    meses_selecionados = st.multiselect("Filtrar meses:", meses_disponiveis, default=meses_disponiveis)


   
    # Só calcula totais e variação se houver pelo menos dois meses selecionados

    df_pivot['Total'] = df_pivot[meses_selecionados].sum(axis=1)
    # df_pivot['Variacao'] = df_pivot[meses_disponiveis[-1]] - df_pivot[meses_disponiveis[-2]]
    # df_pivot['Icone'] = df_pivot['Variacao'].apply(lambda x: '🍀' if x > 0 else ('🔻' if x < 0 else '➡️'))
    
    
    colunas_final = ["Classe"] + meses_disponiveis + ["Total", "Variacao", "Icone"]
    df_mostrar = df_pivot[colunas_final]
    # Mostrar total geral
    with st.container(border = True):
        total_geral = df_mostrar[meses_selecionados].sum().sum()
        st.metric("Total Geral dos Gastos Filtrados", f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # AgGrid
    formatter_real = "(params.value != null) ? 'R$ ' + params.value.toFixed(2) : ''"

    # # Modal com detalhes
    value_formatter = JsCode("""
    function(params) {
        if (params.value != null) {
            return 'R$ ' + params.value.toFixed(2);
        } else {
            return '';
        }
    }
    """)

    gb = GridOptionsBuilder.from_dataframe(df_mostrar)
    gb.configure_default_column(editable=False, resizable=True)
    for mes in meses_selecionados:
        gb.configure_column(mes, type=["numericColumn"], 
                            valueFormatter=formatter_real, 
                            cellRenderer=value_formatter,
                            cellStyle={'textAlign': 'right'})
    gb.configure_column("Total", type=["numericColumn"], valueFormatter=value_formatter, cellStyle={'textAlign': 'right','fontWeight': 'bold'})
    gb.configure_column("Variacao", valueFormatter=formatter_real, hide = True, cellStyle={'textAlign': 'right'})
    gb.configure_column("Icone", headerName="Tendência", cellStyle={'textAlign': 'center'})
    gb.configure_column("Classe", cellStyle={'textAlign': 'left','fontWeight': 'bold'})
    


    AgGrid(
        df_mostrar,
        gridOptions=gb.build(),
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        theme="material",
        fit_columns_on_grid_load=True,
    )

    # Obs: para implementar modal real, seria necessário integrar com frontend customizado. Aqui, usamos o efeito de hover + estilo clicável para simular.

with tab2:
        # app.py
    import streamlit as st
    import pandas as pd
    from backend.function import *
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
    import plotly.express as px
    import numpy as np

    import pandas as pd
    import streamlit as st
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

    # Simulando dados
    df = pd.DataFrame({
        'DataLancamento': pd.date_range(start='2024-01-01', periods=12, freq='W'),
        'Classe': ['Alimentação', 'Transporte', 'Lazer'] * 4,
        'Lancamento': ['Padaria', 'Uber', 'Cinema', 'Restaurante', 'Ônibus', 'Bar', 'Mercado', 'Gasolina', 'Parque', 'Delivery', 'Táxi', 'Teatro'],
        'MeioPagamento': ['Cartão'] * 12,
        'ValorPrincipal': [30, 15, 45, 60, 10, 35, 120, 50, 20, 80, 25, 90]
    })

    # Garantir tipo numérico
    df["ValorPrincipal"] = pd.to_numeric(df["ValorPrincipal"], errors="coerce")
    df["AnoMes"] = df["DataLancamento"].dt.to_period('M').astype(str)

    # Colunas de exibição
    colunas = ["Classe", "AnoMes", "Lancamento", "MeioPagamento", "ValorPrincipal"]

    # Builder
    gb = GridOptionsBuilder.from_dataframe(df[colunas])
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True)

    # Agrupamento
    gb.configure_column("Classe", rowGroup=True, hide=True)
    gb.configure_column("AnoMes", rowGroup=True, hide=True)

    # Coluna de valor
    gb.configure_column(
        "ValorPrincipal",
        type=["numericColumn"],
        aggFunc="sum",
        valueFormatter="(params.value !== undefined) ? 'R$ ' + params.value.toFixed(2) : ''",
        cellStyle={"textAlign": "right"}
    )

    # Detalhe ao clicar na linha agrupada
    gb.configure_grid_options(
        groupIncludeFooter=True,
        groupIncludeTotalFooter=True,
        masterDetail=True,
        detailCellRendererParams={
            "detailGridOptions": {
                "columnDefs": [
                    {"field": "DataLancamento"},
                    {"field": "Lancamento"},
                    {"field": "MeioPagamento"},
                    {"field": "ValorPrincipal"}
                ]
            },
            "getDetailRowData": JsCode("""
                function(params) {
                    params.successCallback([params.data]);
                }
            """)
        },
        autoGroupColumnDef={
            "headerName": "Grupo",
            "field": "Classe",
            "cellRendererParams": {
                "suppressCount": True
            }
        }
    )

    gridOptions = gb.build()

    # Mostrar grid
    AgGrid(
        df[colunas],
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        theme="material",
        height=600,
        fit_columns_on_grid_load=True
    )


with tab3:
    st.write("Dynamic")
    # ...outros componentes...
        
    edited_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "DataDebito": st.column_config.DateColumn("Débito",width="small"),
            "DataLancamento": st.column_config.DateColumn("Lançamento",width="small"),
            "MeioPagamento": st.column_config.TextColumn("Meio",width="small"),
            "Lancamento": st.column_config.TextColumn("Lançamento"),
            "Ref1": st.column_config.TextColumn("Ref1",width="small"),
            "Ref2": st.column_config.TextColumn("Ref2",width="small"),
            "ref3": st.column_config.TextColumn("ref3",width="small"),
            "PagoRecebido": st.column_config.TextColumn("P/R",width="small"),
            "ValorPrincipal": st.column_config.Column("Valor Principal"),
            "ClasseSugerida": st.column_config.TextColumn("Classe Sugerida"),
            "Classe": st.column_config.TextColumn("Classe"),
            "Origem": st.column_config.TextColumn("Origem",width="small"),
            "Detalhes": st.column_config.LinkColumn(
            "Det", 
            help="Clique para ver detalhes", 
            display_text="👻",width="small"),
            #url="https://www.myapp.com/detalhes/"  # ou use um valor dinâmico se quiser
        },
        column_order=["DataDebito", "DataLancamento", "MeioPagamento",
                        "Lancamento", "PagoRecebido",
                        "ValorPrincipal", "ClasseSugerida", "Classe", "Origem","Detalhes", 
                        "Ref1", "Ref2", "ref3","Accurace"],
        disabled=["Id", "user_id","DataDebito"],
        hide_index=True,
    )





pagina = st.sidebar.selectbox("Menu", [ "Main","Sair"])

if pagina == "Sair":
    st.session_state.token = None
    st.session_state.username = ""
    st.rerun()
