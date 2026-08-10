import streamlit as st
import pandas as pd

# Configuração da Página do Streamlit
st.set_page_config(page_title="EA FC 26 Analyst Tool", layout="wide", page_icon="⚽")

st.title("⚽ EA FC 26 Clubs - Analyst Tool")
st.subheader("Central de Inteligência de Atributos e Builds Baseada no Meta")

# Dicionário robusto com a árvore completa de dados do jogo
@st.cache_data
def carregar_matriz_completa():
    return {
        "Aceleração": {"Finisher (ST)": 94, "Spark (Ponta)": 99, "Creator (CAM)": 86, "Recycler (CDM)": 82, "Boss (CB)": 80},
        "Pique (Sprint)": {"Finisher (ST)": 93, "Spark (Ponta)": 98, "Creator (CAM)": 84, "Recycler (CDM)": 83, "Boss (CB)": 85},
        "Posicionamento": {"Finisher (ST)": 99, "Spark (Ponta)": 88, "Creator (CAM)": 90, "Recycler (CDM)": 70, "Boss (CB)": 45},
        "Finalização": {"Finisher (ST)": 98, "Spark (Ponta)": 86, "Creator (CAM)": 82, "Recycler (CDM)": 65, "Boss (CB)": 35},
        "Força do Chute": {"Finisher (ST)": 95, "Spark (Ponta)": 84, "Creator (CAM)": 85, "Recycler (CDM)": 78, "Boss (CB)": 50},
        "Chutes de Longe": {"Finisher (ST)": 90, "Spark (Ponta)": 82, "Creator (CAM)": 88, "Recycler (CDM)": 74, "Boss (CB)": 30},
        "Voleios": {"Finisher (ST)": 92, "Spark (Ponta)": 76, "Creator (CAM)": 78, "Recycler (CDM)": 50, "Boss (CB)": 25},
        "Pênaltis": {"Finisher (ST)": 88, "Spark (Ponta)": 75, "Creator (CAM)": 82, "Recycler (CDM)": 60, "Boss (CB)": 40},
        "Visão de Jogo": {"Finisher (ST)": 82, "Spark (Ponta)": 85, "Creator (CAM)": 96, "Recycler (CDM)": 86, "Boss (CB)": 60},
        "Cruzamento": {"Finisher (ST)": 68, "Spark (Ponta)": 92, "Creator (CAM)": 88, "Recycler (CDM)": 70, "Boss (CB)": 40},
        "Precisão de Faltas": {"Finisher (ST)": 74, "Spark (Ponta)": 78, "Creator (CAM)": 90, "Recycler (CDM)": 65, "Boss (CB)": 30},
        "Passe Curto": {"Finisher (ST)": 85, "Spark (Ponta)": 84, "Creator (CAM)": 97, "Recycler (CDM)": 92, "Boss (CB)": 75},
        "Passe Longo": {"Finisher (ST)": 70, "Spark (Ponta)": 76, "Creator (CAM)": 94, "Recycler (CDM)": 90, "Boss (CB)": 70},
        "Efeito (Curve)": {"Finisher (ST)": 86, "Spark (Ponta)": 88, "Creator (CAM)": 91, "Recycler (CDM)": 72, "Boss (CB)": 35},
        "Agilidade": {"Finisher (ST)": 88, "Spark (Ponta)": 97, "Creator (CAM)": 90, "Recycler (CDM)": 76, "Boss (CB)": 62},
        "Equilíbrio": {"Finisher (ST)": 85, "Spark (Ponta)": 94, "Creator (CAM)": 88, "Recycler (CDM)": 78, "Boss (CB)": 65},
        "Reação": {"Finisher (ST)": 96, "Spark (Ponta)": 88, "Creator (CAM)": 92, "Recycler (CDM)": 90, "Boss (CB)": 88},
        "Controle de Bola": {"Finisher (ST)": 93, "Spark (Ponta)": 92, "Creator (CAM)": 96, "Recycler (CDM)": 85, "Boss (CB)": 70},
        "Drible": {"Finisher (ST)": 91, "Spark (Ponta)": 96, "Creator (CAM)": 93, "Recycler (CDM)": 80, "Boss (CB)": 55},
        "Compostura": {"Finisher (ST)": 95, "Spark (Ponta)": 86, "Creator (CAM)": 93, "Recycler (CDM)": 88, "Boss (CB)": 84},
        "Interceptação": {"Finisher (ST)": 38, "Spark (Ponta)": 42, "Creator (CAM)": 60, "Recycler (CDM)": 94, "Boss (CB)": 92},
        "Precisão do Cabeceio":{"Finisher (ST)": 84, "Spark (Ponta)": 50, "Creator (CAM)": 55, "Recycler (CDM)": 72, "Boss (CB)": 95},
        "Noção Defensiva": {"Finisher (ST)": 28, "Spark (Ponta)": 35, "Creator (CAM)": 52, "Recycler (CDM)": 91, "Boss (CB)": 94},
        "Dividida em Pé": {"Finisher (ST)": 32, "Spark (Ponta)": 38, "Creator (CAM)": 58, "Recycler (CDM)": 93, "Boss (CB)": 95},
        "Carrinho": {"Finisher (ST)": 25, "Spark (Ponta)": 30, "Creator (CAM)": 45, "Recycler (CDM)": 86, "Boss (CB)": 91},
        "Impulsão": {"Finisher (ST)": 85, "Spark (Ponta)": 70, "Creator (CAM)": 68, "Recycler (CDM)": 80, "Boss (CB)": 96},
        "Fôlego (Stamina)": {"Finisher (ST)": 86, "Spark (Ponta)": 90, "Creator (CAM)": 93, "Recycler (CDM)": 96, "Boss (CB)": 85},
        "Força": {"Finisher (ST)": 78, "Spark (Ponta)": 60, "Creator (CAM)": 66, "Recycler (CDM)": 84, "Boss (CB)": 95},
        "Combatividade": {"Finisher (ST)": 65, "Spark (Ponta)": 55, "Creator (CAM)": 70, "Recycler (CDM)": 91, "Boss (CB)": 93},
        "PlayStyle+ Padrão": {"Finisher (ST)": "Finesse / Low Driven", "Spark (Ponta)": "Quick Step / Rapid", "Creator (CAM)": "Incisive Pass / Tiki-Taka", "Recycler (CDM)": "Intercept / Anticipate", "Boss (CB)": "Bruiser / Aerial"},
    }

