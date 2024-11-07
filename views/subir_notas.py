import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *


st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

col_data_1, col_data_2, blank_3 = st.columns([1,1,2])

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

  clientes_sem_endereco_df = dados_crm_df.loc[dados_crm_df["dados_cliente"] == "Cliente sem endereço"]
  colunas_cliente_sem_endereco = ["quote_id","customer_id","customer_name","store_name"]
  visualisar_clientes_sem_endereco = clientes_sem_endereco_df[colunas_cliente_sem_endereco].drop_duplicates()
  quantidade_clientes_sem_endereco = len(visualisar_clientes_sem_endereco)

  @st.dialog("Clientes Sem Endereço", width="large")
  def abrir_clientes_sem_endereco():
    st.write("Lista de clientes sem endereço:")
    st.dataframe(visualisar_clientes_sem_endereco,use_container_width=True,hide_index=True)

  clientes_sem_endereco_botao = st.button(f"{quantidade_clientes_sem_endereco} Clientes Sem Endereço",type="secondary")

  if clientes_sem_endereco_botao:
    abrir_clientes_sem_endereco()

  dados_crm_df = dados_crm_df.loc[dados_crm_df["dados_cliente"] != "Cliente sem endereço"]

  filtro_col_1, filtro_col_2, filtro_col_3 = st.columns(3)

  with filtro_col_1:

    filtro_pagamento = st.selectbox(
      "Selecionar tipo de pagamento",
      dados_crm_df["Tipo de Pagamento"].unique(),
      index=0
      )

  filtered_df = dados_crm_df.loc[dados_crm_df["Tipo de Pagamento"] == filtro_pagamento]

  with filtro_col_2:
    unidades = list(filtered_df["store_name"].unique())
    unidades.insert(0,"TODAS")

    filtro_unidade = st.selectbox(
      "Selecionar unidade",
      unidades,
      index=0
      )

  if filtro_unidade != "TODAS":
    filtered_df = filtered_df.loc[dados_crm_df["store_name"] == filtro_unidade]

  with filtro_col_3:

    soma = filtered_df["amount"].sum()
    soma = f"R$ {soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric(label="Valor Total", value=soma)

  st.write("**Selecione notas para subir**")

  seletor_subir_tudo = st.toggle("Subir Tudo")

  if seletor_subir_tudo:
    filtered_df["Selecionar notas para subir"] = True
    columns_order.remove("Selecionar notas para subir")

  edited_df = st.data_editor(filtered_df,
                  hide_index=True,
                  column_order=columns_order,
                  disabled=columns_to_disable
                  )
  
  gerar_notas_botao = st.button("Gerar Notas",type="primary")

  if gerar_notas_botao:

    with st.status("Criando Notas...", expanded=True) as status:

      st.write("Compilando Base...")

      selected_df = edited_df.loc[edited_df["Selecionar notas para subir"] == True]
      base_compilada = compilar_linhas_para_subir(selected_df)

      st.write("Criando Clientes...")
      clientes_subidos = criar_clientes_selecionados(base_compilada)
      clientes_subidos = clientes_subidos.to_dict(orient='records')
      subir_dados_mongodb("log_clientes",clientes_subidos)

      st.write("Criando Ordens de Serviço...")
      os_subidos = criar_ordens_de_servico_da_planilha(base_compilada)
      os_subidos = os_subidos.to_dict(orient='records')
      subir_dados_mongodb("log_os",os_subidos)

      status.update(
          label="Notas Criadas!", state="complete", expanded=False
      )
