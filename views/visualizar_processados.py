import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from datetime import datetime, timedelta,time

st.set_page_config(page_title="OS Processadas", page_icon="💎",layout="wide")

st.title("OS Processadas")

today = datetime.now()
trinta_dias = today - timedelta(days=3)

data_seletor = st.date_input(
    "Selecione a data do pagamento",
    (trinta_dias, today),
    format="DD/MM/YYYY",
)

if len(data_seletor) == 2:
    data_inicial = pd.to_datetime(data_seletor[0]).strftime("%d/%m/%Y")
    data_final = pd.to_datetime(data_seletor[1]).strftime("%d/%m/%Y")
else:
    data_inicial = pd.to_datetime(data_seletor[0]).strftime("%d/%m/%Y")
    data_final = data_inicial

pegar_os_botao = st.button("Pegar OS Processadas", type="primary")

if pegar_os_botao:

    st.write(f"Buscando OS processadas entre {data_inicial} e {data_final}...")
    os_processados = criar_dataframe_os(data_inicial, data_final)

    if os_processados.empty:
        st.warning("Nenhuma OS processada encontrada nesse período.")

    else:
        os_processados["deletar"] = True
        st.session_state["os_processados_df"] = os_processados


if "os_processados_df" in st.session_state:
    os_processados = st.session_state["os_processados_df"]

    os_selecionadas = st.data_editor(
        os_processados,
        column_config={
            "id_os": st.column_config.Column("Id OS"),
            "data_faturamento": st.column_config.Column("Data de Faturamento"),
            "valor_total": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
            "unidade": st.column_config.Column("Unidade"),
            "deletar": st.column_config.CheckboxColumn("Deletar OS", default=True),
        },
        hide_index=True,
        use_container_width=True,
    )

    if st.button("Deletar OS Selecionadas", type="primary"):
        os_selecionadas = os_selecionadas[os_selecionadas["deletar"] == True]
        resultado_deletar = deletar_os_processadas(os_selecionadas)
        st.write(resultado_deletar)
        st.session_state["os_processadas_df"]