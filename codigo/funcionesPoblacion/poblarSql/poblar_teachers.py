import os
import django
import random
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from module.models import Module
from teacher.models import Teacher, TeacherModule

NAMES = ["Carlos", "María", "David", "Laura", "Alejandro", "Sofía", "Pablo", "Lucía", "Javier", "Marta", "JoseMaría", "Noemí", "Luis"]
LAST_NAMES = ["García", "Fernández", "González", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Díaz", "Calo", "Varela"]

ACCENT_MAP = str.maketrans(
    "áéíóúÁÉÍÓÚñÑ",  
    "aeiouAEIOUnN"   
)

def remove_accents(text):
    return text.translate(ACCENT_MAP)

def generate_dni ():
    dni_number = str(random.randint(10000000, 99999999))
    dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    letter = dni_letters[int(dni_number) % 23]
    return dni_number + letter

def generate_phone ():
    return random.choice(["600", "611", "622", "633", "644", "655", "666", "677", "688", "699"]) + ''.join(random.choices(string.digits, k=6))

def generate_email (name, last_name):
    return f'{remove_accents(name).lower()}{remove_accents(last_name).lower()}@iessanclemente.net'

def create_teachers(n=100, filename="scripts_sql/poblar_profesores.sql"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("BEGIN TRANSACTION;\n")
        
        for _ in range(n):
            name = random.choice(NAMES)
            last_name = random.choice(LAST_NAMES)
            dni = generate_dni()
            phone = generate_phone()
            email = generate_email(name, last_name)

            sql = f"INSERT INTO teacher_teacher (name, last_name, dni, phone, email) VALUES ('{name}', '{last_name}', '{dni}', '{phone}', '{email}');\n"
            f.write(sql)

        f.write("COMMIT;\n")

    print(f"Archivo {filename} generado con {n} profesores.")

if __name__ == "__main__":
    create_teachers()