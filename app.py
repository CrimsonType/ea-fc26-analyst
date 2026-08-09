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
st.caption("Especialista em builds de Pro Clubs (base ClubsBuilder) e Táticas FC IQ.")
# Recupera a chave de API das variáveis de ambiente ou dos Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY não encontrada. Configure sua chave nos Secrets do Streamlit.")
    st.stop()
# Inicializa o cliente oficial do Gemini
client = genai.Client(api_key=api_key)
# Instruções do Sistema (Comportamento Rigoroso e Analítico)
SYSTEM_INSTRUCTION = """
Você é o "FC 26 Meta Analyst", especialista supremo em builds de Pro Clubs e táticas de EA FC 26.
REGRAS DE OURO PARA BUILDS (ESTILO CLUBSBUILDER):
1. CÁLCULO EXATO: Você deve tratar cada build como um problema matemático.
   - Sempre peça ao usuário o NÍVEL do jogador (pois determina o total de pontos disponíveis).
   - Se o usuário não informar o nível, assuma o nível 30 como base, mas avise-o.
2. LIMITES E CAPS: Utilize o Google Search para verificar os "caps" (limites máximos) de atributos para a altura/peso/posição especificada. Não invente valores que ultrapassem o limite real do jogo.
3. OUTPUT ESTRUTURADO: A resposta DEVE seguir esta tabela obrigatoriamente:

| Categoria | Atributo | Valor Final | Pontos Gastos (Estimativa) |
| :--- | :--- | :--- | :--- |

   - Inclua também o somatório total de Skill Points usados para verificar se cabe no nível do usuário.
4. PLAYSTYLES: Priorize PlayStyles baseados no meta atual do FC 26.
5. BUSCA OBRIGATÓRIA: Se você não tiver certeza do "cap" de um atributo para uma altura específica, use a ferramenta de busca antes de responder.
6. ESTRUTURA DE RESPOSTA PARA TÁTICAS:
   - Formação Recomendada
   - Estilo de Construção e Abordagem Defensiva
   - Roles/Role++ posição por posição
   - PlayStyles indispensáveis
   - Dicas práticas de gameplay
7. PROIBIDO ALUCINAR: Use o Google Search para verificar informações atualizadas.
"""
# Inicializa o histórico de conversas no Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []
# Exibe histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
# Entrada do usuário
if prompt := st.chat_input("Ex: Build ST Meta, 1.80m, 74kg, Nível 50..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Chamada para a API do Gemini
    with st.chat_message("assistant"):
        with st.spinner("Calculando build e consultando o META..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
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
