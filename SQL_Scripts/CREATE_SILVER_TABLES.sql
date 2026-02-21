CREATE TABLE Silver_Pokemon (
    Id INT PRIMARY KEY,
    Nome VARCHAR(100),
    Altura INT,
    Peso INT,
    BaseExperience INT,
    DataCarga DATETIME DEFAULT GETDATE()
);

CREATE TABLE Silver_Pokemon_Tipo (
    PokemonId INT,
    Slot INT,
    Tipo VARCHAR(50),
    PRIMARY KEY (PokemonId, Slot),
    FOREIGN KEY (PokemonId) REFERENCES Silver_Pokemon(Id)
);

CREATE TABLE Silver_Pokemon_Stat (
    PokemonId INT,
    NomeStat VARCHAR(50),
    Valor INT,
    PRIMARY KEY (PokemonId, NomeStat),
    FOREIGN KEY (PokemonId) REFERENCES Silver_Pokemon(Id)
);

CREATE TABLE Silver_Pokemon_Ability (
    PokemonId INT,
    Ability VARCHAR(100),
    IsHidden BIT,
    PRIMARY KEY (PokemonId, Ability),
    FOREIGN KEY (PokemonId) REFERENCES Silver_Pokemon(Id)
);