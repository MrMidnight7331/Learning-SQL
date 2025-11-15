import random
import math

NUM_FILIALEN = 5
NUM_KONTEN = 50
NUM_BESITZ_ROWS = 80
NUM_MITARBEITER = 30
NUM_KARTEN = 100
NUM_UEBERWEISUNGEN = 200

T_FILIALE = "mm_filiale"
T_KUNDEN = "mm_kunden"
T_MITARBEITER = "mm_mitarbeiter"
T_BESITZ = "mm_besitz"
T_KARTEN = "mm_karten"
T_UEBERW = "mm_ueberweisungen"


def esc(s):
    return s.replace("'", "''")


def generate_create_tables_sql():
    sql = ""

    sql += "CREATE TABLE " + T_FILIALE + " (\n"
    sql += "    FNr     INT PRIMARY KEY,\n"
    sql += "    name    TEXT,\n"
    sql += "    adresse TEXT\n"
    sql += ");\n\n"

    sql += "CREATE TABLE " + T_KUNDEN + " (\n"
    sql += "    kontostand INT,\n"
    sql += "    kontotyp   TEXT,\n"
    sql += "    kontoNr    INT PRIMARY KEY,\n"
    sql += "    FNr        INT,\n"
    sql += "    FOREIGN KEY (FNr) REFERENCES " + T_FILIALE + "(FNr)\n"
    sql += ");\n\n"

    sql += "CREATE TABLE " + T_MITARBEITER + " (\n"
    sql += "    name     TEXT,\n"
    sql += "    gehalt   FLOAT,\n"
    sql += "    MNr      INT PRIMARY KEY,\n"
    sql += "    position TEXT,\n"
    sql += "    FNr      INT,\n"
    sql += "    FOREIGN KEY (FNr) REFERENCES " + T_FILIALE + "(FNr)\n"
    sql += ");\n\n"

    sql += "CREATE TABLE " + T_BESITZ + " (\n"
    sql += "    kontoNr  INT,\n"
    sql += "    kundenNr INT,\n"
    sql += "    PRIMARY KEY (kontoNr, kundenNr),\n"
    sql += "    FOREIGN KEY (kontoNr) REFERENCES " + T_KUNDEN + "(kontoNr)\n"
    sql += ");\n\n"

    sql += "CREATE TABLE " + T_KARTEN + " (\n"
    sql += "    PIN      INT,\n"
    sql += "    kartenNr INT PRIMARY KEY,\n"
    sql += "    kontoNr  INT,\n"
    sql += "    kundenNr INT,\n"
    sql += "    FOREIGN KEY (kontoNr) REFERENCES " + T_KUNDEN + "(kontoNr),\n"
    sql += "    FOREIGN KEY (kontoNr, kundenNr) REFERENCES " + T_BESITZ + "(kontoNr, kundenNr)\n"
    sql += ");\n\n"

    sql += "CREATE TABLE " + T_UEBERW + " (\n"
    sql += "    betrag   FLOAT,\n"
    sql += "    datum    INT,\n"
    sql += "    uNr      INT PRIMARY KEY,\n"
    sql += "    kontoNrS INT,\n"
    sql += "    kontoNrE INT,\n"
    sql += "    FOREIGN KEY (kontoNrS) REFERENCES " + T_KUNDEN + "(kontoNr),\n"
    sql += "    FOREIGN KEY (kontoNrE) REFERENCES " + T_KUNDEN + "(kontoNr)\n"
    sql += ");\n"

    return sql


