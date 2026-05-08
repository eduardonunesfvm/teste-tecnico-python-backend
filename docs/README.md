# 📊 API de Foco e Produtividade

API REST desenvolvida em **FastAPI** para registrar sessões de trabalho e gerar diagnósticos inteligentes de produtividade. O usuário pode registrar seus blocos de foco e, ao final, obter um resumo analítico do seu desempenho.


## 🛠 Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11 | Linguagem principal |
| FastAPI | 0.136.1 | Framework web |
| SQLAlchemy | 2.0.49 | ORM para banco de dados |
| Alembic | 1.18.4 | Migrações do banco de dados |
| SQLite | — | Banco de dados relacional (arquivo local) |
| Pydantic | 2.13.4 | Validação de dados |
| Uvicorn | 0.46.0 | Servidor ASGI |
| Docker | — | Containerização |


## 📁 Estrutura do Projeto

```
teste-tecnico-python-backend/
├── alembic/                    # Migrações do banco de dados
│   └── versions/
├── api/
│   ├── producao/
│   │   ├── __init__.py
│   │   ├── models.py           # Modelo ORM da tabela de registros
│   │   ├── repository.py       # Camada de acesso ao banco de dados
│   │   ├── router.py           # Definição das rotas (endpoints)
│   │   ├── schemas.py          # Schemas de validação (Pydantic)
│   │   └── service.py          # Regras de negócio e lógica da aplicação
│   ├── __init__.py
│   ├── database.py             # Configuração da conexão com o banco
│   ├── dependencies.py         # Dependências injetáveis (ex: sessão do banco)
│   └── main.py                 # Entry point da aplicação
├── docs/                       # Artefatos e documentação auxiliar
├── .dockerignore
├── .gitignore
├── alembic.ini                 # Configuração do Alembic
├── Dockerfile
├── README.md
└── requirements.txt
```


## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.11+
- Docker (opcional)

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=sqlite:///./banco.db
```


## 🚀 Como Rodar o Projeto

### Opção 1 — Rodando Localmente

**1. Clone o repositório**
```bash
git clone https://github.com/eduardonunesfvm/teste-tecnico-python-backend.git
cd teste-tecnico-python-backend
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute as migrações do banco de dados**
```bash
alembic upgrade head
```

**5. Inicie o servidor**
```bash
uvicorn api.main:app --reload --port 10000
```

A API estará disponível em: `http://localhost:10000`


### Opção 2 — Rodando com Docker

**1. Build da imagem**
```bash
docker build -t api-produtividade .
```

**2. Execute o container**
```bash
docker run -p 10000:10000 --env-file .env api-produtividade
```

A API estará disponível em: `http://localhost:10000`


## 📖 Documentação Interativa

Com o servidor rodando, acesse a documentação automática gerada pelo FastAPI:

- **Swagger UI:** `http://localhost:10000/docs`
- **ReDoc:** `http://localhost:10000/redoc`


## 🛣 Endpoints

Todos os endpoints utilizam o prefixo `/producao`.


### `GET /producao/get`

Rota padrão para verificar se a API está no ar.

**Resposta:**
```json
{
  "mensagem": "Você acessou a rota padrão da api"
}
```


### `POST /producao/registrar_foco`

Registra uma sessão de foco encerrada.

