import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
import requests
import json
import re
import time
import pymongo
from pymongo import MongoClient
import numpy as np
from auxiliar.auxiliar import *

def criar_cc(api_secret, api_key, dados_cc):

    request_data = {
        "call": "IncluirContaCorrente",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [dados_cc]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        "https://app.omie.com.br/api/v1/geral/contacorrente/",
        headers=headers,
        data=json.dumps(request_data))
    
    print(f"done: {dados_cc}")
    return response.json()


def pegar_contas_correntes(pagina_atual, api_secret, api_key):
    
    request_data = {
        "call": "ListarContasCorrentes",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [{
            "pagina": pagina_atual,
            "registros_por_pagina": 500,
            "apenas_importado_api": "S"
        }]
    }
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(
            "https://app.omie.com.br/api/v1/geral/contacorrente/",
            headers=headers,
            data=json.dumps(request_data))
        
    return response.json()


def atualizar_conta_correntes(api_secret,api_key,unidade_omie):
    # Atualiza a base de contas correntes do Omie na planilha do Google Sheets
    nome_padrao_cc = load_dataframe("Auxiliar - Dados para Criar CC")

    base_cc = load_dataframe("Auxiliar - Contas Correntes")
    
    pagina = 1
    dados_cc = pegar_contas_correntes(pagina,api_secret,api_key)

    paginas_total = dados_cc["total_de_paginas"]

    lista_final = []

    while pagina <= paginas_total:
        pagina += 1

        lista_de_contas = dados_cc["ListarContasCorrentes"]

        for conta in lista_de_contas:
    
            required_keys = {'nCodCC', 'descricao', 'cCodCCInt', 'tipo'}
            if not required_keys.issubset(conta.keys()):
                continue
    
            tipo = conta["tipo_conta_corrente"]
            tipo_mask = nome_padrao_cc["tipo_conta_corrente"] == tipo
            if tipo_mask.sum() == 0:
                continue
            else:
                nome_padrao = nome_padrao_cc.loc[tipo_mask,"Nome Padrão"].iloc[0]

            dados_da_conta = {
                                "nCodCC":conta["nCodCC"],
                                "descricao":conta["descricao"],
                                "Unidade":unidade_omie,
                                "cCodCCInt":conta["cCodCCInt"],
                                "TIPO":nome_padrao
                              }

            lista_final.append(dados_da_conta)
        dados_cc = pegar_contas_correntes(pagina,api_secret,api_key)

    contas_correntes_novas = pd.DataFrame(lista_final)

    base_para_atualizar = pd.concat([base_cc,contas_correntes_novas])
    base_para_atualizar = base_para_atualizar.drop_duplicates(subset=["cCodCCInt"])
    colunas = ["nCodCC","descricao","Unidade","cCodCCInt","TIPO"]
    base_para_atualizar = base_para_atualizar[colunas]

    update_sheet("Auxiliar - Contas Correntes", base_para_atualizar)

    return base_para_atualizar


def criar_contas_correntes(unidade_omie,codigo):

    dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")
    api_secret = dados_unidade.loc[dados_unidade["Unidades Omie"] == unidade_omie,"API Secret"].iloc[0]
    api_key = str(dados_unidade.loc[dados_unidade["Unidades Omie"] == unidade_omie,"API KEY"].iloc[0])

    dados_cc_para_criar = load_dataframe("Auxiliar - Dados para Criar CC")
    
    counter = 0
    for dados_para_criar in dados_cc_para_criar.to_dict(orient='records'):
        counter += 1
        id = dados_para_criar["id"]
        tipo_conta = dados_para_criar["tipo_conta_corrente"]
        codigo_banco = dados_para_criar["codigo_banco"]
        nome_padrao = dados_para_criar["Nome Padrão"]

        dados_cc = {
                      "cCodCCInt": f"{codigo}-{id:02d}",
                      "tipo_conta_corrente": tipo_conta,
                      "codigo_banco": codigo_banco,
                      "descricao": f"{nome_padrao} - {unidade_omie}"
                     }
        
        criar_cc(api_secret, api_key, dados_cc)

    atualizar_conta_correntes(api_secret,api_key,unidade_omie)

    st.success(f"Contas Correntes criadas com sucesso na unidade {unidade_omie}!")


