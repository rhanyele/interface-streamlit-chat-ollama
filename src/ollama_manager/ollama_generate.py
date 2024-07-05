import requests
import json
import logging
import pandas as pd
from ollama_manager.ollama_config import *

def ollama_pull_model(model):
    """
    Puxa um modelo específico da API Ollama e retorna o progresso da operação.

    Returns:
    - stream: Um fluxo que fornece o progresso da operação. Em caso de erro, retorna a mensagem de erro.
    """
    try:
        response = requests.post(URL_OLLAMA_PULL,
                                 json={'name': model},
                                 stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            body = json.loads(line)
            total = body.get('total', 1)
            completed = body.get('completed', 0)
            total = int(total)
            completed = int(completed)
            completed_percent = completed / total if total != 0 else 0
            yield completed_percent
            if 'error' in body:
                yield body['error']
                break
        yield True
    except Exception as e:
        logging.error(f"Falha ao puxar modelo '{model}'. Erro: {e}")
        yield str(e)

def ollama_delete_model(model):
    """
    Deleta um modelo específico da API Ollama.

    Returns:
    - bool: True se a operação foi bem-sucedida, False se der erro ou status_code diferente de 200.
    """
    try:
        response = requests.delete(URL_OLLAMA_DELETE, json={"name": model})
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Falha ao deletar modelo '{model}'. Erro: {e}")
        return False
    
def ollama_create_custom_model(model_base, model_name, model_file_content):
    """
    Cria um modelo customizado na API Ollama.

    Returns:
    - bool: True se a operação foi bem-sucedida, False se der erro ou status diferente de success.
    """
    try:
        model_file = f"FROM {model_base}\nSYSTEM {model_file_content}"
        response = requests.post(URL_OLLAMA_CREATE,
                                 json={'name': model_name,
                                       'modelfile': model_file})
        if response.status_code == 200:
            for line in response.iter_lines():
                status = json.loads(line)
                if status.get('status') == "success":
                    return True
        return False
    except Exception as e:
        logging.error(f"Falha ao criar modelo customizado '{model_name}'. Erro: {e}")
        return False

def ollama_generate(model, prompt):
    """
    Gera texto usando um modelo específico da API Ollama a partir de um prompt dado.

    Returns:
    - stream: Um fluxo que fornece partes do texto gerado. Em caso de erro, lança uma exceção com a mensagem de erro.
    """
    try:
        response = requests.post(URL_OLLAMA_GENERATE,
                                 json={'model': model,
                                       'prompt': prompt,
                                       'context': OLLAMA_CONTEXT},
                                 stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            body = json.loads(line)
            response_part = body.get('response', '')
            yield response_part
            if 'error' in body:
                raise Exception(body['error'])
            if body.get('done', False):
                message_context = body['context']
                ollama_add_context(message_context)
    except Exception as e:
        logging.error(f"Falha ao gerar texto usando modelo '{model}'. Erro: {e}")
        raise

def ollama_model_list():
    """
    Lista todos os modelos disponíveis na API Ollama.

    Returns:
    - list: Uma lista de dicionários contendo o nome e o modelo de cada modelo disponível.
    """
    try:
        response = requests.get(URL_OLLAMA_MODELS)
        response.raise_for_status()
        body = response.json()
        models = body.get("models", [])
        return [{"name": model["name"], "model": model["model"]} for model in models]
    except Exception as e:
        logging.error(f"Falha ao listar modelos. Erro: {e}")

def ollama_model_available():
    """
    Retorna um DataFrame Pandas com os modelos disponíveis na configuração OLLAMA_MODEL_AVALIABLE.

    Returns:
    - DataFrame: Um DataFrame Pandas contendo informações sobre os modelos disponíveis.
    """
    try:
        logging.info("Modelos carregados com sucesso.")
        return pd.DataFrame(OLLAMA_MODEL_AVAILABLE)
    except Exception as e:
        logging.error(f"Falha ao carregar os modelos. {e}")

def ollama_add_context(context):
    """
    Adiciona contexto à lista global OLLAMA_CONTEXT.

    Args:
    - list: Lista de contextos a serem adicionados.
    """
    try:
        global OLLAMA_CONTEXT
        OLLAMA_CONTEXT.extend(context)
        logging.info("Contexto global carregado com sucesso.")
    except Exception as e:
        logging.error(f"Falha ao carregar o contexto global. {e}")

def ollama_clear_context():
    """
    Limpa a lista global OLLAMA_CONTEXT.
    """
    try:
        global OLLAMA_CONTEXT
        OLLAMA_CONTEXT.clear()
        logging.info("Contexto global limpo com sucesso.")
    except Exception as e:
        logging.error(f"Falha ao limpar o contexto global. {e}")
