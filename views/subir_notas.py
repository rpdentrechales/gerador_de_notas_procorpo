import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *


st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas - Ajuste dataframe")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

col_data_1, col_data_2, blank_3 = st.columns([1,1,3])

with col_data_1:
  data_seletor = st.date_input(
      "Selecione a data",
      (three_days_ago, today),
      format="DD/MM/YYYY",
  )

  if len(data_seletor) == 2:
    data_inicial = data_seletor[0].strftime('%Y-%m-%d')
    data_final = data_seletor[1].strftime('%Y-%m-%d')
  else:
    data_inicial = data_seletor[0].strftime('%Y-%m-%d')
    data_final = data_inicial

with col_data_2:
  st.write("**Pegar dados do CRM**")
  pegar_dados = st.button("Executar",type="primary")

if (pegar_dados):
  dados_crm_df = paste_billcharges_with_json(data_inicial,data_final)
  st.session_state["dados_crm_df"] = dados_crm_df

if "dados_crm_df" in st.session_state:

  dados_crm_df = st.session_state["dados_crm_df"]
  dados_crm_df["Selecionar notas para subir"] = False
  columns_order = [
            "Selecionar notas para subir",
            "quote_id",
            "billCharge_id",
            "customer_id",
            "customer_name",
            "store_name",
            "quote_status",
            "paymentMethod_name",
            "billcharge_paidAt",
            "bill_installmentsQuantity",
            "bill_amount",
            "servicos_json",
            "os_id",
            "id_conta_corrente",
            "dados_cliente",
            "isPaid",
            "Tipo de Pagamento",
            "billcharge_dueAt",
            "amount"
            ]

  columns_to_disable = [
            "quote_id",
            "billCharge_id",
            "customer_id",
            "customer_name",
            "store_name",
            "quote_status",
            "paymentMethod_name",
            "billcharge_paidAt",
            "bill_installmentsQuantity",
            "bill_amount",
            "servicos_json",
            "os_id",
            "id_conta_corrente",
            "dados_cliente",
            "isPaid",
            "Tipo de Pagamento",
            "billcharge_dueAt",
            "amount"
            ]

  filtro_pagamento = st.selectbox(
    "Selecionar tipo de pagamento",
    dados_crm_df["Tipo de Pagamento"].unique(),
    index=None
    )
  filtered_df = dados_crm_df.loc[dados_crm_df["Tipo de Pagamento"] == filtro_pagamento]

  st.write("**Selecione notas para subir**")

  if filtro_pagamento:
    filtered_df
    dados_CRM_df = st.data_editor(filtered_df,
                   hide_index=True,
                   column_order=columns_order,
                   disabled=columns_to_disable
                   )

  subir_clientes_botao = st.button("Subir Clientes",type="primary")

  if subir_clientes_botao:

    selected_df = dados_CRM_df.loc[dados_CRM_df["Selecionar notas para subir"] == True]
    base_compilada = resultados = compilar_linhas_para_subir(selected_df)
    clientes_subidos = criar_clientes_selecionados(base_compilada)
    os_subidos = criar_ordens_de_servico_da_planilha(base_compilada)

    st.write(os_subidos)
