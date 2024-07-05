import re
import logging
import streamlit as st
from ollama_manager.ollama_generate import *

logging.basicConfig(level=logging.INFO)

# Obtém a lista de modelos disponíveis na inicialização do aplicativo
model_list = ollama_model_list()

def more_info_model():
    """
    Exibe mais informações e modelos disponíveis em um link externo.
    """
    st.caption(f"Mais informações e modelos disponíveis em: https://ollama.com/library")

def validate_custom_model_name(model_custom_name):
    """
    Valida se o nome de um modelo personalizado contém apenas letras e números.

    Args:
        model_custom_name (str): Nome do modelo personalizado.

    Returns:
        bool: True se o nome for válido, False se conter algum caractere especial.
    """
    padrao = r"[^a-zA-Z0-9]"
    if re.search(padrao, model_custom_name):
        return True
    else:
        return False

@st.experimental_dialog("Carregando modelo:", width="large")
def dialog_pull_model(model):
    """
    Configura uma caixa de diálogo para carregar um modelo disponível na Ollama e exibir o progresso.

    Args:
        model (str): Nome do modelo a ser carregado.
    """
    with st.container():
        progress_bar = st.progress(0)
        status_text = st.empty()
        try:
            for loading in ollama_pull_model(model):
                if isinstance(loading, float):
                    progress_bar.progress(loading)
                    status_text.markdown(f"Configurando modelo: **{model}**\n\nProgresso: {loading:.2%}")
                elif loading is True:
                    progress_bar.progress(1.0)
                    status_text.markdown(f"**Carregado com sucesso.**")
                else:
                    status_text.markdown("")
                    st.error(f"Modelo: **{model}**.\n\n**Erro:** {loading}")
                    more_info_model()
                    break
        except requests.exceptions.RequestException as e:
            st.error(f"Erro de conexão: {e}")
            more_info_model()

    if st.button("Confirmar", key="model_pull_confirm"):
        st.rerun()

@st.experimental_dialog("Deletando modelo:", width="large")
def dialog_delete_model(model):
    """
    Configura uma caixa de diálogo para deletar um modelo já carregado no aplicativo.

    Args:
        model (str): Nome do modelo a ser deletado.
    """
    with st.container():
        try:
            deleted = ollama_delete_model(model)
            if deleted:
                st.error(f"Modelo: **{model}** \n\n**Deletado com sucesso.**")
            else:
                st.error(f"Modelo: **{model}** \n\n**Erro ao deletar.**")
                more_info_model()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro de conexão: {e}")
            more_info_model()

    if st.button("Confirmar", key="model_delete_confirm"):
        st.rerun()

@st.experimental_dialog("Criando modelo personalizado:", width="large")
def dialog_create_custom_model(model_base, model_name, model_file_content):
    """
    Configura uma caixa de diálogo para criar um modelo personalizado.

    Args:
        model_base (str): Modelo base para a criação do modelo personalizado.
        model_name (str): Nome do modelo personalizado.
        model_file_content (str): Conteúdo de como o modelo deve atuar.
    """
    with st.container():
        try:
            created = ollama_create_custom_model(model_base, model_name, model_file_content)
            if created:
                st.success(f"Modelo: **{model_name}**\n\nAtuação: **{model_file_content}**\n\n**Criado com sucesso.**")
            else:
                st.error(f"Erro ao criar o modelo: **{model_name}**")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro de conexão: {e}")

    if st.button("Confirmar", key="model_custom_confirm"):
        st.rerun()

def button_pull_model():
    """
    Configura um botão e campo de entrada para puxar um modelo da API Ollama.
    """
    model = st.text_input("Nome do modelo", key="model_create", placeholder="ex: phi3")
    if st.button("Carregar modelo"):
        if model:
            dialog_pull_model(model)
        else:
            st.warning("Por favor, digite o nome do modelo.")

