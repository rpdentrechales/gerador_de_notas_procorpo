
def load_main_dataframe(worksheet):

  conn = st.connection("gsheets", type=GSheetsConnection)
  df = conn.read(worksheet=worksheet,dtype={"Ad ID": str})

  return df

def load_aux_dataframe(worksheet,duplicates_subset):

  conn = st.connection("gsheets", type=GSheetsConnection)
  df = conn.read(worksheet=worksheet)
  df = df.drop_duplicates(subset=duplicates_subset)

  return df
