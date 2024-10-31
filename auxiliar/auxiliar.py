import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
import requests
import json
import re
import time

def load_dataframe(worksheet):

  conn = st.connection("gsheets", type=GSheetsConnection)
  df = conn.read(worksheet=worksheet)

  return df

def update_sheet(worksheet, df):
    conn = st.connection("gsheets", type=GSheetsConnection)
    conn.update(data=df,worksheet=worksheet)
    return df

def query_BillCharges(current_page, start_date, end_date):

    # API URL and token
    baseURL = "https://open-api.eprocorpo.com.br/graphql"
    token = "145418|arQc09gsrcSNJipgDRaM4Ep6rl3aJGkLtDMnxa0u"

    # Define headers and payload
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'query': '''
            query ($filters: BillChargeFiltersInput, $pagination: PaginationInput) {
                fetchBillCharges(filters: $filters, pagination: $pagination) {
                    data {
                        quote {
                            id
                            customer {
                                id
                                name
                                taxvat
                                email
                                address {
                                    street
                                    number
                                    neighborhood
                                    additional
                                    city
                                    state {
                                        abbreviation
                                    }
                                    postcode
                                }
                            }
                            status
                            bill {
                                installmentsQuantity
                                total
                                items {
                                    amount
                                    discountAmount
                                    description
                                    quantity
                                }
                            }
                        }
                        store {
                            name
                        }
                        amount
                        id
                        paidAt
                        dueAt
                        isPaid
                        paymentMethod {
                            name
                        }
                    }
                }
            }''',
        'variables': {
            'filters': {
                'paidAtRange': {
                    'start': start_date,
                    'end': end_date,
                }
            },
            'pagination': {
                'currentPage': current_page,
                'perPage': 500,
            }
        }
    }

    try:
        # Make the request
        response = requests.post(baseURL, headers=headers, data=json.dumps(payload))

        # Return the response JSON
        return response.json()

    except requests.exceptions.RequestException as err:
        # Return the error if any occurs
        return str(err)

def gerar_obj_api():
    api_data = load_dataframe("Auxiliar - Chave das APIs por Unidade")

    api_data_por_unidade = {}

    for _, row in api_data.iterrows():
        unidade = row[0]
        api_secret = row[2]
        api_key = row[3]

        api_data_obj = {"api_secret": api_secret, "api_key": api_key}

        api_data_por_unidade[unidade] = api_data_obj

    return api_data_por_unidade

def gerar_obj_aliquota():
    aliquota_data = load_dataframe("Auxiliar - Alíquotas")

    aliquota_data_por_cidade = {}

    for _, row in aliquota_data.iterrows():
        codigo_municipio = row[0]
        aliquota = row[1]
        cidade = row[2]

        aliquota_data_obj = {"codigo_municipio": codigo_municipio, "aliquota": aliquota}

        aliquota_data_por_cidade[cidade] = aliquota_data_obj

    return aliquota_data_por_cidade

def gerar_obj_cc():
    dados_conta_corrente = load_dataframe("Auxiliar - Contas Correntes")

    cc_obj_array = []

    for _, row in dados_conta_corrente.iterrows():
        id_cc = row[0]
        unidade = row[2]
        tipo_pagamento = row[4]

        cc_obj = {
            "unidade": unidade,
            "id_conta": id_cc,
            "tipo_pagamento": tipo_pagamento
        }

        cc_obj_array.append(cc_obj)

    return cc_obj_array

def gerar_obj_tipo_pagamento():
    dados_tipo_de_pagamento = load_dataframe("Auxiliar - Tipo de Pagamento")

    tipo_pagamento_obj = {}

    for _, row in dados_tipo_de_pagamento.iterrows():
        tipo_de_pagamento = row[0]
        conta_corrente = row[1]

        tipo_pagamento_obj[tipo_de_pagamento] = conta_corrente

    return tipo_pagamento_obj

def find_cc_id(cc_obj_array, tipo_pagamento_obj, unidade_planilha, forma_pagamento_planilha):
    tipo_pagamento_planilha = tipo_pagamento_obj.get(forma_pagamento_planilha)

    for row in cc_obj_array:
        unidade = row['unidade']
        id_conta = row['id_conta']
        tipo_pagamento = row['tipo_pagamento']

        if unidade_planilha == unidade:
            if tipo_pagamento_planilha == tipo_pagamento:
                return id_conta

    return "Tipo de Pagamento inválido"

