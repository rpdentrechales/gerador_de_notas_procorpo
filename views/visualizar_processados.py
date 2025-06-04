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
    "Selecione a data de conciliação",
    (trinta_dias, today),
    format="DD/MM/YYYY",
)

st.caption("Note que a data de conciliação é a data em que o pagamento foi feito e não a data de criação da OS.")

if len(data_seletor) == 2:
    data_inicial = pd.to_datetime(data_seletor[0]).strftime("%d/%m/%Y")
    data_final = pd.to_datetime(data_seletor[1]).strftime("%d/%m/%Y")
else:
    data_inicial = pd.to_datetime(data_seletor[0]).strftime("%d/%m/%Y")
    data_final = data_inicial

pegar_os_botao = st.button("Pegar OS Processadas", type="primary")

if pegar_os_botao:

    if "os_processadas_df" in st.session_state:
        remover_df = st.session_state.pop("os_processadas_df", None)

    st.write(f"Buscando OS processadas entre {data_inicial} e {data_final}...")
    os_processados = criar_dataframe_os(data_inicial, data_final)

    if os_processados.empty:
        st.warning("Nenhuma OS processada encontrada nesse período.")

    else:
        os_processados["deletar"] = True
        st.session_state["os_processadas_df"] = os_processados


if "os_processadas_df" in st.session_state:
    os_processados = st.session_state["os_processadas_df"]

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
        if os_selecionadas.empty:
            st.warning("Nenhuma OS selecionada para deletar.")
        else:
            st.write(f"Deletando {len(os_selecionadas)} OS selecionadas...")
            resultado_deletar = deletar_os_processadas(os_selecionadas)
            st.write(f"Os_deletadas: {resultado_deletar}")
            remover_df = st.session_state.pop("os_processadas_df", None)

            