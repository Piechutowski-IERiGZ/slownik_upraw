import sqlite3 as s3

# Table creation statements
sql_kategoria = """CREATE TABLE IF NOT EXISTS "Kategoria" (
    "IdKategoria" TEXT PRIMARY KEY NOT NULL,
    "Nazwa" TEXT
);"""

sql_podkategoria = """CREATE TABLE IF NOT EXISTS "PodKategoria" (
    "IdPodKategoria" TEXT PRIMARY KEY NOT NULL,
    "Nazwa" TEXT,
    "IdKategoria" TEXT,
    FOREIGN KEY ("IdKategoria") REFERENCES "Kategoria" ("IdKategoria")
);"""

sql_gatunek = """CREATE TABLE IF NOT EXISTS "Gatunek" (
    "IdGatunek" TEXT PRIMARY KEY NOT NULL,
    "Nazwa" TEXT,
    "IdPodKategoria" TEXT,
    FOREIGN KEY ("IdPodKategoria") REFERENCES "PodKategoria" ("IdPodKategoria")
);"""

sql_uprawy = """CREATE TABLE IF NOT EXISTS "Uprawy" (
    "IdUprawy" TEXT PRIMARY KEY NOT NULL,
    "IdGatunek" TEXT,
    "NazwaUprawy" TEXT,
    FOREIGN KEY ("IdGatunek") REFERENCES "Gatunek" ("IdGatunek")
);"""

sql_rodzaje_produktow = """CREATE TABLE IF NOT EXISTS "RodzajeProduktow" (
    "IdRodzajuProduktu" TEXT PRIMARY KEY NOT NULL,
    "NazwaRodzajuProduktu" TEXT
);"""

sql_uprawy_rodzaje_produktow = """CREATE TABLE IF NOT EXISTS "Uprawy_RodzajeProduktow" (
    "IdUprawy" TEXT NOT NULL,
    "IdRodzajuProduktu" TEXT NOT NULL,
    PRIMARY KEY ("IdUprawy", "IdRodzajuProduktu"),
    FOREIGN KEY ("IdUprawy") REFERENCES "Uprawy" ("IdUprawy"),
    FOREIGN KEY ("IdRodzajuProduktu") REFERENCES "RodzajeProduktow" ("IdRodzajuProduktu")
);"""

# Insert statements
insert_kategoria = """INSERT INTO "Kategoria" ("IdKategoria", "Nazwa") VALUES ('01', 'Rośliny');"""

insert_podkategoria = """INSERT INTO "PodKategoria" ("IdPodKategoria", "Nazwa", "IdKategoria") VALUES
    ('01.11', 'ROŚLINY INNE NIŻ WIELOLETNIE', '01'),
    ('01.14', 'TRZCINA CUKROWA', '01'),
    ('01.15', 'TYTOŃ NIEPRZETWORZONY', '01'),
    ('01.19', 'POZOSTAŁE ROŚLINY INNE NIŻ WIELOLETNIE', '01');"""

insert_gatunek = """-- Insert into Uprawy
-- Insert into Gatunek
INSERT INTO "Gatunek" ("IdGatunek", "Nazwa", "IdPodKategoria") VALUES
('01.19.1', 'ROŚLINY PASTEWNE', '01.19'),
('01.19.10', 'ROŚLINY PASTEWNE', '01.19'),
('01.19.2', 'KWIATY CIĘTE I PĄKI KWIATOWE; NASIONA KWIATÓW', '01.19'),
('01.19.21', 'Kwiaty cięte i pąki kwiatowe', '01.19'),
('01.19.22', 'Nasiona kwiatów', '01.19'),
('01.19.3', 'NASIONA ROŚLIN PASTEWNYCH, WŁĄCZAJĄC NASIONA BURAKÓW PASTEWNYCH; POZOSTAŁE SUROWE PRODUKTY ROŚLINNE', '01.19'),
('01.19.31', 'Nasiona roślin pastewnych, włączając nasiona buraków pastewnych', '01.19'),
('01.19.39', 'Pozostałe surowe produkty roślinne, gdzie indziej niesklasyfikowane', '01.19'),
('01.14.1', 'TRZCINA CUKROWA', '01.14'),
('01.14.10', 'TRZCINA CUKROWA', '01.14'),
('01.15.1', 'TYTOŃ NIEPRZETWORZONY', '01.15'),
('01.15.10', 'TYTOŃ NIEPRZETWORZONY', '01.15'),
('01.11.1', 'PSZENICA', '01.11'),
('01.11.11', 'Pszenica durum', '01.11'),
('01.11.12', 'Pozostała pszenica', '01.11'),
('01.11.2', 'Kukurydza', '01.11'),
('01.11.20', 'Kukurydza', '01.11'),
('01.11.3', 'JĘCZMIEŃ, ŻYTO I OWIES', '01.11'),
('01.11.31', 'Jęczmień', '01.11'),
('01.11.32', 'Żyto', '01.11'),
('01.11.33', 'Owies', '01.11');

"""

