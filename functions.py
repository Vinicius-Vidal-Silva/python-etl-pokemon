import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def url_inicial(pokemon_id: int) -> str:
    """
    Monta a URL base para consulta do Pokémon por ID.
    """
    return f"{BASE_URL}/{pokemon_id}"


def verificar_resposta(response: requests.Response) -> bool:
    """
    Verifica se a resposta da API foi bem-sucedida.
    """
    return response.status_code == 200


def extrair_pokemon_por_id(pokemon_id: int) -> dict | None:
    """
    Faz a requisição para a PokéAPI e retorna o JSON completo.
    """
    url = url_inicial(pokemon_id)
    response = requests.get(url)

    if not verificar_resposta(response):
        print(f"Erro ao buscar Pokémon ID {pokemon_id} (status {response.status_code})")
        return None

    return response.json()


def transformar_pokemon(dados: dict):
    """
    Transforma o JSON bruto em estruturas relacionais
    compatíveis com o modelo Silver.
    """

    #  Tabela principal
    pokemon_base = (
        dados["id"],
        dados["name"],
        dados["height"],
        dados["weight"],
        dados["base_experience"],
    )

    #  Tipos
    tipos = [
        (
            dados["id"],
            tipo["slot"],
            tipo["type"]["name"]
        )
        for tipo in dados["types"]
    ]

    #  Stats
    stats = [
        (
            dados["id"],
            stat["stat"]["name"],
            stat["base_stat"]
        )
        for stat in dados["stats"]
    ]

    #  Abilities
    abilities = [
        (
            dados["id"],
            ability["ability"]["name"],
            1 if ability["is_hidden"] else 0
        )
        for ability in dados["abilities"]
    ]

    return pokemon_base, tipos, stats, abilities