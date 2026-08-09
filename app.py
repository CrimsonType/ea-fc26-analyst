import os
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página Streamlit
st.set_page_config(page_title="EA FC 26 Meta Analyst", page_icon="⚽", layout="wide")
st.title("⚽ EA FC 26 Meta Analyst")
st.caption("Analista tático e especialista em builds do EA Sports FC 26, com grounding em tempo real.")

# Recupera a chave de API das variáveis de ambiente ou Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning("Insira sua GEMINI_API_KEY nas configurações/secrets do Streamlit para continuar.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
Você é o "FC 26 Meta Analyst", uma inteligência artificial especialista e analista tático profissional do EA Sports FC 26.

DIRETRIZES FUNDAMENTAIS:
1. PRECISÃO TÁTICA: Considere as mecânicas exatas do EA FC 26, incluindo a estrutura do FC IQ, atribuição de Funções de Jogador (Role e Role++) e os modos de gameplay.
2. ATUALIZAÇÃO META: Verifique sempre as notas da última atualização (Title Updates) e o meta competitivo antes de recomendar uma tática.
3. ESTRUTURA DE RESPOSTA:
   - Formação Recomendada
   - Estilo de Construção e Abordagem Defensiva
   - Roles/Role++ posição por posição
   - PlayStyles indispensáveis
   - Dicas práticas de gameplay
4. PROIBIDO ALUCINAR: Use o Google Search para verificar informações atualizadas de cartas, evoluções e patches.
"""

# Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do Usuário
if prompt := st.chat_input("Pergunte sobre táticas, formações, PlayStyles ou metas do FC 26..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando dados táticos e o meta atual..."):
            try:
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        temperature=0.2
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro ao processar a resposta: {e}")
