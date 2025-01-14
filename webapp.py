import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    dados = pd.read_csv("compras.csv")
except:
    dados = pd.DataFrame({"PRODUTO": [], "PRECO": []})
    dados.to_csv("compras.csv", index=False)

# Title of the app
st.title("Controle de Gastos")

# Budget input
orcamento = st.number_input("Orçamento:", min_value=0.0, step=0.01)

# Calculate total spent
total = dados["PRECO"].sum() if not dados.empty else 0

# Form for new purchase
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0, step=0.01)
    
    submit_button = st.form_submit_button("Adicionar")
    
    if submit_button:
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"PRODUTO": [produto], "PRECO": [preco]})
            dados = pd.concat([dados, nova_linha])
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

# Budget visualization
if orcamento > 0:
    # Create Donut Chart
    fig, ax = plt.subplots(figsize=(8, 8))
    
    if not dados.empty:
        produtos = dados["PRODUTO"].tolist()
        valores = dados["PRECO"].tolist()
        restante = orcamento - total
        
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        
        ax.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        ax.set_title(f"Orçamento: {orcamento}€")
        
        # Create circular hole for the donut chart
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)
        
        st.pyplot(fig)

# Display the data and the total amounts
st.dataframe(dados)
st.write(f"Total gasto: {total}€")
st.write(f"Restante: {orcamento - total}€")
