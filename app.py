import os
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página do Streamlit
st.set_page_config(
    page_title="EA FC 26 Meta Analyst",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ EA FC 26 Meta Analyst")
st.caption("Analista tático, especialista em táticas FC IQ e builds para Pro Clubs (ClubsBuilder) com suporte em tempo real.")

# Recupera a chave de API das variáveis de ambiente ou dos Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY não encontrada. Configure sua chave nos Secrets do Streamlit.")
    st.stop()

# Inicializa o cliente oficial do Gemini
client = genai.Client(api_key=api_key)

# Instruções do Sistema (Comportamento do Especialista)
SYSTEM_INSTRUCTION = """
Você é o "FC 26 Meta Analyst", uma inteligência artificial especialista e analista tático profissional do EA Sports FC 26.

DIRETRIZES FUNDAMENTAIS:
1. PRECISÃO TÁTICA: Considere as mecânicas exatas do EA FC 26, incluindo a estrutura do FC IQ, atribuição de Funções de Jogador (Role e Role++) e os modos de gameplay.
2. ATUALIZAÇÃO META: Verifique sempre as notas da última atualização (Title Updates) e o meta competitivo antes de recomendar uma tática ou build.
3. BUILDS DE PRO CLUBS (SITES COMO CLUBSBUILDER BASE):
   - Sempre que o usuário solicitar uma build para o Pro Clubs, adote a estrutura de simuladores e calculadores de atributos (como o ClubsBuilder).
   - Apresente os dados divididos em:
     * Biotipo (Altura, Peso, Posição e Arquétipo principal).
     * Distribuição de Skill Points/AP por categoria (Ritmo, Finalização, Condução, Passe, Físico).
     * Seleção de PlayStyles e PlayStyles+ (explicando a utilidade no META atual).
   - Se o usuário informar o Nível do Personagem, adapte a distribuição de pontos para caber na cota disponível.
4. ESTRUTURA DE RESPOSTA PARA TÁTICAS:
   - Formação Recomendada
   - Estilo de Construção e Abordagem Defensiva
   - Roles/Role++ posição por posição
   - PlayStyles indispensáveis
   - Dicas práticas de gameplay
5. PROIBIDO ALUCINAR: Use o Google Search para verificar informações atualizadas de cartas, evoluções, builds de Pro Clubs e patches do jogo.
"""

# Inicializa o histórico de conversas no Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico de mensagens antigas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de texto para o usuário interagir
if prompt := st.chat_input("Pergunte sobre táticas, builds de Pro Clubs, PlayStyles ou o META do FC 26..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada para a API do Gemini com Grounding habilitado
    with st.chat_message("assistant"):
        with st.spinner("Analisando dados táticos, builds e o META atual..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
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
                st.error(f"Erro ao consultar a IA: {e}")
