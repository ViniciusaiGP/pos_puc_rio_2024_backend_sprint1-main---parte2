# API de Gerenciamento de Estoque com JWT e Flask

Este projeto é uma API RESTful para gerenciar usuários, produtos e notas fiscais, com autenticação baseada em tokens JWT. A API foi construída utilizando **Flask**, **Flask-RESTful**, **Flask-JWT-Extended**, e **Flask-OpenAPI**. Ela também oferece um sistema de segurança que envolve autenticação, autorização e manipulação de dados.

#### Descrição Geral

O sistema foi desenvolvido para gerenciar produtos de estoque, permitindo:

- Cadastro, edição, exclusão e listagem de produtos.
- Listagem e gerenciamento de usuários, incluindo login e registro.
- Busca de informações de notas fiscais eletrônicas a partir de uma URL externa.
- Integração dos dados de produtos nas operações de estoque.

#### Funcionalidades Principais

1. **Autenticação JWT**: Geração e verificação de tokens JWT para acesso seguro às rotas protegidas.
2. **Gerenciamento de Usuários**: Registro, login, listagem e logout.
3. **Gerenciamento de Produtos**: Listagem, criação, edição e remoção de produtos.
4. **Integração com Notas Fiscais Eletrônicas**: Busca de informações de produtos através de uma URL de nota fiscal.
5. **Proteção de Rotas**: As rotas que manipulam dados sensíveis estão protegidas por JWT, garantindo a segurança do sistema.

---

## Requisitos

Primeiro vamos criar um ambiente virtual para fazer a instalação das bibliotecas.

Windows:
`python -m venv venv`
No macOS e Linux:
`python3 -m venv venv`

Após executar o comando, uma nova pasta com o nome do ambiente virtual será criada no diretório atual.
Ative o ambiente virtual. Isso é feito executando um script específico dependendo do seu sistema operacional.

Windows:
`venv\Scripts\activate`
No macOS e Linux:
`source venv/bin/activate`

Ao fazer isso, você notará que o prompt do terminal será prefixado com o nome do seu ambiente virtual, indicando que está ativo.

Certifique-se de ter o Python instalado em sua máquina. Você pode instalar as dependências do projeto executando:

`pip install -r requirements.txt`

## Configuração

O projeto utiliza um banco de dados SQLite, então não há necessidade de configurações adicionais. Porém, para uso em produção, recomenda-se alterar para um banco de dados mais robusto, como PostgreSQL ou MySQL.

---

## Funcionalidades


### Configuração do CORS

No seu projeto, o CORS (Cross-Origin Resource Sharing) foi habilitado para controlar quais origens podem fazer requisições para os recursos da API, garantindo maior segurança na comunicação com o frontend.

#### 1. `CORS(app, resources={...})`
   
- Habilita o CORS no aplicativo Flask, permitindo controlar de forma explícita as origens autorizadas a acessar os recursos da API.

#### 2. `r"/api/*"`

- A configuração é aplicada a qualquer rota que comece com `/api/`. Isso significa que todas as rotas da API, como as que gerenciam produtos e usuários, estão cobertas por essa política de CORS.

#### 3. `"origins": "http://127.0.0.1:5000"`

- Apenas a origem `http://127.0.0.1:5000`, geralmente associada ao frontend rodando localmente (localhost), está autorizada a fazer requisições para a API.
- Qualquer tentativa de acesso à API a partir de outras origens será bloqueada, garantindo que somente o frontend autorizado possa interagir com o backend.

Essa configuração é essencial para garantir que somente o ambiente de desenvolvimento autorizado tenha acesso à API, prevenindo requisições não autorizadas de outras origens, aumentando assim a segurança da aplicação.

---

Este é o trecho de código relevante do CORS na API:

```python
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
```

Essa implementação controla o acesso às rotas de forma restrita e segura, permitindo que a aplicação funcione conforme esperado em ambientes controlados (como durante o desenvolvimento local).

---

## Endpoints

### 1. **Home**
- **Rota:** `/`
- **Método:** `GET`
- **Descrição:** Redireciona para a documentação Swagger da API.
- **Resposta:**
  - `302`: Redireciona para `/openapi/swagger`

---

### 2. **Listar Produtos**
- **Rota:** `/api/produtos`
- **Método:** `GET`
- **Descrição:** Retorna a lista de todos os produtos cadastrados. Esta rota está protegida por JWT.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Respostas:**
  - `200`: Retorna a lista de produtos.
  - `400`: Erro de requisição.
  - `401`: Acesso não autorizado.
  - `500`: Erro interno no servidor.

---

### 3. **Cadastrar Produto**
- **Rota:** `/api/registrar`
- **Método:** `POST`
- **Descrição:** Cria um novo produto no sistema. Esta rota está protegida por JWT.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Corpo da Requisição:**
  - `nome` (string) - Nome do produto.
  - `descricao` (string) - Descrição do produto.
  - `preco` (float) - Preço do produto.
  - `quantidade` (int) - Quantidade em estoque.