def generate_data_and_inserts():
    random.seed(42)

    sql = ""

    filialen_fnr = []
    filiale_values = []

    for i in range(1, NUM_FILIALEN + 1):
        fname = "Filiale " + str(i)
        fadr = "Beispielstraße " + str(i) + ", Stadt" + str(i)
        filialen_fnr.append(i)

        value = "(" + str(i) + ", '" + esc(fname) + "', '" + esc(fadr) + "')"
        filiale_values.append(value)

    if len(filiale_values) > 0:
        sql += "INSERT INTO " + T_FILIALE + " (FNr, name, adresse) VALUES\n  "
        sql += ",\n  ".join(filiale_values)
        sql += ";\n\n"

    konten_kontoNr = []
    kunden_values = []

    konto_base = 100000
    kontotypen = ["Giro", "Spar", "Business"]

    for i in range(NUM_KONTEN):
        kontoNr = konto_base + i
        konten_kontoNr.append(kontoNr)

        kontostand = random.randint(-5000, 50000)
        kontotyp = random.choice(kontotypen)
        FNr = random.choice(filialen_fnr)

        value = "(" \
                + str(kontostand) + ", '" \
                + esc(kontotyp) + "', " \
                + str(kontoNr) + ", " \
                + str(FNr) + ")"

        kunden_values.append(value)

    if len(kunden_values) > 0:
        sql += "INSERT INTO " + T_KUNDEN + " (kontostand, kontotyp, kontoNr, FNr) VALUES\n  "
        sql += ",\n  ".join(kunden_values)
        sql += ";\n\n"

    mitarbeiter_values = []
    positions = ["Berater", "Filialleiter", "Kassierer", "Service", "IT"]

    for i in range(1, NUM_MITARBEITER + 1):
        name = "Mitarbeiter " + str(i)
        gehalt = round(random.uniform(2000, 6000), 2)
        position = random.choice(positions)
        FNr = random.choice(filialen_fnr)

        value = "('" + esc(name) + "', " \
                + str(gehalt) + ", " \
                + str(i) + ", '" \
                + esc(position) + "', " \
                + str(FNr) + ")"

        mitarbeiter_values.append(value)

    if len(mitarbeiter_values) > 0:
        sql += "INSERT INTO " + T_MITARBEITER + " (name, gehalt, MNr, position, FNr) VALUES\n  "
        sql += ",\n  ".join(mitarbeiter_values)
        sql += ";\n\n"

    besitz_values = []
    besitz_pairs = []
    used_pairs = set()
    max_kunden_nr = max(1, int(math.ceil(NUM_KONTEN * 1.5)))

    while len(besitz_values) < NUM_BESITZ_ROWS:
        kontoNr = random.choice(konten_kontoNr)
        kundenNr = random.randint(1, max_kunden_nr)
        pair = (kontoNr, kundenNr)

        if pair in used_pairs:
            continue

        used_pairs.add(pair)
        besitz_pairs.append(pair)

        value = "(" + str(kontoNr) + ", " + str(kundenNr) + ")"
        besitz_values.append(value)

    if len(besitz_values) > 0:
        sql += "INSERT INTO " + T_BESITZ + " (kontoNr, kundenNr) VALUES\n  "
        sql += ",\n  ".join(besitz_values)
        sql += ";\n\n"

    karten_values = []
    karten_base = 694200

    for i in range(NUM_KARTEN):
        kartenNr = karten_base + i
        kontoNr, kundenNr = random.choice(besitz_pairs)
        PIN = random.randint(1000, 9999)

        value = "(" + str(PIN) + ", " \
                + str(kartenNr) + ", " \
                + str(kontoNr) + ", " \
                + str(kundenNr) + ")"

        karten_values.append(value)

    if len(karten_values) > 0:
        sql += "INSERT INTO " + T_KARTEN + " (PIN, kartenNr, kontoNr, kundenNr) VALUES\n  "
        sql += ",\n  ".join(karten_values)
        sql += ";\n\n"

    # ---------- Überweisungen ----------
    ueberw_values = []

    for i in range(1, NUM_UEBERWEISUNGEN + 1):
        # zwei verschiedene Konten
        kontoNrS = random.choice(konten_kontoNr)
        kontoNrE = random.choice(konten_kontoNr)
        while kontoNrE == kontoNrS:
            kontoNrE = random.choice(konten_kontoNr)

        betrag = round(random.uniform(1.0, 2000.0), 2)
        year = 2022
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        datum = year * 10000 + month * 100 + day

        value = "(" \
                + str(betrag) + ", " \
                + str(datum) + ", " \
                + str(i) + ", " \
                + str(kontoNrS) + ", " \
                + str(kontoNrE) + ")"

        ueberw_values.append(value)

    if len(ueberw_values) > 0:
        sql += "INSERT INTO " + T_UEBERW + " (betrag, datum, uNr, kontoNrS, kontoNrE) VALUES\n  "
        sql += ",\n  ".join(ueberw_values)
        sql += ";\n\n"

    return sql


def main():
    output = []

    # Drop-Statements
    output.append("-- Auto-generated SQL test data script\n")
    output.append("DROP TABLE IF EXISTS " + T_KARTEN + ";")
    output.append("DROP TABLE IF EXISTS " + T_UEBERW + ";")
    output.append("DROP TABLE IF EXISTS " + T_BESITZ + ";")
    output.append("DROP TABLE IF EXISTS " + T_MITARBEITER + ";")
    output.append("DROP TABLE IF EXISTS " + T_KUNDEN + ";")
    output.append("DROP TABLE IF EXISTS " + T_FILIALE + ";\n")

    # Create Tables
    output.append("-- Create tables\n")
    output.append(generate_create_tables_sql())

    # Insert-Daten
    output.append("\n-- Insert test data\n")
    output.append(generate_data_and_inserts())

    full_sql = "\n".join(output)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(full_sql)

    print("SQL successfully written to output.txt")


if __name__ == "__main__":
    main()
