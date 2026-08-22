import sqlite3

def create_table(transaction_type):
    conn = sqlite3.connect('User Profiles/Database.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS "Receivers" (
        "UNIQUE ID" INTEGER PRIMARY KEY,
        "NAME" TEXT NOT NULL,
        "AGE" INTEGER NOT NULL,
        "GENDER" TEXT NOT NULL,
        "LAST VISITED" TEXT,
        "BLOOD GROUP" TEXT NOT NULL,
        "CONTACT NUMBER" INTEGER NOT NULL,
        "EMAIL ID" TEXT,
        "HOME ADDRESS" TEXT,
        "PULSE RATE" INTEGER,
        "HEIGHT" REAL,
        "WEIGHT" REAL,
        "RESTRICTIONS" TEXT,
        "CONSUMPTIONS" TEXT,
        "FEMININE" TEXT,
        "PHOTO" BLOB
    );''')
    conn.commit()
    conn.close()
    print("Table created successfully!")


# if __name__ == "__main__":
#     create_table("Donors")
#     create_table("Receivers")
