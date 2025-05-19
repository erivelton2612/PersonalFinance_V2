# app.py
import streamlit as st
import pandas as pd
from function import *
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


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
            
    # Garantir tipo numérico
    df["ValorPrincipal"] = pd.to_numeric(df["ValorPrincipal"], errors='coerce')

    # Colunas visíveis
    colunas_visiveis = ['Classe', 'Lancamento', 'MeioPagamento', 'ValorPrincipal']

    # Grid Options
    gb = GridOptionsBuilder.from_dataframe(df[colunas_visiveis])
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)

    gb.configure_column("Classe", rowGroup=True, hide=True)

    # Configurar a coluna de valor com agregação e formatação
    gb.configure_column(
        "ValorPrincipal",
        type=["numericColumn", "numberColumnFilter", "agNumberColumnFilter"],
        aggFunc="sum",
        valueFormatter="(params.value !== undefined) ? 'R$ ' + params.value.toFixed(2) : ''",
        cellStyle={"textAlign": "right"}
    )

    # Configurações do grid
    gb.configure_grid_options(
        groupIncludeFooter=True,
        groupIncludeTotalFooter=True,
        groupDefaultExpanded=0,
        autoGroupColumnDef={
            "headerName": "Classe",
            "field": "Classe",
            "cellRendererParams": {
                "suppressCount": True
            }
        }
    )

    # Build e renderização
    gridOptions = gb.build()

    AgGrid(
        df[colunas_visiveis],
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        theme="material",
        fit_columns_on_grid_load=True,
        height=500,
    )
    st.info("Gráficos dinâmicos podem ser criados na aba Tabela usando recursos do AgGrid.")






pagina = st.sidebar.selectbox("Menu", [ "Main","Sair"])

if pagina == "Sair":
    st.session_state.token = None
    st.session_state.username = ""
    st.rerun()
