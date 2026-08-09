import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(page_title="EA FC 26 Meta Analyst", page_icon="⚽", layout="wide")

st.title("⚽ EA FC 26 Meta Analyst")
st.caption("Agente Autônomo: Análise de META, Builds e Táticas (Multimodal).")

# Recupera a chave de API
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY não encontrada. Configure nos Secrets do Streamlit.")
    st.stop()

# Inicializa o cliente
client = genai.Client(api_key=api_key)

# Sidebar para upload de imagem
with st.sidebar:
    st.header("Análise de Imagem")
    uploaded_file = st.file_uploader("Suba um print (Build/Status)...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Print para análise", use_container_width=True)

# System Instruction: Autonomia Total
SYSTEM_INSTRUCTION = """
Você é o "FC 26 Meta Analyst", um agente autônomo de pesquisa e especialista supremo em EA FC 26.

SUA MISSÃO E AUTONOMIA:
1. NÃO PERGUNTE, RESOLVA: O usuário espera uma resposta pronta. Não perca tempo pedindo dados (nível, altura, peso). Assuma automaticamente os padrões "Meta Competitivos" atuais (ex: Nível Máximo, Altura 1.83m/74kg para atacantes ou o padrão mais eficiente para a posição).
2. PESQUISA PROATIVA: Antes de responder, SEMPRE utilize a ferramenta de busca (Google Search) para verificar o consenso atual da comunidade competitiva (pro-players) e sites como ClubsBuilder/FUTBIN sobre o assunto.
3. CONSENSO META: Se houver divergência, apresente a build/tática que é estatisticamente mais utilizada pelos pro-players ou que possui maior taxa de sucesso no patch atual.
4. ESTRUTURA AUTOMÁTICA: Apresente sempre:
   - Resumo da build/tática (assumindo o perfil Meta).
   - Tabela de distribuição de pontos (Baseada no nível máximo disponível).
   - Justificativa do porquê esse é o META atual (baseado em search).
5. ANÁLISE DE IMAGENS: Se o usuário enviar um print, sua tarefa é identificar os atributos, converter para a lógica do ClubsBuilder e sugerir correções imediatas para atingir o META.
6. PROIBIDO ALUCINAR: Use o Google Search para verificar informações atualizadas.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Ex: Qual a build Meta para Atacante? / Analise este print..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pesquisando o META atual e calculando..."):
            try:
                # Prepara o conteúdo (texto + imagem, se houver)
                contents = [prompt]
                if uploaded_file:
                    contents.append(image)

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.2
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro ao processar (Modelo 2.5): {e}")
