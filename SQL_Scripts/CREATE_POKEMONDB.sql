-- 1. Cria o Banco de Dados (se não existir)
CREATE DATABASE PokemonDB;
GO

USE PokemonDB;
GO

-- 2. Cria a tabela de Staging (Camada "Bronze" ou "Raw")
-- Usamos NVARCHAR(MAX) porque o JSON de um pokemon pode ser grande.
CREATE TABLE Staging_Pokemon (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    PokemonId INT,           -- O ID do pokemon (ex: 1, 25, 150)
    Nome VARCHAR(100),       -- O nome (só para facilitar a busca visual)
    JsonDados NVARCHAR(MAX), -- AQUI fica o ouro: o JSON completo
    DataCarga DATETIME DEFAULT GETDATE()
);
GO

SELECT TOP 10 *
FROM Staging_Pokemon;

-- Exclui os dados da tabela caso seja necessário reestartando o id
--DROP TABLE dbo.Staging_Pokemon;

ALTER TABLE Staging_Pokemon
ADD JsonPokemonId AS (CAST(JSON_VALUE(JsonDados, '$.id') AS INT)) PERSISTED;

ALTER TABLE Staging_Pokemon
DROP COLUMN JsonPokemonId;

CREATE NONCLUSTERED INDEX IX_JsonPokemonId
ON Staging_Pokemon (JsonPokemonId);

SELECT PokemonId, JsonDados
FROM Staging_Pokemon
WHERE ISJSON(JsonDados) = 0;

SELECT TOP 10
    T1.id,
    T1.PokemonId,
    T1.Nome,
    JSON_VALUE(JsonDados, '$.height') AS 'Altura',
    T1.DataCarga,
    TIPOS.Tipo AS 'NomeTipo'
FROM Staging_Pokemon AS T1
CROSS APPLY 
    OPENJSON(T1.JsonDados, '$.types')
    WITH(
        Tipo VARCHAR(50) '$.type.name',
        TipoOrdem INT 'key'
    ) AS TIPOS;