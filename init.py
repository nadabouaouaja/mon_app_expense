import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Création de la table "expenses" avec la colonne "name"
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  -- Nouvelle colonne pour le nom de la dépense
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
)
''')

# Insérer quelques données d'exemple avec la colonne "name"
cursor.execute("INSERT INTO expenses (name, category, amount, date) VALUES ('Lunch', 'Food', 15.5, '2025-04-01')")
cursor.execute("INSERT INTO expenses (name, category, amount, date) VALUES ('Bus Ticket', 'Transport', 10, '2025-04-01')")
cursor.execute("INSERT INTO expenses (name, category, amount, date) VALUES ('Movie Night', 'Entertainment', 20, '2025-04-02')")

# Sauvegarder les modifications et fermer la connexion
conn.commit()
conn.close()

print("Base de données et table mises à jour avec succès !")
