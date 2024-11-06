import streamlit as st

# --- PAGE SETUP ---
subir_notas_page = st.Page(
    "views/subir_notas.py",
    title="Subir Notas",
    icon=":material/cloud_upload:",
    default=True,
)
log_page = st.Page(
    "views/log.py",
    title="Logs",
    icon=":material/summarize:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Notas Omie": [subir_notas_page,log_page]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()
