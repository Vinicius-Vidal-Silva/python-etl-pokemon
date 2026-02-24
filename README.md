# 🇧🇷 [PT-BR]

````markdown
# 🧩 Pokédex Data Pipeline

Projeto de engenharia de dados que consome a API pública da PokéAPI, realiza transformação dos dados em Python e carrega as informações em um banco relacional (SQL Server), utilizando arquitetura em camadas Bronze, Silver e Gold.

---

## 📌 Objetivo

Construir um pipeline ETL completo:

- Extração de dados via API REST
- Transformação estruturada em Python
- Modelagem relacional no SQL Server
- Carga incremental baseada em ID
- Criação de views analíticas (Camada Gold)

---

## 🏗 Arquitetura

### 🥉 Bronze
Tabela de controle de carga:

- `Bronze_Pokemon_Load`

Armazena informações básicas para auditoria da ingestão.

---

### 🥈 Silver
Camada relacional normalizada:

- `Silver_Pokemon`
- `Silver_Pokemon_Tipo`
- `Silver_Pokemon_Stat`
- `Silver_Pokemon_Ability`

Transformação pesada ocorre no Python, evitando processamento de JSON dentro do SQL Server.

---

### 🥇 Gold
Camada analítica composta por views como:

- Ranking por Base Experience
- Top 10 por Ataque
- Média de ataque por Tipo
- Distribuições estatísticas

---

## 🔄 Carga Incremental

O arquivo `update.py`:

- Consulta o maior ID existente no banco
- Verifica a quantidade total disponível na API
- Insere apenas novos Pokémons
- Evita duplicidade de dados

---

## 🛠 Tecnologias Utilizadas

- Python
- requests
- pyodbc
- python-dotenv
- Microsoft SQL Server
- PokéAPI

---

## ⚙️ Como Executar

### 1️⃣ Instalar dependências

```bash
pip install -r requirements.txt
````

### 2️⃣ Criar arquivo `.env`

```
DB_DRIVER=
DB_SERVER=
DB_DATABASE=
DB_TRUSTED=
```

### 3️⃣ Executar carga inicial

```
python request.py
```

### 4️⃣ Executar atualização incremental

```
python update.py
```

---

## 📊 Próximos Passos

* Dashboard em Power BI
* Implementação de controle de hash para detectar updates
* Orquestração de pipeline
* Publicação como projeto de portfólio

---

## 🚀 Sobre o Projeto

Este projeto foi desenvolvido com foco em prática de Engenharia de Dados, modelagem relacional e boas práticas de organização de código e versionamento.

````

---

# 🇺🇸 [EN-US]

```markdown
# 🧩 Pokédex Data Pipeline

A data engineering project that consumes the public PokéAPI, transforms the data using Python, and loads structured information into a relational database (SQL Server) using a Bronze, Silver, and Gold architecture.

---

## 📌 Objective

Build a complete ETL pipeline:

- Data extraction via REST API
- Structured transformation in Python
- Relational modeling in SQL Server
- Incremental loading based on ID
- Analytical views (Gold Layer)

---

## 🏗 Architecture

### 🥉 Bronze
Load control table:

- `Bronze_Pokemon_Load`

Stores basic ingestion metadata.

---

### 🥈 Silver
Normalized relational layer:

- `Silver_Pokemon`
- `Silver_Pokemon_Tipo`
- `Silver_Pokemon_Stat`
- `Silver_Pokemon_Ability`

Heavy JSON transformation is handled in Python to avoid processing overhead in SQL Server.

---

### 🥇 Gold
Analytical layer composed of views such as:

- Base Experience ranking
- Top 10 by attack
- Average attack per type
- Statistical distributions

---

## 🔄 Incremental Load

The `update.py` script:

- Checks the highest existing ID in the database
- Compares it with the API total count
- Inserts only new Pokémon
- Prevents duplicate records

---

## 🛠 Technologies Used

- Python
- requests
- pyodbc
- python-dotenv
- Microsoft SQL Server
- PokéAPI

---

## ⚙️ How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
````

### 2️⃣ Create a `.env` file

```
DB_DRIVER=
DB_SERVER=
DB_DATABASE=
DB_TRUSTED=
```

### 3️⃣ Run initial load

```
python request.py
```

### 4️⃣ Run incremental update

```
python update.py
```

---

## 📊 Future Improvements

* Power BI dashboard
* Hash-based update detection
* Pipeline orchestration
* Portfolio publication strategy

---

## 🚀 About

This project was developed as a hands-on data engineering practice focused on relational modeling, ETL design, incremental loading, and clean project structure.

```

---
