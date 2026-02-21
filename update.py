from functions import extrair_pokemon_por_id, transformar_pokemon
import pyodbc
import requests

from dotenv import load_dotenv
import os

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER")
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_TRUSTED = os.getenv("DB_TRUSTED")

dados_conexao = (
    f"Driver={{{DB_DRIVER}}};"
    f"Server={DB_SERVER};"
    f"Database={DB_DATABASE};"
    f"Trusted_Connection={DB_TRUSTED};"
)

print("Conectando ao SQL Server...")
connector = pyodbc.connect(dados_conexao)
cursor = connector.cursor()

cursor.fast_executemany = True

cursor.execute("SELECT ISNULL(MAX(Id), 0) FROM Silver_Pokemon")
ultimo_id_banco = cursor.fetchone()[0]

print(f"Último Pokémon no banco: {ultimo_id_banco}")

response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1")
total_api = response.json()["count"]

print(f"Total de Pokémon na API: {total_api}")

if ultimo_id_banco >= total_api:
    print("Banco já está atualizado ✅")
    cursor.close()
    connector.close()
    exit()

insert_bronze = """
INSERT INTO Bronze_Pokemon_Load (PokemonId, Nome)
VALUES (?, ?)
"""

insert_pokemon = """
INSERT INTO Silver_Pokemon (Id, Nome, Altura, Peso, BaseExperience)
VALUES (?, ?, ?, ?, ?)
"""

insert_tipo = """
INSERT INTO Silver_Pokemon_Tipo (PokemonId, Slot, Tipo)
VALUES (?, ?, ?)
"""

insert_stat = """
INSERT INTO Silver_Pokemon_Stat (PokemonId, NomeStat, Valor)
VALUES (?, ?, ?)
"""

insert_ability = """
INSERT INTO Silver_Pokemon_Ability (PokemonId, Ability, IsHidden)
VALUES (?, ?, ?)
"""

proximo_id = ultimo_id_banco + 1

while proximo_id <= total_api:

    print(f"Inserindo novo Pokémon {proximo_id}")

    dados = extrair_pokemon_por_id(proximo_id)

    if dados:

        base, tipos, stats, abilities = transformar_pokemon(dados)

        try:
            cursor.execute(insert_bronze, (base[0], base[1]))

            cursor.execute(insert_pokemon, base)
            cursor.executemany(insert_tipo, tipos)
            cursor.executemany(insert_stat, stats)
            cursor.executemany(insert_ability, abilities)

            connector.commit()
            print(f"Pokémon {proximo_id} inserido com sucesso.")

        except Exception as e:
            connector.rollback()
            print(f"Erro ao inserir Pokémon {proximo_id}: {e}")

    proximo_id += 1

cursor.close()
connector.close()

print("Atualização concluída com sucesso 🚀")