- **Respostas:**
  - `201`: Produto criado com sucesso.
  - `400`: Erro de validação de dados.
  - `500`: Erro interno no servidor.

---

### 4. **Atualizar Produto**
- **Rota:** `/api/produto/<int:id>`
- **Método:** `PUT`
- **Descrição:** Atualiza as informações de um produto existente. Esta rota está protegida por JWT.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Parâmetros da Rota:**
  - `id` (int) - ID do produto.
- **Corpo da Requisição:**
  - `nome` (string) - Nome do produto (opcional).
  - `descricao` (string) - Descrição do produto (opcional).
  - `preco` (float) - Preço do produto (opcional).
  - `quantidade` (int) - Quantidade em estoque (opcional).
- **Respostas:**
  - `200`: Produto atualizado com sucesso.
  - `400`: Erro de validação de dados.
  - `404`: Produto não encontrado.
  - `500`: Erro interno no servidor.

---

### 5. **Deletar Produto**
- **Rota:** `/api/produto/<int:id>`
- **Método:** `DELETE`
- **Descrição:** Remove um produto do sistema pelo seu ID. Esta rota está protegida por JWT.
- **Autenticação:** Token JWT obrigatório.
- **Segurança:** `Bearer Token`
- **Parâmetros da Rota:**
  - `id` (int) - ID do produto.
- **Respostas:**
  - `200`: Produto removido com sucesso.
  - `404`: Produto não encontrado.
  - `500`: Erro interno no servidor.

---

## Erros Comuns

- `400` - Erro de Requisição: Quando os dados fornecidos na requisição são inválidos ou incompletos.
- `401` - Não Autorizado: Quando o token JWT está ausente ou inválido.
- `404` - Não Encontrado: Quando o recurso solicitado não existe.
- `500` - Erro Interno do Servidor: Problemas ao processar a requisição no servidor.

---

## Executando o projeto

Para iniciar o servidor de desenvolvimento, execute:

```
python app.py
```

O servidor será iniciado em `http://localhost:5002`.

---

# Docker

Exemplo genérico.

#### 1. **Instalação do Docker**

**Para Windows e Mac:**
- **Baixe e instale o Docker Desktop**:
  - Acesse o [site do Docker Desktop](https://www.docker.com/products/docker-desktop) e baixe o instalador apropriado para seu sistema operacional.
  - Siga as instruções do instalador. Durante a instalação, pode ser necessário habilitar o WSL 2 (para Windows).

**Para Linux:**
- **Instalação do Docker**:
  - Abra um terminal e execute os seguintes comandos para instalar o Docker:
    ```bash
    sudo apt-get update
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce
    ```

- **Iniciar o serviço Docker**:
    ```bash
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

- **Verificar se o Docker está rodando**:
    ```bash
    sudo docker run hello-world
    ```

#### 2. **Criar a Estrutura do Projeto**

Agora que o Docker está instalado, você precisa criar a estrutura de pastas para sua aplicação Flask. Execute os seguintes comandos no terminal:

```bash
mkdir minha-app-flask
cd minha-app-flask
touch app.py requirements.txt Dockerfile docker-compose.yml
```

### 3. **Escrever o Código da Aplicação**

Abra o arquivo `app.py` e adicione o seguinte código básico para a aplicação Flask:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Olá, Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 4. **Criar o arquivo requirements.txt**

No arquivo `requirements.txt`, adicione a seguinte linha para instalar o Flask:

```
Flask==2.0.3
```

### 5. **Criar o Dockerfile**

No arquivo `Dockerfile`, cole o seguinte código:

```dockerfile
# Usa a imagem base do Python
FROM python:3.9.10-slim-buster

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho no container
COPY requirements.txt ./

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do projeto para o diretório de trabalho
COPY . .

# Define o comando para rodar a aplicação
CMD ["python", "app.py"]
```

### 6. **Criar o docker-compose.yml**

No arquivo `docker-compose.yml`, cole o seguinte código:

```yaml
version: '3.5'

services:
  flask-app-service:
    build: .  # Aponta para o diretório atual
    ports:
      - "5000:5000"  # Mapeia a porta 5000 do container para a porta 5000 do host
    environment:
      - PYTHONUNBUFFERED=1  # Para garantir que os logs sejam exibidos em tempo real
```

### 7. **Rodar a Aplicação**

Com todos os arquivos configurados, agora você pode rodar a aplicação Flask com Docker. No terminal, na pasta `minha-app-flask`, execute o seguinte comando:

```bash
docker-compose up --build
```

Esse comando irá:
- Construir a imagem Docker da sua aplicação.
- Iniciar um container executando sua aplicação Flask.

### 8. **Acessar a Aplicação**

Depois que o comando acima for executado, abra o seu navegador e vá para `http://localhost:5000`. Você deve ver a mensagem "Olá, Docker!".

# Estrutura

![alt text](image.png)