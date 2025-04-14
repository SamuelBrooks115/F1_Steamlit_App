import streamlit as st

# ✅ This must be the first Streamlit command
st.set_page_config(page_title="Data Editor | F1 Monza", page_icon="🏎️", layout="wide")

import pandas as pd
import sqlite3

# --- Database connection ---
DB_PATH = "data/Structured_Data.db"

def get_tables():
    with sqlite3.connect(DB_PATH) as conn:
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    return tables["name"].tolist()

def load_table(table_name):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(f"SELECT * FROM {table_name}", conn)

def insert_row(table, data_dict):
    with sqlite3.connect(DB_PATH) as conn:
        cols = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        values = list(data_dict.values())
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        conn.execute(query, values)
        conn.commit()

def update_row(table, row_id_col, row_id_val, data_dict):
    with sqlite3.connect(DB_PATH) as conn:
        updates = ', '.join([f"{col} = ?" for col in data_dict])
        values = list(data_dict.values()) + [row_id_val]
        query = f"UPDATE {table} SET {updates} WHERE {row_id_col} = ?"
        conn.execute(query, values)
        conn.commit()

def delete_row(table, row_id_col, row_id_val):
    with sqlite3.connect(DB_PATH) as conn:
        query = f"DELETE FROM {table} WHERE {row_id_col} = ?"
        conn.execute(query, (row_id_val,))
        conn.commit()

# --- Page Header ---
st.markdown("<h1 style='font-size: 40px;'>🛠️ Data Editor</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px;'>View, insert, update, or delete data from the database.</p>", unsafe_allow_html=True)

# --- Select Table ---
st.markdown("<h2 style='font-size: 28px;'>Select a table to manage:</h2>", unsafe_allow_html=True)
table_options = get_tables()
selected_table = st.selectbox("", table_options)

if selected_table:
    df = load_table(selected_table)
    st.dataframe(df)

    # Insert Section
    st.markdown("<h2 style='font-size: 26px;'>➕ Insert New Row</h2>", unsafe_allow_html=True)
    with st.form("insert_form"):
        insert_data = {}
        for col in df.columns:
            st.markdown(f"<label style='font-size:18px;'>{col}</label>", unsafe_allow_html=True)
            insert_data[col] = st.text_input("", key=f"insert_{col}")
        submitted = st.form_submit_button("Insert")
        if submitted:
            insert_row(selected_table, insert_data)
            st.success("Row inserted!")

    # Update Section
    st.markdown("<h2 style='font-size: 26px;'>✏️ Update Existing Row</h2>", unsafe_allow_html=True)
    row_id_col = df.columns[0]  # assumes first column is ID
    st.markdown(f"<label style='font-size:18px;'>Select {row_id_col} to update</label>", unsafe_allow_html=True)
    update_id = st.selectbox("", df[row_id_col], key="update_id")
    with st.form("update_form"):
        update_data = {}
        for col in df.columns[1:]:
            st.markdown(f"<label style='font-size:18px;'>New value for '{col}'</label>", unsafe_allow_html=True)
            update_data[col] = st.text_input("", key=f"update_{col}")
        updated = st.form_submit_button("Update")
        if updated:
            update_row(selected_table, row_id_col, update_id, update_data)
            st.success("Row updated!")

    # Delete Section
    st.markdown("<h2 style='font-size: 26px;'>❌ Delete Row</h2>", unsafe_allow_html=True)
    st.markdown(f"<label style='font-size:18px;'>Select {row_id_col} to delete</label>", unsafe_allow_html=True)
    delete_id = st.selectbox("", df[row_id_col], key="delete")
    if st.button("Delete Row"):
        delete_row(selected_table, row_id_col, delete_id)
        st.success("Row deleted.")
#test 