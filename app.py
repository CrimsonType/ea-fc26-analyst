import streamlit as st
import subprocess
import os
import sys
import pandas as pd

st.set_page_config(page_title="EA FC 26 Analyst - Testes", layout="wide")
st.title("⚽ EA FC 26 - Pro Clubs Analyst Tool (Painel de Testes)")

# Sidebar de Administração
st.sidebar.header("⚙️ Painel de Testes / ETL")

# Botão principal de disparo
if st.sidebar.button("🚀 Executar Raspagem em Tempo Real"):
    log_container = st.expander("📄 Logs de Execução do Robô", expanded=True)
    
    with st.spinner("Conectando ao ClubsBuilder e coletando dados..."):
        try:
            processo = subprocess.run(
                [sys.executable, "extract_clubsbuilder.py"],
                capture_output=True,
                text=True
            )
            
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

# Exibição dos dados
st.subheader("📊 Visualização dos Dados Carregados")
if os.path.exists("data/attributes_lvl1.csv"):
    df_test = pd.read_csv("data/attributes_lvl1.csv")
    st.dataframe(df_test, use_container_width=True)
else:
    st.info("Nenhum dado capturado ainda. Clique no botão na barra lateral para testar a extração.")
