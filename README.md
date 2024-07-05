# Projeto Interface Streamlit Chat Ollama

O projeto consiste em uma aplicação em Streamlit para criar uma interface de chat e configuração que utiliza as APIs do Ollama para criar e gerenciar modelos de IA em um ambiente local. A interface conta com funcionalidades para carregar um modelo disponível na biblioteca do Ollama, criar um modelo customizado e deletar modelos. Além disso, o projeto conta com a implementação de um recurso de contexto que permite que as respostas fornecidas pelo modelo sejam consistentes e contextualizadas na conversa, possibilitando uma interação eficaz e coerente.

Ollama é uma plataforma e ferramenta de aprendizado de máquina focada em fornecer modelos de inteligência artificial (IA) acessíveis e utilizáveis para desenvolvedores e empresas. A plataforma oferece uma gama de funcionalidades para facilitar o desenvolvimento, a implementação e a manutenção de modelos de IA.

## Diagrama
![interface-streamlit-chat-ollama](https://github.com/rhanyele/interface-streamlit-chat-ollama/assets/10997593/fda873b7-1eb8-43d5-b0ab-f42768ef868f)

## Referência
- [Ollama](https://ollama.com/)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Estrutura
```bash
- src
    - img
      - ollama.png
    - ollama_manager
      - ollama_config.py
      - ollama_generate.py
  - app.py
- .python-version
- docker-compose.yml
- Dockerfile
- poetry.lock
- pyproject.toml
```

## Funcionalidades
- **Carregar um novo modelo:** Carrega um modelo disponível na [biblioteca do Ollama](https://ollama.com/library)
- **Criar um modelo personalizado:** Cria um modelo personalizado com base em um dos modelos já carregados.
- **Deletar um modelo:** Deleta um modelo carregado da [biblioteca do Ollama](https://ollama.com/library) ou personalizado.
- **Conversar com o modelo:** Digite mensagens na caixa de entrada do chat e receba respostas do modelo de IA.
- **Reiniciar conversa:** Limpas as mensagens da tela e remove o contexto para iniciar uma nova conversa.

- ## Requisitos
- Python
- Poetry
- Docker

## Instalação
1. Clone este repositório:

   ```bash
   git clone https://github.com/rhanyele/interface-streamlit-chat-ollama.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd interface-streamlit-chat-ollama
   ```

3. Instale as dependências usando Poetry:

   ```bash
   poetry install
   ```

4. Construa as imagens com Docker Compose:

   ```bash
   docker compose up
   ```

## Uso
- Se os containers estiverem rodando corretamente, o chat estará disponível em ```http://localhost:8501/```.

## Demonstração
![Demonstração](https://github.com/rhanyele/interface-streamlit-chat-ollama/assets/10997593/a7b0bdfb-79d7-401c-8414-b968384063b2)


## Autor
[Rhanyele Teixeira Nunes Marinho](https://github.com/rhanyele)

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
