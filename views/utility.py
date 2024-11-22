import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
from auxiliar.auxiliar import *

st.set_page_config(page_title="Utilitários", page_icon="💎",layout="wide")

st.title("Utilitários")

image_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwebmasters.stackexchange.com%2Fquestions%2F5135%2Fwhat-is-the-typical-example-of-old-school-website-design&psig=AOvVaw28mDDSs8vIgghf0wOJdKna&ust=1732375562466000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCJDnq4Sg8IkDFQAAAAAdAAAAABAE"

# Display the image in Streamlit
st.image(image_url, caption="Example of old-school website design")

# df_1,df_2 = atualizar_base_de_clientes()

# st.write(df_1)
# st.write(df_2)
