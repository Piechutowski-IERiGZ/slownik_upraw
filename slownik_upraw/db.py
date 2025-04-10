import sqlite3 as s3


table_kategoria = """
CREATE TABLE IF NOT EXISTS Kategoria (
    IdKategoria TEXT PRIMARY KEY NOT NULL,
    Nazwa TEXT
);
"""

table_podkategoria = """
CREATE TABLE IF NOT EXISTS PodKategoria (
    IdPodKategoria TEXT PRIMARY KEY NOT NULL,
    Nazwa TEXT,
    IdKategoria TEXT,
    FOREIGN KEY (IdKategoria) REFERENCES Kategoria(IdKategoria)
);
"""

table_gatunek = """
CREATE TABLE IF NOT EXISTS Gatunek (
    IdGatunek TEXT PRIMARY KEY NOT NULL,
    Nazwa TEXT,
    IdPodKategoria TEXT,
    FOREIGN KEY (IdPodKategoria) REFERENCES PodKategoria(IdPodKategoria)
);
"""

table_uprawy = """
CREATE TABLE IF NOT EXISTS Uprawy (
    IdUprawy TEXT PRIMARY KEY NOT NULL,
    IdGatunek TEXT,
    NazwaUprawy TEXT,
    FOREIGN KEY (IdGatunek) REFERENCES Gatunek(IdGatunek)
);
"""

table_rodzaje_produktow = """
CREATE TABLE IF NOT EXISTS RodzajeProduktow (
    IdRodzajuProduktu TEXT PRIMARY KEY NOT NULL,
    NazwaRodzajuProduktu TEXT
);
"""

table_uprawy_rodzaje_produktow = """
CREATE TABLE IF NOT EXISTS Uprawy_RodzajeProduktow (
    IdUprawy TEXT NOT NULL,
    IdRodzajuProduktu TEXT NOT NULL,
    PRIMARY KEY (IdUprawy, IdRodzajuProduktu),
    FOREIGN KEY (IdUprawy) REFERENCES Uprawy(IdUprawy),
    FOREIGN KEY (IdRodzajuProduktu) REFERENCES RodzajeProduktow(IdRodzajuProduktu)
);
"""

insert_kategoria = """
INSERT INTO Kategoria (IdKategoria, Nazwa) VALUES ('01', 'Rośliny');
"""

insert_podkategoria = """
INSERT INTO PodKategoria (IdPodKategoria, Nazwa, IdKategoria) VALUES
    ('01.11', 'ROŚLINY INNE NIŻ WIELOLETNIE', '01'),
    ('01.14', 'TRZCINA CUKROWA', '01'),
    ('01.15', 'TYTOŃ NIEPRZETWORZONY', '01'),
    ('01.19', 'POZOSTAŁE ROŚLINY INNE NIŻ WIELOLETNIE', '01');
"""

insert_gatunek = """
INSERT INTO Gatunek (IdGatunek, Nazwa, IdPodKategoria) VALUES
    ('01.19.1', 'ROŚLINY PASTEWNE', '01.19'),
    ('01.19.10', 'ROŚLINY PASTEWNE', '01.19'),
    ('01.19.2', 'KWIATY CIĘTE I PĄKI KWIATOWE; NASIONA KWIATÓW', '01.19'),
    ('01.19.21', 'Kwiaty cięte i pąki kwiatowe', '01.19'),
    ('01.19.22', 'Nasiona kwiatów', '01.19'),
    ('01.19.3', 'NASIONA ROŚLIN PASTEWNYCH', '01.19'),
    ('01.19.31', 'Nasiona roślin pastewnych', '01.19'),
    ('01.19.39', 'Pozostałe surowe produkty roślinne', '01.19'),
    ('01.14.1', 'TRZCINA CUKROWA', '01.14'),
    ('01.15.1', 'TYTOŃ NIEPRZETWORZONY', '01.15'),
    ('01.11.1', 'PSZENICA', '01.11'),
    ('01.11.11', 'Pszenica durum', '01.11'),
    ('01.11.12', 'Pozostała pszenica', '01.11'),
    ('01.11.2', 'Kukurydza', '01.11'),
    ('01.11.31', 'Jęczmień', '01.11'),
    ('01.11.32', 'Żyto', '01.11'),
    ('01.11.33', 'Owies', '01.11');
"""

