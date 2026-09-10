# Encurtador de URLs

API que recebe uma URL longa, gera um código curto de 6 caracteres e redireciona quem acessa esse código pra URL original — registrando quantos acessos (`hits`) cada link teve.

## Stack

- **Python + FastAPI** — API
- **SQLAlchemy + MySQL** — persistência
- **uv** — gerenciador de dependências
- **Docker Compose** — orquestração (app + banco)

## Estrutura

```
encurtador-url/
├── app/
│   ├── main.py          # FastAPI app e endpoints
│   ├── shortener.py      # geração do código curto
│   └── db/
│       ├── session.py    # engine, SessionLocal, get_db()
│       └── models.py     # modelo ShortURL
├── Dockerfile
├── docker-compose.yaml
├── Makefile
└── pyproject.toml
```

## Como rodar

1. Crie um `.env` na raiz do projeto:

   ```
   MYSQL_ROOT_PASSWORD=alguma_senha
   MYSQL_DATABASE=db_encurtador
   MYSQL_USER=user_encurtador
   MYSQL_PASSWORD=outra_senha
   ```

2. Suba os containers:

   ```bash
   make up
   ```

A API fica disponível em `http://localhost:8080`. O MySQL fica exposto ao host na porta `3307` (mapeado pra `3306` dentro do container).

## Comandos do Makefile

|               Comando             |                                   O que faz                               |
|-----------------------------------|---------------------------------------------------------------------------|
| `make up`                         | builda e sobe os containers                                               |
| `make down`                       | derruba os containers                                                     |
| `make restart`                    | down + up                                                                 |
| `make logs`                       | segue os logs do app                                                      |
| `make ps`                         | status dos containers                                                     |
| `make shorten URL=https://...`    | testa o endpoint de encurtar                                              |
| `make test-redirect CODE=abc123`  | testa o redirecionamento                                                  |
| `make hits`                       | mostra a tabela `short_urls` (código, url, hits, data) direto no banco    |
| `make clean`                      | derruba tudo e apaga o volume do banco                                    |

## Endpoints

**Encurtar uma URL**

```bash
curl -X POST http://localhost:8080/shorten-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

```json
{"short_code": "aZ3kQ1", "short_url": "http://localhost:8080/aZ3kQ1"}
```

**Redirecionar (e registrar o hit)**

```bash
curl -i http://localhost:8080/aZ3kQ1
```

Retorna `302 Found` com o `location` apontando pra URL original.

## Respostas - Desafio de arquitetura

### Disponibilidade
Se o banco cair por 10 segundos, **todo request**, inclusive o simples redirecionamento de um link que já existe, falha, porque a rota de redirecionamento depende de uma consulta ao banco pra saber pra onde mandar o usuário. Sem um cache na frente do banco, não existe caminho para responder sem ele. Para melhorar esse processo, seria bom adicionar um cache (Redis, ou até em memória) para os códigos mais acessados, de forma que o redirecionamento sobreviva a uma indisponibilidade curta do banco.

### Consistência
A geração do `short_code` usa a constraint `UNIQUE` do banco como árbitro final: se dois usuários gerarem exatamente o mesmo código no mesmo milissegundo, ambos tentam o `INSERT`, mas o banco garante atomicidade, só um é aceito, o outro recebe uma violação de unicidade e a aplicação tenta de novo com outro código (ver `app/shortener.py`). Checar unicidade em memória antes de inserir não seria seguro, pois abriria uma janela de corrida entre a checagem e a escrita.

### Desempenho
Como a API e a escrita no banco vivem no mesmo processo, o tempo do `POST /shorten-url` é a soma do tempo de gerar o código **mais** o tempo de ida e volta ao MySQL (rede + disco + índice único). Se o banco estiver sob carga, o usuário que só quer encurtar uma URL sente a lentidão do banco como se fosse lentidão da própria API, não há isolamento entre a camada de API e a de persistência. Desacoplar a escrita (ex: fila assíncrona) ou escalar horizontalmente atrás de um load balancer resolveria isso, ao custo de mais complexidade operacional.