**Body (JSON):**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nivel_foco` | `int` | ✅ | Nível de foco de **1 a 5** (1 = muito distraído, 5 = estado de flow) |
| `tempo_minutos` | `int` | ✅ | Duração da sessão em minutos (deve ser maior que 0) |
| `comentario` | `string` | ✅ | O que foi feito ou o que causou distração |
| `categoria` | `string` | ❌ | Categoria da sessão (ex: `coding`, `reunião`, `estudo`) |

**Exemplo de requisição:**
```json
{
  "nivel_foco": 4,
  "tempo_minutos": 45,
  "comentario": "Implementei os endpoints da API sem grandes interrupções.",
  "categoria": "coding"
}
```

**Resposta — `201 Created`:**
```json
{
  "id": 1,
  "nivel_foco": 4,
  "tempo_minutos": 45,
  "comentario": "Implementei os endpoints da API sem grandes interrupções.",
  "categoria": "coding"
}
```

**Erros possíveis:**

| Código | Motivo |
|---|---|
| `422 Unprocessable Entity` | Campo obrigatório ausente, `nivel_foco` fora do range 1–5, ou `tempo_minutos` menor ou igual a 0 |


### `GET /producao/obter_todos_registros`

Retorna todos os registros de foco cadastrados.

**Resposta — `200 OK`:**
```json
{
  "registros": [
    {
      "id": 1,
      "nivel_foco": 4,
      "tempo_minutos": 45,
      "comentario": "Implementei os endpoints da API.",
      "categoria": "coding"
    },
    {
      "id": 2,
      "nivel_foco": 2,
      "tempo_minutos": 20,
      "comentario": "Muitas notificações durante a sessão.",
      "categoria": "estudo"
    }
  ]
}
```


### `GET /producao/obter_diagnostico/visualizar`

Retorna um diagnóstico inteligente baseado em todos os registros salvos.

**Resposta — `200 OK`:**
```json
{
  "media_foco": 3.0,
  "tempo_total_minutos": 65,
  "total_registros": 2,
  "mensagem": "O diagnóstico indica que sua produtividade está baixa. Considere identificar e minimizar distrações, estabelecer metas claras e criar um ambiente de trabalho mais focado."
}
```

**Resposta quando não há registros:**
```json
{
  "media_foco": 0,
  "tempo_total_minutos": 0,
  "total_registros": 0,
  "mensagem": "Nenhum registro encontrado para gerar diagnóstico."
}
```

**Lógica do diagnóstico:**

| Média de foco | Mensagem |
|---|---|
| `<= 3` | Produtividade baixa — sugestões para minimizar distrações e melhorar o foco |
| `> 3` | Produtividade boa — incentivo a manter os hábitos produtivos |


## ✅ Decisões Técnicas

- **Arquitetura em camadas:** O projeto separa responsabilidades em `router → service → repository → model`, facilitando a manutenção e os testes.
- **Validação automática com Pydantic:** O campo `nivel_foco` é validado no schema para aceitar apenas valores entre 1 e 5. `tempo_minutos` deve ser maior que 0. Campos inválidos retornam `422` automaticamente pelo FastAPI.
- **Campo `categoria` opcional:** Permite que o usuário classifique suas sessões (ex: `coding`, `reunião`, `estudo`) sem tornar o registro mais burocrático.
- **Diagnóstico com contexto:** Além da média e do total de minutos, o endpoint de diagnóstico retorna o número total de registros e uma mensagem de feedback personalizada.
- **Migrações com Alembic:** O esquema do banco é versionado e reproduzível em qualquer ambiente.
- **Docker pronto para uso:** O `Dockerfile` usa a imagem `python:3.11-slim` para manter a imagem enxuta.


## 🤖 Uso de Inteligência Artificial

Conforme solicitado nas regras do desafio, descrevo abaixo como utilizei ferramentas de IA durante o desenvolvimento.

### Como a IA foi utilizada

A IA foi usada como um **par de revisão técnica**: apresentei dúvidas específicas de design e estrutura, avaliei as respostas e tomei as decisões com base no meu entendimento do problema.


**1. Decisão sobre a estrutura dos schemas**

Tive dúvida sobre a melhor forma de modelar os schemas Pydantic: usar dois schemas separados (um de entrada e um de saída) ou apenas um schema de registro com um response de diagnóstico. A IA confirmou a abordagem de **schemas separados por finalidade** (`RegistroSchema` para entrada e `RegistroResponse` para saída), o que ficou alinhado com as boas práticas de separação de responsabilidades.


**2. Revisão da camada de service**

Apresentei a estrutura inicial do meu `service.py` e pedi uma análise crítica. A IA apontou incoerências na assinatura das funções, como passar `RegistroResponse` onde deveria ser apenas a `Session`, o que me ajudou a corrigir a lógica antes de testar os endpoints.


**3. Validação do escopo entregue**

Ao finalizar o projeto, usei a IA para confirmar se o que havia entregue estava coerente com o que o desafio pedia. O feedback foi positivo, validando os principais pontos: FastAPI, organização em camadas, persistência com SQLite, diagnóstico calculado, validação com Pydantic, lógica de feedback e Swagger funcionando.


**4. Avaliação da decisão de usar Docker**

Antes de commitar o `Dockerfile`, questionei se incluí-lo sem um `docker-compose` seria uma decisão válida ou excessiva. A IA confirmou que um Dockerfile simples agrega valor sem parecer exagero, pois resolve padronização de ambiente, facilidade de execução e demonstra noção de containerização, decisão que mantive.

**5. Auxílio na criação dos testes automatizados**

Também utilizei IA como apoio para aprender e estruturar os testes automatizados com `pytest` e `TestClient` do FastAPI, pois ainda estou aprofundando meus conhecimentos em testes backend.

A IA foi utilizada para esclarecer:
- estrutura básica de arquivos de teste;
- funcionamento do `TestClient`;
- diferença entre testes manuais via Swagger e testes automatizados;
- interpretação de erros relacionados ao `pytest` e imports do projeto.

Os testes foram adaptados e compreendidos antes de serem aplicados ao projeto.

