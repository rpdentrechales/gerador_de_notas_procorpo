import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from datetime import datetime, timedelta,time

st.set_page_config(page_title="OS Processadas", page_icon="💎",layout="wide")

st.title("OS Processadas - bugfix")

today = datetime.now().date()
trinta_dias = today - timedelta(days=30)

# Remove the format parameter
data_seletor = st.date_input(
    "Selecione a data",
    (trinta_dias, today)
)

# Handle date range
if isinstance(data_seletor, (list, tuple)) and len(data_seletor) == 2:
    start_date, end_date = data_seletor
else:
    start_date = end_date = data_seletor

query = {
    "billcharge_paidAt": {
        "$gte": start_date,
        "$lte": end_date
    }
}

pegar_dados_button = st.button("Pegar dados")

if pegar_dados_button:

    colunas = ['quote_id', 'billCharge_id', 'customer_id', 'customer_name',
       'store_name', 'quote_status', 'paymentMethod_name', 'billcharge_paidAt',
       'bill_installmentsQuantity', 'bill_amount', 'servicos_json', 'os_id',
       'id_conta_corrente', 'dados_cliente', 'isPaid', 'Tipo de Pagamento',
       'billcharge_dueAt', 'amount']
    
    os_processados = pegar_dados_mongodb("os_processados",query=query)
    
    st.dataframe(os_processados,hide_index=True)