def gerar_obj_unidades():
    unidades_data = load_dataframe("Auxiliar - Chave das APIs por Unidade")

    unidades_obj = {}

    for _, row in unidades_data.iterrows():
        unidade_crm = row[0]
        unidade_omie = row[1]
        cidade = row[4]

        unidades_obj[unidade_crm] = {"unidade_omie": unidade_omie, "cidade": cidade}

    return unidades_obj

def paste_billcharges_with_json(start_date, end_date):
    # Fetch dates and initialize variables
    current_page = 1

    # Load data from the other helper functions
    cc_obj_array = gerar_obj_cc()
    tipo_pagamento_obj = gerar_obj_tipo_pagamento()
    unidades_obj = gerar_obj_unidades()
    aliquota_obj = gerar_obj_aliquota()

    # First API query to get BillCharges
    results = query_BillCharges(current_page, start_date, end_date)
    billcharges_data = results['data']['fetchBillCharges']['data']
    billcharges_data_length = len(billcharges_data)

    # Initialize sheet data array
    sheet_array = [["quote_id", "billCharge_id", "customer_id", "customer_name", "store_name", "quote_status",
                    "paymentMethod_name", "billcharge_paidAt", "bill_installmentsQuantity", "bill_amount",
                    "servicos_json", "os_id", "id_conta_corrente", "dados_cliente", "isPaid", "Tipo de Pagamento",
                    "billcharge_dueAt", "amount"]]

    # Main loop to process data
    while billcharges_data_length > 0:
        for data_row in billcharges_data:
            quote_items = data_row['quote']['bill']['items']

            # Extract necessary fields
            quote_id = data_row['quote']['id']
            billCharge_id = data_row['id']
            customer_id = data_row['quote']['customer']['id']
            customer_name = data_row['quote']['customer']['name']
            store_name = data_row['store']['name']
            quote_status = data_row['quote']['status']
            paymentMethod_name = data_row['paymentMethod']['name']
            billcharge_paidAt = data_row['paidAt']
            billcharge_dueAt = data_row['dueAt']
            bill_installmentsQuantity = data_row['quote']['bill']['installmentsQuantity']
            bill_amount = data_row['amount'] / 100
            customer_document = data_row['quote']['customer']['taxvat']
            isPaid = data_row['isPaid']

            # Continue if conditions are not met
            if not isPaid or quote_status != "completed":
                continue

            regex_pagamentos_para_excluir = r".*Crédito Promocional.*|.*Utilizar Crédito.*|.*INKLO.*|.*CRMBonus.*"
            if re.search(regex_pagamentos_para_excluir, paymentMethod_name):
                continue

            # Process customer address
            customer_address = data_row['quote']['customer']['address']
            if customer_address:
                dados_cliente = {
                    "razao_social": customer_name,
                    "cnpj_cpf": customer_document,
                    "codigo_cliente_integracao": customer_id,
                    "endereco": customer_address['street'],
                    "endereco_numero": customer_address['number'],
                    "bairro": customer_address['neighborhood'],
                    "complemento": customer_address['additional'],
                    "estado": customer_address['state']['abbreviation'],
                    "cidade": customer_address['city'],
                    "cep": customer_address['postcode'],
                    "email": data_row['quote']['customer']['email']
                }
                dados_cliente = json.dumps(dados_cliente)
            else:
                dados_cliente = "Cliente sem endereço"

            # Process unit and aliquota data
            dados_da_unidade = unidades_obj.get(store_name)
            if not dados_da_unidade:
                continue

            unidade_omie = dados_da_unidade['unidade_omie']
            cidade = dados_da_unidade['cidade']
            dados_aliquotas = aliquota_obj.get(cidade)
            codigo_municipio = dados_aliquotas['codigo_municipio']
            aliquota = dados_aliquotas['aliquota']

            # Find account ID
            id_conta_corrente = find_cc_id(cc_obj_array, tipo_pagamento_obj, unidade_omie, paymentMethod_name)

            # Process service and payment types
            servico_obj = {
                "cDadosAdicItem": f"Serviço Prestado - {billCharge_id}",
                "cTribServ": "01",
                "cCodServMun": codigo_municipio,
                "cCodServLC116": "6.02",
                "nQtde": 1,
                "nValUnit": bill_amount,
                "cRetemISS": "N",
                "nValorDesconto": 0,
                "cTpDesconto": "V",
                "impostos": {
                    "nAliqISS": aliquota
                }
            }
            servico_obj = json.dumps(servico_obj)

            # Process recurring payments and service order ID
            regex_recorrente = r".*Recorrente.*"
            if re.search(regex_recorrente, paymentMethod_name, re.IGNORECASE):
                os_id = str(quote_id)  # Convert to string
                tipo_de_pagamento = "Recorrente"
            else:
                os_id = str(quote_id)  # Convert to string
                regex_pagamentos_em_dinheiro = r".*PIX.*|.*Dinheiro.*|.*Transferência.*"
                if re.search(regex_pagamentos_em_dinheiro, paymentMethod_name):
                    tipo_de_pagamento = "Pontual - Dinheiro"
                    os_id = f"{os_id}-00"  # Concatenate strings
                else:
                    tipo_de_pagamento = "Pontual - Cartão"
                    os_id = f"{os_id}-01"  # Concatenate strings

            # Add processed row to sheet array
            sheet_row = [quote_id, billCharge_id, customer_id, customer_name, store_name, quote_status, paymentMethod_name,
                         billcharge_paidAt, bill_installmentsQuantity, bill_amount, servico_obj, os_id, id_conta_corrente,
                         dados_cliente, isPaid, tipo_de_pagamento, billcharge_dueAt, bill_amount]
            sheet_array.append(sheet_row)

        # Fetch the next page of results
        current_page += 1
        results = query_BillCharges(current_page, start_date, end_date)
        billcharges_data = results['data']['fetchBillCharges']['data']
        billcharges_data_length = len(billcharges_data)

    billcharges_df = pd.DataFrame(sheet_array[1:], columns=sheet_array[0])
    # Update the Google Sheets with the processed data
    # update_sheet("CRM - Billcharges (Json)", billcharges_df)

    return billcharges_df

