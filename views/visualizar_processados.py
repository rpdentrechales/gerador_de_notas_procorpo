import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *
from datetime import datetime, timedelta,time

st.set_page_config(page_title="OS Processadas", page_icon="💎",layout="wide")

st.title("OS Processadas")

today = datetime.now()
trinta_dias = today - timedelta(days=30)

data_seletor = st.date_input(
    "Selecione a data do pagamento",
    (trinta_dias, today),
    format="DD/MM/YYYY",
)

if len(data_seletor) == 2:
    data_inicial = data_seletor[0]
    data_final = data_seletor[1]
else:
    data_inicial = data_seletor[0]
    data_final = data_inicial

colunas = ['quote_id', 'billCharge_id', 'customer_id', 'customer_name',
       'store_name', 'quote_status', 'paymentMethod_name', 'billcharge_paidAt',
       'bill_installmentsQuantity', 'bill_amount', 'servicos_json', 'os_id',
       'id_conta_corrente', 'dados_cliente', 'isPaid', 'Tipo de Pagamento',
       'billcharge_dueAt', 'amount']
    
os_processados = pegar_dados_mongodb("os_processados")

os_processados['billcharge_paidAt'] = pd.to_datetime(os_processados['billcharge_paidAt'])

os_processados = os_processados.loc[
    (os_processados['billcharge_paidAt'] >= data_inicial) & 
    (os_processados['billcharge_paidAt'] <= data_final)

]st.dataframe(os_processados[colunas],hide_index=True)