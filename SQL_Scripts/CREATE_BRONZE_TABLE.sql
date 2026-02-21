CREATE TABLE Bronze_Pokemon_Load (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    PokemonId INT,
    Nome VARCHAR(100),
    DataCarga DATETIME DEFAULT GETDATE()
);