def criar_os(api_secret, api_key, dados_ordem):
    # Requisição da API do Omie para criar Ordem de Serviço
    st.write(dados_ordem)
    request = {
        "call": "IncluirOS",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [dados_ordem]
    }

    request_body = json.dumps(request)
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post("https://app.omie.com.br/api/v1/servicos/os/", headers=headers, data=request_body)

    data = response.json()

    return data

def criar_ordens_de_servico_da_planilha(linhas_selecionadas):
  resultados = []

  for index, linha in linhas_selecionadas.iterrows():

    resposta = subir_linha(linha)
    resultados.append([linha,resposta])

  resultados_df = pd.DataFrame(resultados,columns=["Dados","resposta"])

  return resultados_df

def subir_linha(dados_da_linha):
    # Arruma os dados da linha para subir na API do Omie

    unidade = dados_da_linha["store_name"]
    codigo_pedido = dados_da_linha["os_id"]
    codigo_integracao = codigo_pedido
    observacoes = dados_da_linha["quote_id"]
    codigo_cliente_integracao = dados_da_linha["customer_id"]
    quantidade_de_parcelas = dados_da_linha["bill_installmentsQuantity"]

    cDadosAdicNF = str(codigo_pedido)
    nCodCC = dados_da_linha["id_conta_corrente"]

    servicos_jsons = dados_da_linha["servicos_json"].split(";")
    servicos_array = [json.loads(servico) for servico in servicos_jsons]

    cDadosAdicNF = "Serviços prestados - " + cDadosAdicNF

    # Busca as chaves da API
    chaves_api = gerar_obj_api()
    api_secret = chaves_api[unidade]["api_secret"]
    api_key = chaves_api[unidade]["api_key"]

    # Define a quantidade de parcelas e outras informações da OS
    codigo_parcela = "000"

    dados_os = {
        "Cabecalho": {
            "cCodIntOS": codigo_integracao,
            "cCodIntCli": codigo_cliente_integracao,
            "cEtapa": "50",
            "cCodParc": codigo_parcela,
            "nQtdeParc": quantidade_de_parcelas
        },
        "InformacoesAdicionais": {
            "cDadosAdicNF": cDadosAdicNF,
            "cCodCateg": "1.01.02",
            "nCodCC": nCodCC,
            "cNumPedido": codigo_pedido
        },
        "Observacoes": {
            "cObsOS": observacoes
        },
        "ServicosPrestados": servicos_array
    }

    # json_string = json.dumps(dados_os)

    # Envia a requisição para criar a OS
    response = criar_os(api_secret, api_key, dados_os)
    return response

