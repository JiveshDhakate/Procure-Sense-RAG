import streamlit as st
from datetime import datetime

# ------------------- Page Setup -------------------
st.set_page_config(
    page_title="🏠 Home | Procure-Sense-RAG",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Header -------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            color: #1F618D;
            font-weight: 800;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #4E5D6C;
            margin-top: -10px;
            margin-bottom: 25px;
        }
        .footer {
            text-align: center;
            color: gray;
            font-size: 0.8rem;
            margin-top: 50px;
        }
        div[data-testid="stMarkdownContainer"] ul{
            padding-left:2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">⚙️ Procure Sense RAG: Multi-Agent System for Supplier Quotation Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Empowering procurement intelligence through Retrieval-Augmented Generation and Multi-Agent reasoning.</p>', unsafe_allow_html=True)

# ------------------- Content -------------------
st.markdown("### 🧠 What is this?")
st.info(
    """
    **Procure Sense RAG** combines four specialized AI agents —  
    🧩 **Extractor**, 🧮 **Retriever**, ⚖️ **Evaluator**, and 📝 **Summarizer** —  
    to analyze supplier quotations, compare offers, and recommend the best choice with transparent reasoning.
    """
)

st.markdown("### 🚀 Get Started")
col1, col2 = st.columns(2)

with col1:
    st.success("📤 **Upload Page** — Add supplier quotations.")
    st.markdown("Paste supplier offer text here. The Extractor Agent structures it and stores embeddings in ChromaDB.")

with col2:
    st.warning("🔍 **Query Page** — Search and evaluate offers.")
    st.markdown("Ask natural language questions to compare suppliers. The Evaluator and Summarizer Agents explain the best recommendation.")

# ------------------- Optional Image or Banner -------------------
st.markdown("---")
st.image(
    "https://cdn-icons-png.flaticon.com/512/2920/2920244.png",
    caption="AI-powered Supplier Intelligence",
    width=200
)

# ------------------- Footer -------------------
st.markdown(
    f"""
    <p class="footer">
        © {datetime.now().year} Developed by <b>Jivesh Dhakate</b> 🧑‍💻
    </p>
    """,
    unsafe_allow_html=True
)
