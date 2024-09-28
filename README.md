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

Crie um ambiente virtual para instalar as dependências do projeto:

Windows:
```
python -m venv venv
```
macOS e Linux:
```
python3 -m venv venv
```

Ative o ambiente virtual:

Windows:
```
venv\Scripts\activate
```
macOS e Linux:
```
source venv/bin/activate
```

Instale as dependências do projeto:

```
pip install -r requirements.txt
```

Não esqueça de fazer um arquivo `.env` na pasta raiz.

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

### 1. Criar a rede manualmente:
Você pode criar a rede antes de subir os containers usando o comando abaixo:

```bash
docker network create my_custom_network
```

### 2. Definir os containers no `docker-compose.yml`:

Depois, no arquivo `docker-compose.yml`, associe os containers a essa rede criada:

```yaml
version: '3'
services:
  flask-1:
    image: docker-1-flask-app-service
    container_name: flask-1
    ports:
      - "5001:5000"
    networks:
      - my_custom_network

  flask-2:
    image: docker-2-flask-app-service
    container_name: flask-2
    ports:
      - "5002:5000"
    networks:
      - my_custom_network

  flask-3:
    image: docker-3-flask-app-service
    container_name: flask-3
    ports:
      - "5003:5000"
    networks:
      - my_custom_network

networks:
  my_custom_network:
    external: true
```

### Explicação:
- **`networks`:** Aqui estamos indicando que a rede `my_custom_network` já existe (`external: true`), ou seja, ela foi criada previamente e não será gerada automaticamente pelo Docker Compose.

### 3. Subir os containers:
Com a rede criada, você pode subir os containers normalmente:

```bash
docker-compose up -d
```

### Verificar os containers na rede:
Você pode verificar se os containers estão corretamente conectados à rede com o seguinte comando:

```bash
docker network inspect my_custom_network
```

Dessa forma, você cria uma rede separada e coloca os containers dentro dela para que possam se comunicar.

# Estrutura

![alt text](image.png)
