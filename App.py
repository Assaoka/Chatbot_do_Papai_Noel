import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

import ChainNoel

# Configuração da página
st.set_page_config(page_title="Contato com o Papai Noel", page_icon="🎅")


# Cabeçalho centralizado com toque natalino
with st.container():
    st.markdown('''
        <div style="background-color: #ffffff; padding: 10px; border-radius: 12px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
            <h2 align="center">🎅 Converse com o Papai Noel 🎄</h2>
            <p align="center">Envie sua mensagem e receba respostas especiais do bom velhinho!</p>
        </div><br>
                
    ''', unsafe_allow_html=True)


# Verifica se já existe histórico de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Ho Ho Ho! Como posso ajudar você neste Natal? 🎁")]

# Exibe o histórico de mensagens
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("Papai Noel", avatar="🎅"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Você", avatar="👤"):
            st.write(message.content)

# Cria o encadeamento para a conversa
chain = ChainNoel.create_chain(temperature=0.5)

# Área para interações
with st.container():
    # Botão para contar uma história de Natal
    if st.button("Contar uma história de Natal 🎄"):
        with st.chat_message("Papai Noel", avatar="🎅"):
            resp = st.write_stream(ChainNoel.talk_to_noel(chain, "Me conte uma história de Natal", st.session_state.chat_history))
            st.session_state.chat_history.append(AIMessage(content=resp))
        st.rerun()

    # Botão para limpar a conversa
    if st.button("Limpar conversa 🗑️"):
        st.session_state.chat_history = [AIMessage(content="Ho Ho Ho! Como posso ajudar você neste Natal? 🎁")]
        st.rerun()

# Entrada de mensagem para o usuário
user_input = st.chat_input("Escreva sua mensagem para o Papai Noel aqui: 🎅")
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("Você", avatar="👤"):
        st.write(user_input)
    with st.chat_message("Papai Noel", avatar="🎅"):
        resp = st.write_stream(ChainNoel.talk_to_noel(chain, user_input, st.session_state.chat_history))
        st.session_state.chat_history.append(AIMessage(content=resp))
    st.rerun()

st.html("""
    <style>
        .stApp {
            background-image: url('https://media.istockphoto.com/vectors/no-people-santa-claus-factory-with-gifts-and-decorated-christmas-tree-vector-id1351965430?k=20&m=1351965430&s=612x612&w=0&h=vk8OIiEKZGD8hd7B9RHXmjZZF2xXKY1IEyGQvRmdtUE=');
        }
        body {
            background-color: #f1f1f1;
        }
        .stButton>button {
            background-color: #d9534f;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #c9302c;
        }
        .stChatMessage {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 12px;
        }
        .stChatMessage[data-from="Papai Noel"] {
            background-color: #f1c40f;
            color: #fff;
        }
    </style>""")
