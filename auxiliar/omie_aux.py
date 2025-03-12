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
            "apenas_importado_api": "N"
        }]
    }
    
    headers = {"Content-Type": "application/json"}

    response = requests.post(
            "https://app.omie.com.br/api/v1/geral/contacorrente/",
            headers=headers,
            data=json.dumps(request_data))
        
    return response.json()


def atualizar_conta_correntes(unidade_omie):
    dados_unidade = load_dataframe("Auxiliar - Chave das APIs por Unidade")
    api_secret = dados_unidade.loc[dados_unidade["Unidades Omie"] == unidade_omie,"API Secret"].iloc[0]
    api_key = str(dados_unidade.loc[dados_unidade["Unidades Omie"] == unidade_omie,"API KEY"].iloc[0])

    nome_padrao_cc = dados_unidade = load_dataframe("Auxiliar - Dados para Criar CC")

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

    base_para_atualizar = pd.concat([base_cc,contas_correntes_novas])
    base_para_atualizar = base_para_atualizar.drop_duplicates(subset=["cCodCCInt"])
    colunas = ["nCodCC","descricao","Unidade","cCodCCInt","TIPO"]
    base_para_atualizar = base_para_atualizar[colunas]

    update_sheet("Auxiliar - Contas Correntes", base_para_atualizar)

    return base_para_atualizar


def criar_contas_correntes(unidade_omie,codigo):

    api_secret = "2fae495eb5679299260c3676fe88d291"
    api_key = "2485921847409"
    dados_cc_para_criar = load_dataframe("Auxiliar - Dados para Criar CC")

    for dados_para_criar in dados_cc_para_criar.to_dict(orient='records'):

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


def pegar_contas_teste():
    #Dados Backoffice Omie

    api_secret = "2fae495eb5679299260c3676fe88d291"
    api_key = "2485921847409"
    unidade_omie = "BackOffice"
    


    nome_padrao_cc = dados_unidade = load_dataframe("Auxiliar - Dados para Criar CC")

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
        
        




    