def button_custom_model():
    """
    Configura opções para selecionar um modelo base e criar um modelo personalizado.
    """
    model_base = st.selectbox('**Selecione um modelo base**',options= (model_list.get('name') for model_list in model_list), key="model_list_custom")
    model_custom_name = st.text_input("Nome do modelo", key="model_custom_name", placeholder="ex: meuModelo")
    model_custom_command = st.text_area("Como o modelo deve atuar", key="model_custom_command", placeholder="ex: você é o mario do super mario")
    if st.button("Customizar modelo"):
        if model_custom_name:
            if not validate_custom_model_name(model_custom_name):
                if model_custom_command:
                    dialog_create_custom_model(model_base, model_custom_name, model_custom_command)
                else:
                    st.warning("Por favor, digite como o modelo deve atuar.")
            else:
                st.warning("Por favor, digite um nome do modelo valido apenas letras e números.")       
        else:
            st.warning("Por favor, digite o nome do modelo.")

def button_delete_model():
    """
    Configura opções para selecionar e deletar um modelo da API Ollama.
    """
    option = st.selectbox('**Modelo selecionado**',options= (model_list.get('name') for model_list in model_list), key="model_list_delete")
    validate_model = st.text_input("Confirme digitando o nome do modelo", key="validate_model", placeholder="ex: phi3")
    if st.button("Deletar modelo"):
        if option == validate_model:
            dialog_delete_model(option)
        else:
            st.warning("Por favor, confirme o nome do modelo que deseja deletar.")

def show_model():
    """
    Exibe uma tabela com os modelos disponíveis.
    """
    model_avaliabre = ollama_model_available()
    st.subheader("Modelos mais populares:")      
    st.table(model_avaliabre)
    more_info_model()

def app_config_model():
    """
    Configura a tela inicial para configurar o primeiro modelo.
    """
    st.header("Vamos configurar o seu primeiro modelo para o uso:")
    col1, col2 = st.columns(2)   
    with col1:
        show_model()
    with col2:
        button_pull_model()
            
# Reinicia a conversa
def reset_conversation():
    """
    Limpa o histórico de conversa e o contexto global.
    """
    st.session_state.messages = []
    ollama_clear_context()

def menu_sidebar(model_list):
    """
    Configura o menu lateral com opções para gerenciar modelos.

    Args:
        models (list): Lista de modelos disponíveis.
    """
    with st.sidebar:
        st.header("Modelo:")
        option = st.selectbox('**Modelo selecionado**',options= (model_list.get('name') for model_list in model_list), key="model_list")
        st.button("Reiniciar conversa", on_click=reset_conversation)
        with st.container(border=True):
            st.header("Gerenciamento:")
            with st.expander("Carregar um novo modelo"):
                button_pull_model()
            with st.expander("Criar um modelo personalizado:"):
                button_custom_model()
            with st.expander("Deletar um modelo:"):
                button_delete_model()
        more_info_model()      
    return option

# tela principal do chat
def app_chat(models):
    """
    Configura a tela principal do chat com interações entre usuário e assistente.

    Args:
        models (list): Lista de modelos disponíveis.
    """
    option = menu_sidebar(models)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        if message["role"] == 'assistant':
            with st.chat_message(message["role"], avatar="src/img/ollama.png"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    if prompt := st.chat_input("Escreva sua mensagem:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="src/img/ollama.png"):
            ollama = ollama_generate(option, prompt)
            response_content = st.write_stream(ollama)  
        st.session_state.messages.append({"role": "assistant", "content": response_content})

def check_model_available(models):
    """
    Verifica se há modelos disponíveis, caso não tenha, configura o primeiro modelo. Se houver modelos disponíveis, carrega a tela de chat.

    Args:
        models (list): Lista de modelos disponíveis.
    """
    if models == []:
        app_config_model()
    else:
        app_chat(models)
        
def main():
    """
    Configurações principais do aplicativo.
    """
    st.set_page_config(page_title="Simple Interface Chat Ollama", page_icon="src/img/ollama.png", layout="wide")
    st.title("Simple Interface Chat Ollama")
    check_model_available(model_list)

if __name__ == "__main__":
    main()