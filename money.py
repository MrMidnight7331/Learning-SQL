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

# Predefined lists for name generation
FIRST_NAMES = ["Lena", "Max", "Anna", "Paul", "Laura", "David", "Mia", "Tim", "Nina", "Leo"]
LAST_NAMES = ["Schmidt", "Müller", "Weber", "Schneider", "Fischer", "Meier", "Wolf", "Hoffmann", "Schulz", "Zimmermann"]

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
    sql += "    name       TEXT,\n"  # Added 'name' column for customers
    sql += "    FOREIGN KEY (FNr) REFERENCES " + T_FILIALE + "(FNr)\n"
    sql += ");\n\n"

    # Other table definitions remain the same...

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

        # Randomly generate a full name
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"

        value = "(" \
                + str(kontostand) + ", '" \
                + esc(kontotyp) + "', " \
                + str(kontoNr) + ", " \
                + str(FNr) + ", '" \
                + esc(telefon) + "', '" \
                + esc(adresse) + "', '" \
                + gebdatum + "', '" \
                + esc(full_name) + "')"

        kunden_values.append(value)

    if len(kunden_values) > 0:
        sql += "INSERT INTO " + T_KUNDEN + " (kontostand, kontotyp, kontoNr, FNr, telefon, adresse, gebdatum, name) VALUES\n  "
        sql += ",\n  ".join(kunden_values)
        sql += ";\n\n"

    # Remaining parts (Mitarbeiter, Besitz, Karten, Überweisungen) remain unchanged...
    
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