def pegar_contas_teste():
    #Dados Backoffice Omie

    api_secret = "2fae495eb5679299260c3676fe88d291"
    api_key = "2485921847409"
    unidade_omie = "BackOffice"

    nome_padrao_cc = load_dataframe("Auxiliar - Dados para Criar CC")

    pagina = 1
    dados_cc = pegar_contas_correntes(pagina,api_secret,api_key)

    paginas_total = dados_cc["total_de_paginas"]

    lista_final = []
    while pagina <= paginas_total:
        pagina += 1

        lista_de_contas = dados_cc["ListarContasCorrentes"]

        for conta in lista_de_contas:
    
            required_keys = {'nCodCC', 'descricao', 'cCodCCInt', 'tipo'}
            if not required_keys.issubset(conta.keys()):
                continue
    
            nCodCC = conta["nCodCC"]
            descricao = conta["descricao"]
            cCodCCInt = conta["cCodCCInt"]
            tipo = conta["tipo_conta_corrente"]
            nome_padrao = nome_padrao_cc.loc[nome_padrao_cc["tipo_conta_corrente"] == tipo,"Nome Padrão"].iloc[0]

            dados_da_conta = {
                                "nCodCC":conta["nCodCC"],
                                "descricao":conta["descricao"],
                                "Unidade":unidade_omie,
                                "cCodCCInt":conta["cCodCCInt"],
                                "TIPO":nome_padrao
                              }

            lista_final.append(dados_da_conta)
        dados_cc = pegar_contas_correntes(pagina,api_secret,api_key)

    contas_correntes_novas = pd.DataFrame(lista_final)

    return contas_correntes_novas
        

def pegar_servicos(pagina_atual, api_secret, api_key):
    
    request_data = {
        "call": "ListarCadastroServico",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [{
            "nPagina": pagina_atual,
            "nRegPorPagina": 500
        }]
    }
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(
            "https://app.omie.com.br/api/v1/servicos/servico/",
            headers=headers,
            data=json.dumps(request_data))
        
    return response.json()       


def atualizar_servicos():
    dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")

    todos_servicos = []

    for index, row in dados_unidade.iterrows():
        unidade_omie = row["Unidades Omie"]
        api_secret = row["API Secret"]
        api_key = row["API KEY"]
        pagina_atual = 1
        servicos = pegar_servicos(pagina_atual, api_secret, api_key)
        
        servicos_cadastrados = servicos["cadastros"]

        for servico in servicos_cadastrados:
            cCodCateg = servico["cabecalho"]["cCodCateg"]
            cCodLC116 = servico["cabecalho"]["cCodLC116"]
            cCodServMun = servico["cabecalho"]["cCodServMun"]
            cDescricao = servico["cabecalho"]["cDescricao"]
            cIdTrib = servico["cabecalho"]["cIdTrib"]
            nCodServ = servico["intListar"]["nCodServ"]

            dados_servico = {
                            "unidade_omie":unidade_omie,
                            "cCodCateg":cCodCateg,
                            "cCodLC116":cCodLC116,
                            "cCodServMun":cCodServMun,
                            "cDescricao":cDescricao,
                            "cIdTrib":cIdTrib,
                            "nCodServ":nCodServ
                            }
            
            todos_servicos.append(dados_servico)

    servicos_df = pd.DataFrame(todos_servicos)
    update_sheet("Auxiliar - Serviços", servicos_df)

    return servicos_df


def pegar_clientes(pagina_atual, api_secret, api_key):
    
    request_data = {
        "call": "ListarClientesResumido",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [{
            "pagina": pagina_atual,
            "registros_por_pagina": 500,
            "apenas_importado_api": "N"
        }]
    }
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(
            "https://app.omie.com.br/api/v1/geral/clientes/",
            headers=headers,
            data=json.dumps(request_data))
        
    return response.json()     