insert_uprawy = """
INSERT INTO Uprawy (IdUprawy, NazwaUprawy, IdGatunek) VALUES
    ('01.11.11.0', 'Pszenica durum', '01.11.11'),
    ('01.11.12', 'Pozostała pszenica', '01.11.12'),
    ('01.11.20.0', 'Kukurydza', '01.11.20'),
    ('01.11.31.0', 'Jęczmień', '01.11.31'),
    ('01.11.32.0', 'Żyto', '01.11.32'),
    ('01.11.33.0', 'Owies', '01.11.33'),
    ('01.14.10.0', 'TRZCINA CUKROWA', '01.14.10'),
    ('01.15.10.0', 'TYTOŃ NIEPRZETWORZONY', '01.15.10'),
    ('01.19.10.0', 'ROŚLINY PASTEWNE', '01.19.10'),
    ('01.19.21.0', 'Kwiaty cięte i pąki kwiatowe', '01.19.21'),
    ('01.19.22.0', 'Nasiona kwiatów', '01.19.22'),
    ('01.19.31.0', 'Nasiona roślin pastewnych', '01.19.31'),
    ('01.19.39.0', 'Pozostałe surowe produkty roślinne', '01.19.39');
"""

insert_rodzaje_produktow = """
INSERT INTO RodzajeProduktow (IdRodzajuProduktu, NazwaRodzajuProduktu) VALUES
    ('101', 'na ziarno'),
    ('102', 'na owoce'),
    ('103', 'na bulwy'),
    ('104', 'na korzenie'),
    ('105', 'na kłącza'),
    ('106', 'na łodygi/włókna'),
    ('107', 'na liście'),
    ('108', 'na zielonkę'),
    ('109', 'na siano'),
    ('110', 'na słomę'),
    ('111', 'na nasiona/sadzonki'),
    ('112', 'na nawóz zielony'),
    ('113', 'na łuski/plewy');
"""

insert_uprawy_rodzaje_produktow = """
INSERT INTO Uprawy_RodzajeProduktow (IdUprawy, IdRodzajuProduktu)
VALUES
    ('01.11.11.0', '101'),
    ('01.11.11.0', '110'),
    ('01.11.12', '101'),
    ('01.11.12', '110'),
    ('01.11.20.0', '101'),
    ('01.11.20.0', '108'),
    ('01.11.31.0', '101'),
    ('01.11.31.0', '110'),
    ('01.11.32.0', '101'),
    ('01.11.32.0', '110'),
    ('01.11.33.0', '101'),
    ('01.11.33.0', '109'),
    ('01.14.10.0', '106'),
    ('01.15.10.0', '107'),
    ('01.19.10.0', '108'),
    ('01.19.10.0', '109'),
    ('01.19.21.0', '102'),
    ('01.19.22.0', '111'),
    ('01.19.31.0', '111'),
    ('01.19.39.0', '113');
"""

_connection = s3.connect(":memory:")


async def run_fixture():
    # Execute table creation
    _connection.execute(table_kategoria)
    _connection.execute(table_podkategoria)
    _connection.execute(table_gatunek)
    _connection.execute(table_uprawy)
    _connection.execute(table_rodzaje_produktow)
    _connection.execute(table_uprawy_rodzaje_produktow)

    # Execute insertions
    _connection.execute(insert_kategoria)
    _connection.execute(insert_podkategoria)
    _connection.execute(insert_gatunek)
    _connection.execute(insert_uprawy)
    _connection.execute(insert_rodzaje_produktow)
    _connection.execute(insert_uprawy_rodzaje_produktow)

    _connection.commit()


async def connection() -> s3.Connection:
    return _connection


async def close_connection():
    _connection.close()







