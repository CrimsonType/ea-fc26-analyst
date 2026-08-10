import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="EA FC 26 Pro Clubs Analyst",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ EA FC 26 - Pro Clubs Analyst Tool")
st.markdown("Base de dados unificada de atributos, matrizes de nível e projeções para IAs.")

# Função com cache do Streamlit para alta performance
@st.cache_data
def load_data():
    lvl1_path = "data/attributes_lvl1.csv"
    meta_path = "data/attributes_meta.csv"
    
    # Fallback se os arquivos CSV processados ainda não existirem
    if os.path.exists(lvl1_path) and os.path.exists(meta_path):
        df_lvl1 = pd.read_csv(lvl1_path)
        df_meta = pd.read_csv(meta_path)
    else:
        # Exemplo de estrutura padrão caso esteja em inicialização
        df_lvl1 = pd.DataFrame({
            "Posição": ["Atacante (FWD)", "Meio-Campo (MID)", "Defensor (DEF)"],
            "Ritmo Base": [75, 70, 68],
            "Finalização Base": [78, 65, 45],
            "Passe Base": [65, 75, 60],
            "Drible Base": [72, 74, 55],
            "Defesa Base": [35, 55, 75],
            "Físico Base": [60, 65, 78]
        })
        df_meta = df_lvl1.copy()
        
    return df_lvl1, df_meta

df_lvl1, df_meta = load_data()

# Menu Lateral (Sidebar)
st.sidebar.header("Navegação & Filtros")
visao = st.sidebar.radio(
    "Selecione a Visão de Dados:",
    ["1. Atributos Iniciais (Nível 1)", "2. Planejamento Meta (Fim de Jogo)", "3. Exportar para IA"]
)

if visao == "1. Atributos Iniciais (Nível 1)":
    st.subheader("📊 Matriz de Atributos Base - Nível 1")
    st.dataframe(df_lvl1, use_container_width=True)
    
    st.download_button(
        label="📥 Baixar Atributos Nível 1 (.CSV)",
        data=df_lvl1.to_csv(index=False).encode('utf-8'),
        file_name="eafc26_attributes_lvl1.csv",
        mime="text/csv"
    )

elif visao == "2. Planejamento Meta (Fim de Jogo)":
    st.subheader("🎯 Teto Recomendado - Nível Máximo")
    st.dataframe(df_meta, use_container_width=True)
    
    st.download_button(
        label="📥 Baixar Base Meta (.CSV)",
        data=df_meta.to_csv(index=False).encode('utf-8'),
        file_name="eafc26_attributes_meta.csv",
        mime="text/csv"
    )

elif visao == "3. Exportar para IA":
    st.subheader("🤖 Exportação de Prompt & Dados para IAs")
    st.write("Copie o texto estruturado abaixo ou baixe a base completa para usar em modelos de linguagem (GPT-4, Claude, Gemini).")
    
    json_export = {
        "nivel_1": df_lvl1.to_dict(orient="records"),
        "meta": df_meta.to_dict(orient="records")
    }
    
    st.text_area("JSON de Atributos:", value=json.dumps(json_export, indent=2, ensure_ascii=False), height=300)