def atualizar_base_clientes():

    dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")
    base_mongo = pegar_dados_mongodb("id_clientes")

    clientes_omie_list = []

    for index, row in dados_unidade.iterrows():
        unidade_crm = row["Unidades CRM"]
        api_secret = row["API Secret"]
        api_key = row["API KEY"]
        
        pagina_atual = 1
        clientes_data = pegar_clientes(pagina_atual, api_secret, api_key)
        pagina_total = clientes_data["total_de_paginas"]

        while pagina_atual <= pagina_total:
            todos_clientes = clientes_data["clientes_cadastro_resumido"]

            for cliente in todos_clientes:
                codigo_cliente_integracao = cliente["codigo_cliente_integracao"]
                
                if codigo_cliente_integracao != "":

                    cliente_data = {"unidade":unidade_crm,
                                    "codigo_cliente_integracao":codigo_cliente_integracao}
                    
                    clientes_omie_list.append(cliente_data)

            pagina_atual += 1

            if pagina_atual <= pagina_total:
                clientes_data = pegar_clientes(pagina_atual, api_secret, api_key)            

    clientes_omie_df = pd.DataFrame(clientes_omie_list)

    merged = clientes_omie_df.merge(base_mongo, on=['unidade', 'codigo_cliente_integracao'], how='left', indicator=True)
    missing_rows = merged.loc[merged['_merge'] == 'left_only',['unidade', 'codigo_cliente_integracao']]
    clientes_para_criar = missing_rows.to_dict('records')

    if len(clientes_para_criar) > 0:
        subir_dados_mongodb("id_clientes",clientes_para_criar)

    return clientes_para_criar
    
        
def pegar_os(pagina_atual, api_secret, api_key):
    # Por enquanto não estamos usando, mas já deixei pronta, porque talvez tenha que usar.
    request_data = {
        "call": "ListarOS",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [{
            "pagina": pagina_atual,
            "registros_por_pagina": 1000,
            "apenas_importado_api": "S"
        }]
    }
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(
            "https://app.omie.com.br/api/v1/servicos/os/",
            headers=headers,
            data=json.dumps(request_data))
        
    return response.json()     

def pegar_todos_os():
    dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")
    os_list = []

    for index, row in dados_unidade.iterrows():
        api_secret = row["API Secret"]
        api_key = row["API KEY"]
        unidade_crm = row["Unidades CRM"]
        
        pagina_atual = 1
        os_data = pegar_os(pagina_atual, api_secret, api_key)
        pagina_total = os_data["total_de_paginas"]
        
        while pagina_atual <= pagina_total:
            print(f"{unidade_crm} - {pagina_atual}/{pagina_total}")
            todos_os = os_data["osCadastro"]

            for os in todos_os:
                cCodIntOS = os["Cabecalho"]["cCodIntOS"]
                
                if cCodIntOS != "":

                    os_list.append(cCodIntOS)

            pagina_atual += 1

            if pagina_atual <= pagina_total:
                os_data = pegar_os(pagina_atual, api_secret, api_key)            

    return os_list

def deletar_os(codigo_os, api_secret, api_key):
    request_data = {
        "call": "ExcluirOS",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [{
            "cCodIntOS": codigo_os
        }]
    }
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(
            "https://app.omie.com.br/api/v1/servicos/os/",
            headers=headers,
            data=json.dumps(request_data))
        
    return response.json()

def to_native(x):
    return x.item() if isinstance(x, np.generic) else x 

def subir_linha_teste(dados_da_linha):
    # Arruma os dados da linha para subir na API do Omie

    unidade = to_native(dados_da_linha["store_name"])
    codigo_pedido = to_native(dados_da_linha["os_id"])
    codigo_integracao = codigo_pedido
    observacoes = to_native(dados_da_linha["quote_id"])
    codigo_cliente_integracao = to_native(dados_da_linha["customer_id"])
    quantidade_de_parcelas = to_native(dados_da_linha["bill_installmentsQuantity"])
    data_de_faturamento = to_native(dados_da_linha["billcharge_paidAt"])
    data_de_faturamento = pd.to_datetime(data_de_faturamento).strftime("%d/%m/%Y")

    cDadosAdicNF = str(codigo_pedido)
    nCodCC = to_native(dados_da_linha["id_conta_corrente"])

    servicos_jsons = to_native(dados_da_linha["servicos_json"]).split(";")
    servicos_array = [json.loads(servico) for servico in servicos_jsons]

    cDadosAdicNF = "Serviços prestados - " + cDadosAdicNF

    # Dados Backoffice Omie Teste!!!!!!!!!!!!!!!!!!!!!
    api_secret = "2fae495eb5679299260c3676fe88d291"
    api_key = "2485921847409"

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
        "InfoCadastro":{
            "dDtFat":data_de_faturamento},
        "Observacoes": {
            "cObsOS": observacoes
        },
        "ServicosPrestados": servicos_array
    }
    print(f"Subindo OS: {dados_os}")

    request = {
        "call": "IncluirOS",
        "app_key": api_key,
        "app_secret": api_secret,
        "param": [dados_os]
    }

    request_body = json.dumps(request)

    # Envia a requisição para criar a OS
    response = criar_os(api_secret, api_key, dados_os)
    return response