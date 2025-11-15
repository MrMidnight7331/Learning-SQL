import random
import math


NUM_FILIALEN = 5
NUM_KONTEN = 50
NUM_BESITZ_ROWS = 80
NUM_MITARBEITER = 30
NUM_KARTEN = 100
NUM_UEBERWEISUNGEN = 200

TABLE_PREFIXES = {
    "besitzt": "mm_",
    "filialen": "mm_",
    "karten": "mm_",
    "kunden": "mm_",
    "mitarbeiter": "mm_",
    "ueberweisungen": "mm_",
}


def table_name(base: str) -> str:
    prefix = TABLE_PREFIXES.get(base, "")
    if prefix.endswith("_"):
        return f"{prefix}{base}"
    return f"{prefix}{base.capitalize()}"


def esc(s: str) -> str:
    return s.replace("'", "''")


def generate_create_tables_sql() -> str:
    t_filiale = table_name("filiale")
    t_kunden = table_name("kunden")
    t_mitarbeiter = table_name("mitarbeiter")
    t_besitz = table_name("besitz")
    t_karten = table_name("karten")
    t_ueberw = table_name("ueberweisungen")

    stmts = []

    stmts.append(f"""
CREATE TABLE {t_filiale} (
    FNr     INT PRIMARY KEY,
    name    TEXT,
    adresse TEXT
);
""".strip())

    stmts.append(f"""
CREATE TABLE {t_kunden} (
    kontostand INT,
    kontotyp   TEXT,
    kontoNr    INT PRIMARY KEY,
    FNr        INT,
    FOREIGN KEY (FNr) REFERENCES {t_filiale}(FNr)
);
""".strip())

    stmts.append(f"""
CREATE TABLE {t_mitarbeiter} (
    name     TEXT,
    gehalt   FLOAT,
    MNr      INT PRIMARY KEY,
    position TEXT,
    FNr      INT,
    FOREIGN KEY (FNr) REFERENCES {t_filiale}(FNr)
);
""".strip())

    stmts.append(f"""
CREATE TABLE {t_besitz} (
    kontoNr  INT,
    kundenNr INT,
    PRIMARY KEY (kontoNr, kundenNr),
    FOREIGN KEY (kontoNr) REFERENCES {t_kunden}(kontoNr)
);
""".strip())

    stmts.append(f"""
CREATE TABLE {t_karten} (
    PIN      INT,
    kartenNr INT PRIMARY KEY,
    kontoNr  INT,
    kundenNr INT,
    FOREIGN KEY (kontoNr) REFERENCES {t_kunden}(kontoNr),
    FOREIGN KEY (kontoNr, kundenNr) REFERENCES {t_besitz}(kontoNr, kundenNr)
);
""".strip())

    stmts.append(f"""
CREATE TABLE {t_ueberw} (
    betrag   FLOAT,
    datum    INT,
    uNr      INT PRIMARY KEY,
    kontoNrS INT,
    kontoNrE INT,
    FOREIGN KEY (kontoNrS) REFERENCES {t_kunden}(kontoNr),
    FOREIGN KEY (kontoNrE) REFERENCES {t_kunden}(kontoNr)
);
""".strip())

    return "\n\n".join(stmts)