# Interface
st.sidebar.header("🎛️ Filtros do Analista")
modo_visualizacao = st.sidebar.radio("Selecione o Foco da Análise:", ["Ver Matriz Completa", "Filtrar por Posição Específica"])

dados_brutos = carregar_matriz_completa()
df = pd.DataFrame(dados_brutos)

if modo_visualizacao == "Ver Matriz Completa":
    st.success("Matriz com todos os Atributos Meta carregada com sucesso!")
    
    # Inverte as colunas por linhas para facilitar a leitura por arquétipo
    df_exibicao = df.T
    st.dataframe(df_exibicao, use_container_width=True)
    
    csv = df_exibicao.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Baixar Matriz Completa de Atributos (.CSV)",
        data=csv,
        file_name="matriz_completa_eafc26_clubs.csv",
        mime="text/csv"
    )

else:
    posicoes_disponiveis = list(df.index)
    posicao_selecionada = st.sidebar.selectbox("Selecione a Posição/Arquétipo:", posicoes_disponiveis)
    
    st.subheader(f"📊 Relatório Detalhado: {posicao_selecionada}")
    
    # Isola apenas os dados daquela linha e transforma em tabela vertical
    df_posicao = df.loc[[posicao_selecionada]].T
    df_posicao.columns = ["Valor Base Meta"]
    
    st.dataframe(df_posicao, use_container_width=True)
    
    csv = df_posicao.to_csv().encode('utf-8')
    st.download_button(
        label=f"📥 Baixar Relatório de {posicao_selecionada} (.CSV)",
        data=csv,
        file_name=f"build_{posicao_selecionada.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
