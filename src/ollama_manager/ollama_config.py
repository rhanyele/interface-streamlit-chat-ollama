"""
Configurações para integração com as APIs do OLLAMA.

Este módulo define as URLs da API, endpoints específicos, e listas de modelos disponíveis mais populares.

Variáveis:
- URL_OLLAMA_API: URL base para a API OLLAMA.
- URL_OLLAMA_PULL, URL_OLLAMA_DELETE, URL_OLLAMA_CREATE, URL_OLLAMA_GENERATE, URL_OLLAMA_MODELS: Endpoints específicos da API OLLAMA.
- OLLAMA_CONTEXT: Lista vazia para armazenar contexto relacionado à conversa com o OLLAMA.
- OLLAMA_MODEL_AVAILABLE: Lista de dicionários contendo modelos OLLAMA disponíveis mais populares com suas especificações.

Exemplo de uso:

>>> from ollama_config import *

# Acessando a URL da API OLLAMA
print(URL_OLLAMA_API)  # Output: http://127.0.0.1:11434/api

# Iterando sobre os modelos disponíveis
for model in OLLAMA_MODEL_AVAILABLE:
    print(f"Modelo: {model['Model']}, Parâmetros: {model['Parameters']}, Tamanho: {model['Size']}")
"""

URL_OLLAMA_API = "http://ollama:11434/api"

URL_OLLAMA_PULL = URL_OLLAMA_API + "/pull"
URL_OLLAMA_DELETE = URL_OLLAMA_API + "/delete"
URL_OLLAMA_CREATE = URL_OLLAMA_API + "/create"
URL_OLLAMA_GENERATE = URL_OLLAMA_API + "/generate"
URL_OLLAMA_MODELS = URL_OLLAMA_API + "/tags"

OLLAMA_CONTEXT = []

OLLAMA_MODEL_AVAILABLE = [
    {"Model": "Llama 3", "Parameters": "8B", "Size": "4.7GB", "Download": "llama3"},
    {"Model": "Llama 3", "Parameters": "70B", "Size": "40GB", "Download": "llama3:70b"},
    {"Model": "Phi 3 Mini", "Parameters": "3.8B", "Size": "2.3GB", "Download": "phi3"},
    {"Model": "Phi 3 Medium", "Parameters": "14B", "Size": "7.9GB", "Download": "phi3:medium"},
    {"Model": "Gemma 2", "Parameters": "9B", "Size": "5.5GB", "Download": "gemma2"},
    {"Model": "Gemma 2", "Parameters": "27B", "Size": "16GB", "Download": "gemma2:27b"},
    {"Model": "Mistral", "Parameters": "7B", "Size": "4.1GB", "Download": "mistral"},
    {"Model": "Moondream 2", "Parameters": "1.4B", "Size": "829MB", "Download": "moondream"},
    {"Model": "Neural Chat", "Parameters": "7B", "Size": "4.1GB", "Download": "neural-chat"},
    {"Model": "Starling", "Parameters": "7B", "Size": "4.1GB", "Download": "starling-lm"},
    {"Model": "Code Llama", "Parameters": "7B", "Size": "3.8GB", "Download": "codellama"},
    {"Model": "Llama 2 Uncensored", "Parameters": "7B", "Size": "3.8GB", "Download": "llama2-uncensored"},
    {"Model": "LLaVA", "Parameters": "7B", "Size": "4.5GB", "Download": "llava"},
    {"Model": "Solar", "Parameters": "10.7B", "Size": "6.1GB", "Download": "solar"},
]
