import sqlite3

conn = sqlite3.connect("db.sqlite3")  
cursor = conn.cursor()

datos = [
    ("FP001", "FP Administración", "Gestión empresarial", "MEDIO", "Admin", 24, "ADM"),
    ("FP002", "FP Informática", "Desarrollo de software", "SUPERIOR", "Info", 36, "INF"),
    ("FP003", "FP Electricidad", "Instalaciones eléctricas", "BASICO", "Elect", 12, "ELE"),
]

cursor.executemany(
    "INSERT INTO fp_fp (code, name, description, fp_type, short_name, duration, initials) VALUES (?, ?, ?, ?, ?, ?, ?)", 
    datos
)

conn.commit()
conn.close()
print("Datos insertados en SQLite")
