import streamlit as st
import subprocess
import os
import sys
import pandas as pd

st.set_page_config(page_title="EA FC 26 Analyst - Testes", layout="wide")

st.title("⚽ EA FC 26 - Pro Clubs Analyst Tool (Painel de Testes)")

# Configuração de ambiente para rodar o Playwright no Streamlit Cloud
@st.cache_resource
def setup_playwright():
    try:
        # Garante a instalação do navegador no contêiner da nuvem
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Erro ao inicializar navegadores: {e}")

setup_playwright()

# Sidebar de Administração
st.sidebar.header("⚙️ Painel de Testes / ETL")

# Botão principal de disparo
if st.sidebar.button("🚀 Executar Raspagem em Tempo Real"):
    log_container = st.expander("📄 Logs de Execução do Robô", expanded=True)
    
    with st.spinner("Abrindo navegador e conectando ao ClubsBuilder..."):
        try:
            # Roda o script de extração e captura os logs de saída
            processo = subprocess.run(
                [sys.executable, "extract_clubsbuilder.py"],
                capture_output=True,
                text=True
            )
            
            # Exibe os logs na tela em tempo real
            if processo.stdout:
                log_container.text("LOGS DE SAÍDA:\n" + processo.stdout)
            if processo.stderr:
                log_container.error("ERROS / AVISOS:\n" + processo.stderr)
                
            if processo.returncode == 0:
                st.success("✅ Extração concluída com sucesso!")
                st.balloons()
            else:
                st.error("❌ Falha na extração. Veja os logs acima.")
                
        except Exception as e:
            st.error(f"Erro ao disparar o processo: {str(e)}")

st.divider()

# Exibição dos dados capturados
st.subheader("📊 Visualização dos Dados Carregados")

if os.path.exists("data/attributes_lvl1.csv"):
    df_test = pd.read_csv("data/attributes_lvl1.csv")
    st.dataframe(df_test, use_container_width=True)
else:
    st.info("Nenhum dado capturado ainda. Clique no botão na barra lateral para testar a extração.")
