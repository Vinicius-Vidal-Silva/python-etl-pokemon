from functions import extrair_pokemon_por_id, transformar_pokemon
import pyodbc
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

id_atual = 1
ultimo_id = 1025

while id_atual <= ultimo_id:

    print(f"Processando Pokémon {id_atual}...")

    dados = extrair_pokemon_por_id(id_atual)

    if dados:

        # TRANSFORMAÇÃO
        base, tipos, stats, abilities = transformar_pokemon(dados)

        try:
            #  BRONZE (controle de carga)
            cursor.execute(insert_bronze, (base[0], base[1]))

            # SILVER
            cursor.execute(insert_pokemon, base)
            cursor.executemany(insert_tipo, tipos)
            cursor.executemany(insert_stat, stats)
            cursor.executemany(insert_ability, abilities)

            connector.commit()
            print(f"Pokémon {id_atual} inserido com sucesso.")

        except Exception as e:
            connector.rollback()
            print(f"Erro ao inserir Pokémon {id_atual}: {e}")

    id_atual += 1

cursor.close()
connector.close()

print("Carga finalizada com sucesso.")