insert_uprawy = """-- Insert into Uprawy
INSERT INTO "Uprawy" ("IdUprawy", "NazwaUprawy", "IdGatunek") VALUES
('01.11.11.0', 'Pszenica durum', '01.11.11'),
('01.11.12', 'Pozostała pszenica', '01.11.12'),
('01.11.20.0', 'Kukurydza (z wyłączeniem kukurydzy cukrowej i pastewnej)', '01.11.20'),
('01.11.31.0', 'Jęczmień', '01.11.31'),
('01.11.32.0', 'Żyto', '01.11.32'),
('01.11.33.0', 'Owies', '01.11.33'),
('01.14.10.0', 'TRZCINA CUKROWA', '01.14.10'),
('01.15.10.0', 'TYTOŃ NIEPRZETWORZONY', '01.15.10'),
('01.19.10.0', 'ROŚLINY PASTEWNE', '01.19.10'),
('01.19.21.0', 'Kwiaty cięte i pąki kwiatowe', '01.19.21'),
('01.19.22.0', 'Nasiona kwiatów', '01.19.22'),
('01.19.31.0', 'Nasiona roślin pastewnych, włączając nasiona buraków pastewnych', '01.19.31'),
('01.19.39.0', 'Pozostałe surowe produkty roślinne, gdzie indziej niesklasyfikowane', '01.19.39');
"""

insert_rodzaje_produktow = """-- Insert into RodzajeProduktow
INSERT INTO "RodzajeProduktow" ("IdRodzajuProduktu", "NazwaRodzajuProduktu") VALUES
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

insert_uprawy_rodzaje_produktow = """-- Insert random relations into Uprawy_RodzajeProduktow
INSERT INTO "Uprawy_RodzajeProduktow" ("IdUprawy", "IdRodzajuProduktu") VALUES
('01.11.11.0', '101'), -- Pszenica durum -> na ziarno
('01.11.11.0', '110'), -- Pszenica durum -> na słomę
('01.11.12', '101'), -- Pozostała pszenica -> na ziarno
('01.11.12', '110'), -- Pozostała pszenica -> na słomę
('01.11.20.0', '101'), -- Kukurydza -> na ziarno
('01.11.20.0', '108'), -- Kukurydza -> na zielonkę
('01.11.31.0', '101'), -- Jęczmień -> na ziarno
('01.11.31.0', '110'), -- Jęczmień -> na słomę
('01.11.32.0', '101'), -- Żyto -> na ziarno
('01.11.32.0', '110'), -- Żyto -> na słomę
('01.11.33.0', '101'), -- Owies -> na ziarno
('01.11.33.0', '109'), -- Owies -> na siano
('01.14.10.0', '106'), -- Trzcina cukrowa -> na łodygi/włókna
('01.15.10.0', '107'), -- Tytoń nieprzetworzony -> na liście
('01.19.10.0', '108'), -- Rośliny pastewne -> na zielonkę
('01.19.10.0', '109'), -- Rośliny pastewne -> na siano
('01.19.21.0', '102'), -- Kwiaty cięte -> na owoce
('01.19.22.0', '111'), -- Nasiona kwiatów -> na nasiona/sadzonki
('01.19.31.0', '111'), -- Nasiona roślin pastewnych -> na nasiona/sadzonki
('01.19.39.0', '113'); -- Pozostałe surowe produkty -> na łuski/plewy
"""

# Function only executes queries
def create_db_structure():
    with s3.connect("db.sqlite") as conn:
        cursor = conn.cursor()

        # Execute table creation
        cursor.execute(sql_kategoria)
        cursor.execute(sql_podkategoria)
        cursor.execute(sql_gatunek)
        cursor.execute(sql_uprawy)
        cursor.execute(sql_rodzaje_produktow)
        cursor.execute(sql_uprawy_rodzaje_produktow)

        # Execute insertions
        cursor.execute(insert_kategoria)
        cursor.execute(insert_podkategoria)
        cursor.execute(insert_gatunek)
        cursor.execute(insert_uprawy)
        cursor.execute(insert_rodzaje_produktow)
        cursor.execute(insert_uprawy_rodzaje_produktow)

        conn.commit()


if __name__ == '__main__':
    create_db_structure()
