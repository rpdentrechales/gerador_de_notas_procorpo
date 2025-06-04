import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
import math

st.set_page_config(page_title="Subir Notas", page_icon="💎",layout="wide")

st.title("Subir Notas")

today = datetime.datetime.now()
three_days_ago = today - timedelta(days=3)

col_data_1, col_data_2, col_data_3 = st.columns([1,1,2])

with col_data_1:
  data_seletor = st.date_input(
      "Selecione a data",
      (three_days_ago, today),
      format="DD/MM/YYYY",
  )

  if len(data_seletor) == 2:
    data_inicial = data_seletor[0].strftime('%Y-%m-%d')
    data_inicial_br  = data_seletor[0].strftime('%d/%m/%Y')

    data_final = data_seletor[1].strftime('%Y-%m-%d')
    data_final_br  = data_seletor[1].strftime('%d/%m/%Y')
  else:
    data_inicial = data_seletor[0].strftime('%Y-%m-%d')
    data_inicial_br  = data_seletor[0].strftime('%d/%m/%Y')

    data_final = data_inicial
    data_final_br = data_inicial_br

with col_data_2:
  st.write("")
  pegar_dados = st.button("Executar",type="primary")

with col_data_3:
  st.caption("**Pegar dados do CRM**")
  
if (pegar_dados):
  dados_crm_df = paste_billcharges_with_json(data_inicial,data_final)
  ids_os_subidos = pegar_todos_os(data_inicial_br,data_final_br)
  
  if len(ids_os_subidos) == 0:
    dados_crm_df['os_na_base'] = False

  else:
    dados_crm_df['os_na_base'] = dados_crm_df['os_id'].isin(ids_os_subidos)

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
            "amount",
            "os_na_base"
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
            "amount",
            "os_na_base",
            "linha_com_erros"
            ]

  clientes_sem_cadastro_df = dados_crm_df.loc[dados_crm_df["linha_com_erros"] == True]
  colunas_cliente_sem_cadastro = ["quote_id","customer_id","customer_name","store_name","paymentMethod_name","dados_cliente"]
  visualisar_clientes_sem_cadastro = clientes_sem_cadastro_df[colunas_cliente_sem_cadastro].drop_duplicates()
  quantidade_clientes_sem_cadastro = len(visualisar_clientes_sem_cadastro)

  @st.dialog("Clientes Sem Cadastro", width="large")
  def abrir_clientes_sem_cadastro():
    st.write("Lista de clientes sem Cadastro:")
    st.dataframe(visualisar_clientes_sem_cadastro,use_container_width=True,hide_index=True)

  clientes_sem_cadastro_botao = st.button(f"{quantidade_clientes_sem_cadastro} Clientes Sem Cadastro",type="secondary")

  if clientes_sem_cadastro_botao:
    abrir_clientes_sem_cadastro()

  dados_crm_df = dados_crm_df.loc[~dados_crm_df["dados_cliente"].str.contains("Cadastro inválido", na=False)]

  filtro_col_1, filtro_col_2, filtro_col_3, filtro_col_4, filtro_col_5 = st.columns(5)

  with filtro_col_1:

    filtro_pagamento = st.selectbox(
      "Selecionar tipo de pagamento",
      dados_crm_df["Tipo de Pagamento"].unique(),
      index=0
      )

  filtered_df = dados_crm_df.loc[dados_crm_df["Tipo de Pagamento"] == filtro_pagamento]
  filtered_df_sem_cadastro = clientes_sem_cadastro_df.loc[clientes_sem_cadastro_df["Tipo de Pagamento"] == filtro_pagamento]

  with filtro_col_2:
    unidades = list(filtered_df["store_name"].sort_values().unique())
    unidades.insert(0,"TODAS")

    filtro_unidade = st.selectbox(
      "Selecionar unidade",
      unidades,
      index=0
      )

  if filtro_unidade != "TODAS":
    filtered_df = filtered_df.loc[filtered_df["store_name"] == filtro_unidade]
    filtered_df_sem_cadastro = filtered_df_sem_cadastro.loc[filtered_df_sem_cadastro["store_name"] == filtro_unidade]

  with filtro_col_3:

    soma = filtered_df["amount"].sum()
    soma_string = f"R$ {soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric(label="Valor Total - Cliente com Cadastro", value=soma_string)

  with filtro_col_4:

    soma_sem_cadastro = filtered_df_sem_cadastro["amount"].sum()
    soma_sem_cadastro_string = f"R$ {soma_sem_cadastro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric(label="Valor Total - Cliente sem Cadastro", value=soma_sem_cadastro_string)

  with filtro_col_5:

    soma_total = soma+soma_sem_cadastro
    soma_total_string = f"R$ {soma_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.metric(label="Valor Total", value=soma_total_string)

  seletor_1,seletor_2 = st.columns(2)
  
  with seletor_1:
    st.write("**Selecione notas para subir**")

    seletor_subir_tudo = st.toggle("Subir Tudo")

    if seletor_subir_tudo:
      filtered_df["Selecionar notas para subir"] = True
      columns_order.remove("Selecionar notas para subir")
  
  with seletor_2:
    st.write("Selecione notas para visulizar")
    
    seletor_visualizar = st.toggle("Ocultar ids processados",value=True)

    if seletor_visualizar:
      filtered_df = filtered_df.loc[filtered_df["os_na_base"] == False]

  edited_df = st.data_editor(filtered_df,
                  hide_index=True,
                  column_order=columns_order,
                  disabled=columns_to_disable
                  )

  st.write(f"Total de linhas: {filtered_df.shape[0]}")

  gerar_notas_botao = st.button("Gerar Notas",type="primary")

  if gerar_notas_botao:

    with st.status("Criando Notas...", expanded=True) as status:

      st.write("Compilando Base...")

      selected_df = edited_df.loc[edited_df["Selecionar notas para subir"] == True]
      base_compilada = compilar_linhas_para_subir(selected_df)
      linhas_para_subir = base_compilada.shape[0]
      
      st.write(f"Itens pós compilação: {linhas_para_subir}")
      st.write(f"Tempo estimado: {math.ceil(linhas_para_subir/30)} minutos")      
      
      st.write("Criando Clientes...")
      clientes_subidos = criar_clientes_selecionados(base_compilada)
      st.write("Clientes criados")
      st.write(f"Relatório de erros: {clientes_subidos}")

      st.write("Criando Ordens de Serviço...")
      os_subidos = criar_ordens_de_servico_da_planilha(base_compilada)
      os_subidos_dic = os_subidos.to_dict(orient='records')
      subir_dados_mongodb("log_os",os_subidos_dic)

      erros_mask = os_subidos["resposta"].astype(str).str.contains("ERROR", case=False, na=False)
      ids_para_subir = os_subidos.loc[~erros_mask,"os_id"]
      base_para_subir = dados_crm_df.loc[dados_crm_df['os_id'].isin(ids_para_subir)]
      base_para_subir = base_para_subir.drop_duplicates()
      base_para_subir_dic = base_para_subir.to_dict(orient='records')
      subir_dados_mongodb("os_processados",base_para_subir_dic)

      status.update(
          label="Notas Criadas!", state="complete", expanded=False
      )