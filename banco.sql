CREATE DATABASE sistema_reuso_agua;

\c sistema_reuso_agua;

CREATE TABLE leituras (
    id SERIAL PRIMARY KEY,
    distancia NUMERIC(10,2),
    volume NUMERIC(10,2),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO leituras (distancia, volume) VALUES
(71.62, 56.76),
(32.31, 135.38),
(18.08, 163.84),
(54.90, 90.20),
(17.98, 164.04);
