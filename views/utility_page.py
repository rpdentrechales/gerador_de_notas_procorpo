import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from auxiliar.omie_aux import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Deletar Base MongoDB")
deletar_button = st.button("Deletar Base")

if deletar_button:
    with st.status("Deletandos Bases...", expanded=True) as status:

        deletar_todos_documentos("log_clientes", query=None)
        deletar_todos_documentos("log_os", query=None)
        deletar_todos_documentos("os_processados", query=None)
        st.balloons()

        status.update(
            label="Bases deletadas", state="complete", expanded=False
        )

st.title("Adicionar Conta Corrente")

contas_correntes = load_dataframe("Auxiliar - Contas Correntes")
dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")

unidades_set = set(dados_unidade["Unidades Omie"].dropna().unique())
conta_set = set(np.append(contas_correntes["Unidade"].dropna().unique(), "teste"))

unidade_novas = unidades_set - conta_set
unidades_novas = list(unidade_novas)

if len(unidade_novas) > 0:

    seletores_1,seletores_2 = st.columns(2)

    with seletores_1:
        unidade_selecionada = st.selectbox("Selecione a Unidade",unidades_novas)
    with seletores_2:
        sigla_selecionada = st.text_input("Insira uma Sigla para CC - ex: Para Vila Matildade: VLM")

    criar_contas_botao = st.button("Criar CC novas")

    if criar_contas_botao:
        criar_contas_correntes(unidade_selecionada,sigla_selecionada)

else:
    link_da_planilha = "https://docs.google.com/spreadsheets/d/1MG2Idj77C4-qrraUyNcdE6dMCKjieV2v0lfyen2aopc"
    st.write("Não há unidades novas.")
    st.markdown(f"Para adicionar novas contas correntes, primeiro adicione os dados da Unidade na [planilha]({link_da_planilha})")


