include .env

.PHONY: up down build restart logs ps shorten test-redirect hits clean

# Sobe os containers (build + start em background)
up:
	docker compose up -d --build

# Para e remove os containers
down:
	docker compose down

# So builda as imagens, sem subir
build:
	docker compose build

# Reinicia tudo do zero
restart: down up

# Segue os logs do app (Ctrl+C para sair)
logs:
	docker compose logs -f app-encurtador

# Mostra status dos containers
ps:
	docker compose ps

# Testa o endpoint de encurtar (uso: make shorten URL=https://exemplo.com)
URL ?= https://google.com
shorten:
	curl -s -X POST http://localhost:8080/shorten-url \
		-H "Content-Type: application/json" \
		-d '{"url": "$(URL)"}' | python3 -m json.tool

# Testa o redirecionamento (uso: make test-redirect CODE=abc123)
test-redirect:
	curl -is http://localhost:8080/$(CODE) | head -5

# Mostra os registros e contadores de hits direto no banco
hits:
	docker compose exec db-mysql mysql -u $(MYSQL_USER) -p$(MYSQL_PASSWORD) $(MYSQL_DATABASE) \
		-e "SELECT short_code, original_url, hits, created_at FROM short_urls;"

# Para os containers e remove volumes (apaga os dados do banco)
clean:
	docker compose down -v
