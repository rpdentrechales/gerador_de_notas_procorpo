import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from auxiliar.omie_aux import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

@st.dialog("Deletar CC", width=500)
def deletar_cc_dialog():
    st.write("Deletar Conta Corrente")
    contas_correntes["contas para deletar"] = False
    selected_data = st.data_editor(contas_correntes, use_container_width=True, hide_index=True)
    
    if st.button("Deletar CC selecionadas"):
        contas_para_deletar = selected_data[selected_data["contas para deletar"] == True]
        for index, row in contas_para_deletar.iterrows():
            unidade = row["Unidade"]
            nCodCC = row["nCodCC"]
            api_secret = dados_unidade.loc[dados_unidade["Unidades Omie"] == unidade, "API Secret"].values[0]
            api_key = dados_unidade.loc[dados_unidade["Unidades Omie"] == unidade, "API Key"].values[0]
            
            try:
                deletar_contas_correntes(api_secret, api_key, nCodCC)
                st.write(f"Conta Corrente {nCodCC} da unidade {unidade} deletada com sucesso.")
            except Exception as e:
                st.write(f"Erro ao deletar a conta corrente {nCodCC} da unidade {unidade}: {e}")
        
        contas_para_manter = selected_data[selected_data["contas para deletar"] == False]
        update_sheet("Auxiliar - Contas Correntes", contas_para_manter)           

st.title("Deletar Base MongoDB")
st.caption("Deleta dados das bases 'Log Clientes', 'Log OS' e 'OS Processados' do MongoDB")
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

link_da_planilha = "https://docs.google.com/spreadsheets/d/1MG2Idj77C4-qrraUyNcdE6dMCKjieV2v0lfyen2aopc"

if len(unidade_novas) > 0:

    seletores_1,seletores_2 = st.columns(2)

    with seletores_1:
        unidade_selecionada = st.selectbox("Selecione a Unidade",unidades_novas)
    with seletores_2:
        sigla_selecionada = st.text_input("Insira uma Sigla para CC - ex: Para Vila Matildade: VLM")

    criar_contas_botao = st.button("Criar CC novas")

    if criar_contas_botao:
        criar_contas_correntes(unidade_selecionada,sigla_selecionada)
    
    st.markdown(f"[Link para cadastrar Unidades Novas]({link_da_planilha})")

else:
    
    st.write("Não há unidades novas.")
    st.markdown(f"Para adicionar novas contas correntes, primeiro adicione os dados da Unidade na [planilha]({link_da_planilha}).")

st.title("Deletar Contas Correntes:")
if st.button("Deletar CC"):
    deletar_cc_dialog()



st.title("Atualizar Base de Clientes")
st.write("Baixa os ids de clientes do OMiE e atualiza a base de clientes no MongoDB que o script usa para verificar se há a necessidade de criar clientes novos")
atualizar_clientes_button = st.button("Atualizar Base de Clientes")

if atualizar_clientes_button:
    clientes_omie = atualizar_base_clientes()
    st.write(f"{len(clientes_omie)} clientes novos criados")

st.write("Last Update - 27/03/2025")