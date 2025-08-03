import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Dashboard de Livros", page_icon="📚", layout="wide")
API_URL = "http://127.0.0.1:8000/api/v1"

def login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        payload = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(
                f"{API_URL}/login",
                data=payload
            )
            if response.status_code == 200:
                token = response.json().get("access_token")
                st.session_state["logged_in"] = True
                st.session_state["token"] = token
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
        except Exception as e:
            st.error(f"Erro ao conectar à API: {e}")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

@st.cache_data(ttl=3600)
def load_data(title="", category=""):
    token = st.session_state.get("token", "")
    try:
        headers = {"Authorization": f"Bearer {token}"}

        params = {"page_size": 1000}
        if title:
            params["title"] = title
        if category:
            params["category"] = category

        response = requests.get(
            f"{API_URL}/books/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_data()

df_results = pd.DataFrame(df["results"].tolist())

if df_results.empty:
    st.warning("Não foram encontrados livros para serem listados.")
    st.stop()

# Create a new column for category names
df_results["category_name"] = df_results["category"].apply(lambda x: x["name"] if isinstance(x, dict) and "name" in x else "")

# Filters
st.sidebar.header("Filtros")

# Check if df_display exists in session state, if not, initialize it
if 'df_display' not in st.session_state:
    st.session_state.df_display = df_results

name_filter = st.sidebar.text_input("Nome do Livro")

# Category filter with a placeholder
placeholder_text = "Todas as Categorias"
categories = sorted(df_results["category_name"].dropna().unique())
options_list = [placeholder_text] + categories
category_filter = st.sidebar.selectbox("Categoria", options=options_list, index=0)
                                       
search = st.sidebar.button("Buscar", key="search_button")

# Ordering options
order_by = st.sidebar.selectbox(
    "Ordenar por",
    options=["Preço crescente", "Preço decrescente", "Avaliação crescente", "Avaliação decrescente"]
)


if search:
    category_to_send = "" if category_filter == placeholder_text else category_filter
    print(f"Buscando livros com título: {name_filter} e categoria: {category_to_send}")
    df_raw_search = load_data(
        title=name_filter,
        category=category_to_send
    )
    if not df_raw_search.empty and "results" in df_raw_search.columns:
        st.session_state.df_display = pd.DataFrame(df_raw_search["results"].tolist())
        st.session_state.df_display["category_name"] = st.session_state.df_display["category"].apply(lambda x: x["name"] if isinstance(x, dict) else "")
    else:
        st.session_state.df_display = pd.DataFrame()

df_to_display = st.session_state.df_display

# Ordering
if order_by == "Preço crescente":
    df_to_display = df_to_display.sort_values(by="price", ascending=True)
elif order_by == "Preço decrescente":
    df_to_display = df_to_display.sort_values(by="price", ascending=False)
elif order_by == "Avaliação crescente":
    df_to_display = df_to_display.sort_values(by="rating", ascending=True)
elif order_by == "Avaliação decrescente":
    df_to_display = df_to_display.sort_values(by="rating", ascending=False)


# Dashboard
st.title("📚 Dashboard de Livros")

# Métricas lado a lado
col1, col2 = st.columns(2)
col1.metric("Total geral de livros", df['total_items'].iloc[0])
col2.metric("Total de livros filtrados", len(df_to_display))

st.markdown("---")

# Graph of categories
if not df_results.empty:
    # 1. Conta a ocorrência de cada categoria
    category_counts = df_results['category_name'].value_counts()

    df_chart = category_counts.reset_index()
    df_chart.columns = ['Categoria', 'Quantidade'] 

    fig = px.bar(
        df_chart,
        x='Categoria',
        y='Quantidade',
        title="Quantidade de Livros por Categoria",
        text='Quantidade',
        color='Categoria',
    )

    fig.update_layout(
        xaxis_title="Categorias", 
        yaxis_title="Número de Livros", 
        showlegend=False 
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum livro para exibir no gráfico.")

st.markdown("---")

# Map rating to stars
rating_dict = {
    "1": "⭐",
    "2": "⭐⭐",
    "3": "⭐⭐⭐",
    "4": "⭐⭐⭐⭐",
    "5": "⭐⭐⭐⭐⭐"
}

# Painel de livros filtrados
st.subheader("Livros Filtrados")
for _, row in df_to_display.iterrows():
    cols = st.columns([1, 6, 2, 2])
    cols[0].image(row["image_url"], width=40)
    cols[1].markdown(f"**{row['title']}**")
    cols[1].markdown(f"£ {row['price']:.2f}")
    if row["availability"]:
        cols[2].markdown('<span style="color:green">Disponível</span>', unsafe_allow_html=True)
    else:
        cols[2].markdown('<span style="color:red">Indisponível</span>', unsafe_allow_html=True)
    cols[3].markdown(rating_dict.get(str(row['rating']), ""))
    st.markdown("---")