def criar_clientes_selecionados(base_df):

  chaves_api = gerar_obj_api()
  resultados = [["client_id","Resultado","Response"]]
  counter = 0

  for index,row in base_df.iterrows():

    dados_cliente = row["dados_cliente"]
    unidade = row["store_name"]
    id_do_cliente = row["customer_id"]

    api_secret = chaves_api[unidade]["api_secret"]
    api_key = chaves_api[unidade]["api_key"]

    cadastro_novo = False
    result_status = "Error"

    try:
      dados_cliente = json.loads(dados_cliente)  # Tenta converter a string JSON para um dicionário Python
    except json.JSONDecodeError:
      result_status = "Erro ao converter JSON"
      full_response = "Erro ao converter JSON"
      resultados.append([id_do_cliente,result_status,full_response])
      continue  # Pula para a próxima iteração

    id_cliente = dados_cliente["codigo_cliente_integracao"]

    full_response = criar_cliente(api_secret,api_key,dados_cliente)
    full_response = check_response(full_response)

    if full_response:
        if re.search(r"Cliente cadastrado com sucesso.", full_response):
            # Checa se é cliente novo
            cadastro_novo = True
            result_status = "Cliente Novo Cadastrado"

        if re.search(r"código de integração \[\]", full_response):
          regex = r"com o Id \[([0-9]+)\]"
          match = re.search(regex, full_response)
          codigo_omie = match.group(1)

          dados_cliente = {
              "codigo_cliente_omie": codigo_omie,
              "codigo_cliente_integracao": id_cliente
          }

          associar_cliente = associar_id_cliente(dados_cliente, api_secret, api_key)
          full_response = check_response(associar_cliente)

          if full_response:
            result_status = "Id do Cliente Associado"
          else:
            result_status = "Erro ao Associar Id do Cliente"

    if not cadastro_novo:
        # Se não for cadastro novo, atualiza os dados do cliente
        atualizar_dados = alterar_dados(dados_cliente, api_secret, api_key)
        full_response = check_response(atualizar_dados)

        if full_response:
          result_status = "Cadastro do cliente atualizado"
        else:
          result_status = "Erro ao Atualizar Cadastro do Cliente"

    if counter % 20 == 0:
        time.sleep(5)  # Aguarda 5 segundos

    resultados.append([id_do_cliente,result_status,full_response])
    counter += 1

  resultados_df = pd.DataFrame(resultados[1:], columns=resultados[0])
  return resultados_df

def criar_cliente(api_secret, api_key, dados_cliente):

    request = {
        "call": "IncluirCliente",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [dados_cliente]
    }

    request_body = json.dumps(request)

    headers = {
        "Content-Type": "application/json"
    }

    # Usa POST para enviar os dados
    response = requests.post("https://app.omie.com.br/api/v1/geral/clientes/", headers=headers, data=request_body)

    response_text = response.json()

    return response_text

def associar_id_cliente(dados_cliente, api_secret, api_key):
    # Requisição para associar código de integração do cliente

    request = {
        "call": "AssociarCodIntCliente",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [dados_cliente]
    }

    request_body = json.dumps(request)

    headers = {
        "Content-Type": "application/json"
    }

    # Usa POST para enviar os dados
    response = requests.post("https://app.omie.com.br/api/v1/geral/clientes/", headers=headers, data=request_body)

    response_text = response.json()

    return response_text

def alterar_dados(dados_cliente, api_secret, api_key):
    # Requisição para alterar dados do cliente

    request = {
        "call": "AlterarCliente",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [dados_cliente]
    }

    request_body = json.dumps(request)

    headers = {
        "Content-Type": "application/json"
    }

    # Usa POST para enviar os dados
    response = requests.post("https://app.omie.com.br/api/v1/geral/clientes/", headers=headers, data=request_body)

    response_text = response.json()

    return response_text

def check_response(response):

  # Check if response is fault or sucessfull

    if 'faultstring' in response:
        return response['faultstring']
    elif 'descricao_status' in response:
        return response['descricao_status']
    else:
        return None

def update_value_json(row):

    json_obj = json.loads(row['servicos_json'])  
    json_obj['nValUnit'] = row['bill_amount']  
    st.write(f"Update Valeu: {row['bill_amount']}")
    return json.dumps(json_obj) 

def compilar_linhas_para_subir(df_selecionado):
  df_groupby = df_selecionado.groupby(["os_id"]).agg({'bill_amount': 'sum'})

  df_drop_duplicates = df_selecionado.drop_duplicates(subset=["os_id"],keep="first")
  df_drop_duplicates = df_drop_duplicates.drop(columns=["bill_amount"])
  
  df_merge = pd.merge(df_drop_duplicates, df_groupby, on="os_id")

  df_merge['json_data'] = df_merge.apply(update_value_json, axis=1)

  return df_merge
