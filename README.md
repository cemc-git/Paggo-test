
---

# PAGGO – Teste Prático de Pipeline ETL

Este projeto é uma simulação de um pipeline ETL (Extract, Transform, Load) com dois bancos PostgreSQL (fonte e alvo), uma API para extração de dados e um processo de transformação/carregamento, tudo orquestrado com Docker.

---

## 🐳 Como rodar o projeto com Docker

Para iniciar todos os containers (bancos de dados, API de origem e pipeline ETL), execute:

```bash
docker-compose -p paggo -f "CAMINHO_PARA_app.yml" up -d
```

Isso irá:

* Subir dois containers de banco de dados PostgreSQL.
* Popular automaticamente o banco **source** com dados aleatórios.
* Criar automaticamente a tabela no banco **target** via SQLAlchemy no container ETL.

> **Obs:** Os dados gerados terão timestamps a partir do dia atual da execução e se estenderão por 10 dias.

---

## 📅 Executar o ETL para uma data específica

Você pode definir a variável de ambiente `DATE_INPUT` no `Dockerfile.etl` com o valor da data desejada no formato `DD-MM-YYYY`.

```dockerfile
ENV DATE_INPUT=05-05-2025
```

Depois, **rebuild a imagem** para aplicar a mudança:

```bash
docker-compose -p paggo -f "CAMINHO_PARA_app.yml" build
```

---

## ⚙️ Rodando sem Docker

Se desejar rodar localmente sem alguns containers:

1. Altere as URLs no `app.yml`, trocando os nomes dos serviços para `localhost`.

2. Instale os requirements:

```bash
pip install -r requirements.txt
```

3. Em um terminal, rode o servidor da API:

```bash
fastapi run ./source-api/main.py
```

4. Em outro terminal, rode o ETL manualmente:

```bash
python target-etl/pipeline_etl.py
```

> Utilize a função `generate_dates("05-05-2025")` para gerar uma lista de datas para testar.

---

## 🔍 Acessar os bancos de dados

Entre no container desejado e use o `psql`:

```bash
psql -U paggo -d source
```

ou

```bash
psql -U paggo -d target
```

Execute queries normalmente, por exemplo:

```sql
SELECT * FROM data LIMIT 10;
SELECT * FROM signal LIMIT 10;
```

> **Dica:** lembra do ponto e virgula por favor, fiquei 1 hora tentando printar o resultado mas não tava entendendo o motivo

---

## ⚠️ Comentários sobre o Teste

* A implementação feita no pipeline foi pensada para ser passada uma lista de datas, utilizando o dask com um bag para fazer as requisições utilizando paralelismo trazendo mais velocidade, caso deseje testar pode utilizar o método de generate_dates para pegar uma lista de 10 dias.

### ✍️ Coisas que poderiam ser melhores:

* Uso de `.env` para separar variáveis de ambiente e deixar o código mais configurável.
* Tipagem e comentários mais detalhados nos métodos.
* Substituir `print()` por `logging` com níveis apropriados.
* Implementação do bônus com Dagster para orquestração.

---

## 💬 Feedback Pessoal

* Levei cerca de **6 horas** para implementar tudo.
* No início fiquei bastante confuso com a estrutura da tabela `Signal`, tive que reler algumas vezes até conseguir clareza (e pedi ajuda pro ChatGPT 😅).
* No geral foi bem divertido, alguma das coisas nunca tive contato e gostaria de ter feito essa parte do dagster mas infelizmente não vou ter tempo para tentar concluir

---
