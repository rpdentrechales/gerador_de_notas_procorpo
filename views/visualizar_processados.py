import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from datetime import datetime, timedelta,time

st.set_page_config(page_title="OS Processadas", page_icon="💎",layout="wide")

st.title("OS Processadas")

today = datetime.now().date()
trinta_dias = today - timedelta(days=30)

data_seletor = st.date_input(
    "Selecione a data",
    (trinta_dias, today),
    format="DD/MM/YYYY",
)

if isinstance(data_seletor, (list, tuple)) and len(data_seletor) == 2:
    data_inicial = datetime.combine(data_seletor[0], time.min)
    data_final = datetime.combine(data_seletor[1], time.max)
else:
    data_inicial = datetime.combine(data_seletor, time.min)
    data_final = datetime.combine(data_seletor, time.max)

query = {
    "billcharge_paidAt": {
        "$gte": data_inicial,
        "$lte": data_final
    }
}

st.write(query)

pegar_dados_button = st.button("Pegar dados")

if pegar_dados_button:

    colunas = ['quote_id', 'billCharge_id', 'customer_id', 'customer_name',
       'store_name', 'quote_status', 'paymentMethod_name', 'billcharge_paidAt',
       'bill_installmentsQuantity', 'bill_amount', 'servicos_json', 'os_id',
       'id_conta_corrente', 'dados_cliente', 'isPaid', 'Tipo de Pagamento',
       'billcharge_dueAt', 'amount']
    
    os_processados = pegar_dados_mongodb("os_processados",query=query)
    
    st.dataframe(os_processados,hide_index=True)