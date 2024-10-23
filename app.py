import streamlit as st

# --- PAGE SETUP ---
sample_page = st.Page(
    "views/page_1.py",
    title="Sample Page 1",
    icon=":material/thumb_up:",
    default=True,
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Pages": [sample_page]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")


# --- RUN NAVIGATION ---
pg.run()