def generate_data_and_inserts() -> str:
    random.seed(42)

    t_filiale = table_name("filiale")
    t_kunden = table_name("kunden")
    t_mitarbeiter = table_name("mitarbeiter")
    t_besitz = table_name("besitz")
    t_karten = table_name("karten")
    t_ueberw = table_name("ueberweisungen")

    sql_parts = []


    filialen = []
    for i in range(1, NUM_FILIALEN + 1):
        filialen.append({
            "FNr": i,
            "name": f"Filiale {i}",
            "adresse": f"Beispielstraße {i}, Stadt{i}"
        })

    if filialen:
        values = [f"({f['FNr']}, '{esc(f['name'])}', '{esc(f['adresse'])}')" for f in filialen]
        sql_parts.append(f"INSERT INTO {t_filiale} (FNr, name, adresse) VALUES\n  " + ",\n  ".join(values) + ";\n")

    konten = []
    konto_base = 100000
    kontotypen = ["Giro", "Spar", "Business"]

    for i in range(NUM_KONTEN):
        kontoNr = konto_base + i
        FNr = random.choice(filialen)["FNr"]
        konten.append({
            "kontoNr": kontoNr,
            "kontostand": random.randint(-5000, 50000),
            "kontotyp": random.choice(kontotypen),
            "FNr": FNr
        })

    if konten:
        values = [
            f"({k['kontostand']}, '{esc(k['kontotyp'])}', {k['kontoNr']}, {k['FNr']})"
            for k in konten
        ]
        sql_parts.append(f"INSERT INTO {t_kunden} (kontostand, kontotyp, kontoNr, FNr) VALUES\n  " + ",\n  ".join(values) + ";\n")

    konto_nrs = [k["kontoNr"] for k in konten]

    mitarbeiter = []
    positions = ["Berater", "Filialleiter", "Kassierer", "Service", "IT"]

    for i in range(1, NUM_MITARBEITER + 1):
        FNr = random.choice(filialen)["FNr"]
        mitarbeiter.append({
            "MNr": i,
            "name": f"Mitarbeiter {i}",
            "gehalt": round(random.uniform(2000, 6000), 2),
            "position": random.choice(positions),
            "FNr": FNr
        })

    values = [
        f"('{esc(m['name'])}', {m['gehalt']}, {m['MNr']}, '{esc(m['position'])}', {m['FNr']})"
        for m in mitarbeiter
    ]
    sql_parts.append(f"INSERT INTO {t_mitarbeiter} (name, gehalt, MNr, position, FNr) VALUES\n  " + ",\n  ".join(values) + ";\n")

    besitz_rows = []
    used_pairs = set()
    max_kunden_nr = max(1, math.ceil(NUM_KONTEN * 1.5))

    while len(besitz_rows) < NUM_BESITZ_ROWS:
        kontoNr = random.choice(konto_nrs)
        kundenNr = random.randint(1, max_kunden_nr)
        key = (kontoNr, kundenNr)
        if key in used_pairs:
            continue
        used_pairs.add(key)
        besitz_rows.append({"kontoNr": kontoNr, "kundenNr": kundenNr})

    values = [f"({b['kontoNr']}, {b['kundenNr']})" for b in besitz_rows]
    sql_parts.append(f"INSERT INTO {t_besitz} (kontoNr, kundenNr) VALUES\n  " + ",\n  ".join(values) + ";\n")

    besitz_pairs = [(b["kontoNr"], b["kundenNr"]) for b in besitz_rows]


    karten = []
    karten_base = 500000

    for i in range(NUM_KARTEN):
        kartenNr = karten_base + i
        kontoNr, kundenNr = random.choice(besitz_pairs)
        PIN = random.randint(1000, 9999)
        karten.append({"PIN": PIN, "kartenNr": kartenNr, "kontoNr": kontoNr, "kundenNr": kundenNr})

    values = [
        f"({c['PIN']}, {c['kartenNr']}, {c['kontoNr']}, {c['kundenNr']})"
        for c in karten
    ]
    sql_parts.append(f"INSERT INTO {t_karten} (PIN, kartenNr, kontoNr, kundenNr) VALUES\n  " + ",\n  ".join(values) + ";\n")


    ueberweisungen = []

    for i in range(1, NUM_UEBERWEISUNGEN + 1):
        kontoNrS, kontoNrE = random.sample(konto_nrs, 2)
        betrag = round(random.uniform(1.0, 2000.0), 2)
        year = 2022
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        datum = year * 10000 + month * 100 + day
        ueberweisungen.append({
            "uNr": i, "betrag": betrag, "datum": datum,
            "kontoNrS": kontoNrS, "kontoNrE": kontoNrE
        })

    values = [
        f"({u['betrag']}, {u['datum']}, {u['uNr']}, {u['kontoNrS']}, {u['kontoNrE']})"
        for u in ueberweisungen
    ]
    sql_parts.append(f"INSERT INTO {t_ueberw} (betrag, datum, uNr, kontoNrS, kontoNrE) VALUES\n  " + ",\n  ".join(values) + ";\n")

    return "\n".join(sql_parts)


def main():
    t_filiale = table_name("filiale")
    t_kunden = table_name("kunden")
    t_mitarbeiter = table_name("mitarbeiter")
    t_besitz = table_name("besitz")
    t_karten = table_name("karten")
    t_ueberw = table_name("ueberweisungen")

    output = []
    output.append("-- Auto-generated SQL test data script\n")
    output.append(f"DROP TABLE IF EXISTS {t_karten};")
    output.append(f"DROP TABLE IF EXISTS {t_ueberw};")
    output.append(f"DROP TABLE IF EXISTS {t_besitz};")
    output.append(f"DROP TABLE IF EXISTS {t_mitarbeiter};")
    output.append(f"DROP TABLE IF EXISTS {t_kunden};")
    output.append(f"DROP TABLE IF EXISTS {t_filiale};\n")

    output.append("-- Create tables\n")
    output.append(generate_create_tables_sql())

    output.append("\n-- Insert test data\n")
    output.append(generate_data_and_inserts())

    full_sql = "\n".join(output)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(full_sql)

    print("SQL successfully written to output.txt")


if __name__ == "__main__":
    main()
