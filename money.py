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
    sql += "    telefon    VARCHAR(30),\n"
    sql += "    adresse    TEXT,\n"
    sql += "    gebdatum   DATE,\n"
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
    sql += "    kartenNr BIGINT PRIMARY KEY,\n"
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

    # Filialen
    filialen = []
    for i in range(1, NUM_FILIALEN + 1):
        fname = "Filiale " + str(i)
        fadr = "Beispielstraße " + str(i) + ", Stadt" + str(i)
        filialen.append((i, fname, fadr))

    if len(filialen) > 0:
        sql += "INSERT INTO " + T_FILIALE + " (FNr, name, adresse) VALUES\n"
        rows = []
        for f in filialen:
            rows.append("  (%d, '%s', '%s')" % (f[0], esc(f[1]), esc(f[2])))
        sql += ",\n".join(rows) + ";\n\n"

    filialen_fnr = [f[0] for f in filialen]

    # Kunden
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

        telefon = "0151"
        for z in range(7):
            telefon += str(random.randint(0, 9))

        adresse = "Kundenstraße " + str(i + 1) + ", Stadt" + str((i % NUM_FILIALEN) + 1)

        year = random.randint(1950, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        gebdatum = f"{year:04d}-{month:02d}-{day:02d}"

        value = "(" \
                + str(kontostand) + ", '" \
                + esc(kontotyp) + "', " \
                + str(kontoNr) + ", " \
                + str(FNr) + ", '" \
                + esc(telefon) + "', '" \
                + esc(adresse) + "', '" \
                + gebdatum + "')"

        kunden_values.append(value)

    if len(kunden_values) > 0:
        sql += "INSERT INTO " + T_KUNDEN + " (kontostand, kontotyp, kontoNr, FNr, telefon, adresse, gebdatum) VALUES\n  "
        sql += ",\n  ".join(kunden_values)
        sql += ";\n\n"

    # Mitarbeiter
    mitarbeiter = []
    positions = ["Berater", "Filialleiter", "Kassierer", "Service", "IT"]

    for i in range(1, NUM_MITARBEITER + 1):
        name = "Mitarbeiter_" + str(i)
        gehalt = round(random.uniform(2000, 6000), 2)
        position = random.choice(positions)
        FNr = random.choice(filialen_fnr)
        mitarbeiter.append((name, gehalt, i, position, FNr))

    sql += "INSERT INTO " + T_MITARBEITER + " (name, gehalt, MNr, position, FNr) VALUES\n"
    rows = []
    for m in mitarbeiter:
        rows.append("  ('%s', %s, %d, '%s', %d)" %
                    (esc(m[0]), m[1], m[2], esc(m[3]), m[4]))
    sql += ",\n".join(rows) + ";\n\n"

    # Besitz
    besitz = []
    used = set()
    max_kunden_nr = int(math.ceil(NUM_KONTEN * 1.5))

    while len(besitz) < NUM_BESITZ_ROWS:
        # FIX: choose from the list of all konto numbers
        konto = random.choice(konten_kontoNr)
        kunde = random.randint(1, max_kunden_nr)
        key = (konto, kunde)
        if key in used:
            continue
        used.add(key)
        besitz.append(key)

    sql += "INSERT INTO " + T_BESITZ + " (kontoNr, kundenNr) VALUES\n"
    rows = []
    for b in besitz:
        rows.append("  (%d, %d)" % (b[0], b[1]))
    sql += ",\n".join(rows) + ";\n\n"

    # Karten
    karten = []
    karten_base = 53026110134523100  # groß → BIGINT

    for i in range(NUM_KARTEN):
        kartenNr = karten_base + i
        kontoNr, kundenNr = random.choice(besitz)
        PIN = random.randint(1000, 9999)
        karten.append((PIN, kartenNr, kontoNr, kundenNr))

    sql += "INSERT INTO " + T_KARTEN + " (PIN, kartenNr, kontoNr, kundenNr) VALUES\n"
    rows = []
    for c in karten:
        rows.append("  (%d, %d, %d, %d)" % (c[0], c[1], c[2], c[3]))
    sql += ",\n".join(rows) + ";\n\n"

    # Überweisungen
    ueberw = []

    for i in range(1, NUM_UEBERWEISUNGEN + 1):
        # FIX: use konten_kontoNr instead of undefined konto_nrs
        s = random.choice(konten_kontoNr)
        e = random.choice(konten_kontoNr)
        while s == e:
            e = random.choice(konten_kontoNr)
        betrag = round(random.uniform(1.0, 2000.0), 2)
        datum = 20220000 + random.randint(101, 1231)
        ueberw.append((betrag, datum, i, s, e))

    sql += "INSERT INTO " + T_UEBERW + " (betrag, datum, uNr, kontoNrS, kontoNrE) VALUES\n"
    rows = []
    for u in ueberw:
        sql += "  (%s, %d, %d, %d, %d)" % (u[0], u[1], u[2], u[3], u[4])
        if u != ueberw[-1]:
            sql += ",\n"
        else:
            sql += ";\n\n"

    return sql



def main():
    sql = ""

    sql += "-- Auto-generated SQL test data script\n"
    sql += "SET FOREIGN_KEY_CHECKS = 0;\n"
    sql += "DROP TABLE IF EXISTS " + T_KARTEN + ";\n"
    sql += "DROP TABLE IF EXISTS " + T_UEBERW + ";\n"
    sql += "DROP TABLE IF EXISTS " + T_BESITZ + ";\n"
    sql += "DROP TABLE IF EXISTS " + T_MITARBEITER + ";\n"
    sql += "DROP TABLE IF EXISTS " + T_KUNDEN + ";\n"
    sql += "DROP TABLE IF EXISTS " + T_FILIALE + ";\n"
    sql += "SET FOREIGN_KEY_CHECKS = 1;\n\n"

    sql += "-- Create tables\n"
    sql += generate_create_tables_sql()

    sql += "\n-- Insert test data\n"
    sql += generate_data_and_inserts()

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(sql)

    print("SQL successfully written to output.txt")


if __name__ == "__main__":
    main()
