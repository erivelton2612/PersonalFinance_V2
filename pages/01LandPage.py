# app.py
import streamlit as st
import pandas as pd
from backend.function import *
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import plotly.express as px


# LandPage.py
st.set_page_config(page_title="Página Inicial", layout="wide")

st.title("Sistema de Classificação")
st.write("Bem-vindo ao sistema de classificação. Selecione uma opção no menu lateral.")
# st.sidebar.markdown("### Opções")
# st.sidebar.markdown("- [Importar Extrato](pages/ImportarExtrato.py)")
# st.sidebar.markdown("- [Classificações](pages/Classificacao.py)")


df = pd.DataFrame()
df = carregar_dados(st.session_state.token)
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
    st.write("Dynamic")
    # ...outros componentes...
        
    edited_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "DataDebito": st.column_config.TextColumn("Débito",width="small"),
            "DataLancamento": st.column_config.TextColumn("Lançamento",width="small"),
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

with tab2:
    # st.dataframe(df)
    # ...outros componentes...
    
    # Filtrar colunas visíveis no grid
    colunas_visiveis = ['Classe', 'Lancamento', 'MeioPagamento', 'ValorPrincipal']

    gb = GridOptionsBuilder.from_dataframe(df[colunas_visiveis])
    gb.configure_side_bar() 
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gb.configure_column("Classe",rowGroup=True,pinned="left")  # ou "right"
    gb.configure_column("ValorPrincipal", type=["numericColumn", "numberColumnFilter", "agNumberColumnFilter"], 
                    aggFunc="sum", 
                    valueFormatter="(params.value != null) ? 'R$ ' + params.value.toFixed(2) : ''",
                    cellStyle={'textAlign': 'right'})
        # Outras opções úteis
    gb.configure_grid_options(domLayout='normal', suppressRowClickSelection=True,
                            groupDefaultExpanded=-1,  # <- expande todos os grupos
                            groupIncludeFooter=True,     # Subtotal por grupo
                            groupIncludeTotalFooter=True,  # Total geral no final
                            suppressAggFuncInHeader=True,
                            autoGroupColumnDef={
                                "headerName": "Classe",
                                "field": "Classe",
                                "cellRendererParams": {
                                    "suppressCount": True
                                }
                            })
    # gb.configure_selection("multiple", use_checkbox=True, groupSelectsChildren="Group checkbox select children")
    
    # gb.configure_grid_options(# ver mais detalher
    #     masterDetail=True,
    #     detailCellRendererParams={
    #         "detailGridOptions": {
    #             "columnDefs": [
    #                 {"field": "Detalhes"}
    #             ]
    #         },
    #         "getDetailRowData": JsCode("""
    #             function(params) {
    #                 params.successCallback([
    #                     {Detalhes: params.data.Detalhes}
    #                 ]);
    #             }
    #         """)
    #     }
    # )
    
    gridOptions = gb.build()

    AgGrid(
        df[colunas_visiveis],
        gridOptions=gridOptions,
        enable_enterprise_modules=True,  # permite pivot, agrupamento, etc.
        allow_unsafe_jscode=True,
        # theme="streamlit"
        theme="material",
        height=600,
        groupable=True,
        enable_pivot=True,
        enable_pivot_mode=True,
        filter=True,
        fit_columns_on_grid_load=True
    )

with tab3:
    # Simulando DataFrame original
    df = pd.DataFrame({
        "DataLancamento": pd.date_range(start="2025-01-01", periods=20),
        "MeioPagamento": ["Cartão"] * 10 + ["PIX"] * 10,
        "Lancamento": ['Padaria', 'Uber', 'Cinema', 'Restaurante', 'Ônibus', 'Bar', 'Mercado', 'Gasolina', 'Parque', 'Delivery',
                    'Táxi', 'Teatro', 'Lanche', 'Farmácia', 'Posto', 'Sorvete', 'Streaming', 'Roupas', 'Bebidas', 'Doces'],
        "Classe": ['Alimentação', 'Transporte', 'Lazer', 'Alimentação', 'Transporte', 'Lazer', 'Mercado', 'Transporte', 'Lazer', 'Delivery',
                'Transporte', 'Cultura', 'Alimentação', 'Saúde', 'Transporte', 'Alimentação', 'Entretenimento', 'Roupas', 'Bebidas', 'Doces'],
        "ValorPrincipal": [30, 15, 45, 60, 10, 35, 120, 50, 20, 80, 25, 90, 18, 33, 70, 12, 22, 40, 28, 8],
    })

    # Agrupar por lançamento e calcular acumulado percentual
    gastos = df.groupby("Lancamento", as_index=False)["ValorPrincipal"].sum()
    gastos = gastos.sort_values("ValorPrincipal", ascending=False)
    gastos["Acumulado"] = gastos["ValorPrincipal"].cumsum()
    total = gastos["ValorPrincipal"].sum()
    gastos["PercentualAcumulado"] = gastos["Acumulado"] / total

    # Classificar em grupo
    gastos["Grupo"] = gastos["PercentualAcumulado"].apply(lambda x: "TOP 80%" if x <= 0.8 else "Outros")

    # Juntar com df original
    df = df.merge(gastos[["Lancamento", "Grupo"]], on="Lancamento", how="left")

    # Contagem por grupo + lançamento
    contagem = df.groupby(["Grupo", "Lancamento"]).size().reset_index(name="Quantidade")

    # Gráfico
    fig = px.bar(
        contagem,
        x="Quantidade",
        y="Lancamento",
        color="Grupo",
        orientation="h",
        color_discrete_map={"TOP 80%": "royalblue", "Outros": "orangered"},
        title="Gastos que compõem 80% do total (frequência de lançamentos)"
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Filtro por grupo
    grupo_selecionado = st.radio("Selecione o grupo de gastos para detalhar:", ["TOP 80%", "Outros"])

    df_filtrado = df[df["Grupo"] == grupo_selecionado]

    # AgGrid
    colunas_visiveis = ['Classe', 'Lancamento', 'MeioPagamento', 'ValorPrincipal', 'DataLancamento']

    gb = GridOptionsBuilder.from_dataframe(df_filtrado[colunas_visiveis])
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
    gb.configure_column("Classe", rowGroup=True, hide=True, pinned="left")
    gb.configure_column("ValorPrincipal", type=["numericColumn", "numberColumnFilter", "agNumberColumnFilter"],
                        aggFunc="sum",
                        valueFormatter="(params.value != null) ? 'R$ ' + params.value.toFixed(2) : ''",
                        cellStyle={'textAlign': 'right'})
    gb.configure_grid_options(domLayout='normal',
                            groupIncludeFooter=True,
                            groupIncludeTotalFooter=True,
                            suppressAggFuncInHeader=True,
                            autoGroupColumnDef={
                                "headerName": "Classe",
                                "field": "Classe",
                                "cellRendererParams": {"suppressCount": True}
                            })

    grid_options = gb.build()

    st.markdown(f"### Detalhamento: {grupo_selecionado}")
    AgGrid(
        df_filtrado,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        theme="material",
        height=500,
        fit_columns_on_grid_load=True
    )





pagina = st.sidebar.selectbox("Menu", [ "Main","Sair"])

if pagina == "Sair":
    st.session_state.token = None
    st.session_state.username = ""
    st.rerun()
