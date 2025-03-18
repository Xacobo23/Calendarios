import os
import django
import random
import string 
from datetime import datetime
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from user.models import CustomUser

NAMES = ["Carlos", "María", "David", "Laura", "Alejandro", "Sofía", "Pablo", "Lucía", "Javier", "Marta"]
LAST_NAMES = ["García", "Fernández", "González", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Díaz"]


ACCENT_MAP = str.maketrans(
    "áéíóúÁÉÍÓÚñÑ",  
    "aeiouAEIOUnN"  
)

def remove_accents(text):
    return text.translate(ACCENT_MAP)

def generate_dni():
    dni_number = str(random.randint(10000000, 99999999))
    dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    letter = dni_letters[int(dni_number) % 23]
    return dni_number + letter

def generate_phone():
    return random.choice(["600", "611", "622", "633", "644", "655", "666", "677", "688", "699"]) + ''.join(random.choices(string.digits, k=6))

def generate_unique_username(name, last_name, existing_usernames):
    year_prefix = "A" + str(random.randint(17, 24))
    last_name_initials = remove_accents(last_name[:2].upper())
    base_username = f"{year_prefix}{remove_accents(name)}{last_name_initials}"
    
    username = base_username
    counter = 1
    
    while username in existing_usernames or CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    existing_usernames.add(username) 
    return username

def create_students (n=500, filename="scripts_sql/poblar_usuarios.sql"):
    users_instances = []
    existing_usernames = set(CustomUser.objects.values_list("username", flat=True))  
    default_password = make_password("abc123.")  
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for _ in range(500):
        name = random.choice(NAMES)
        last_name = random.choice(LAST_NAMES)
        dni = generate_dni()
        phone = generate_phone()
        username = generate_unique_username(name, last_name, existing_usernames)
        email = f"{username}@iessanclemente.net"

        sql_line = f"INSERT INTO user_customuser (username, first_name, last_name, dni, phone, email, restart_password, is_superuser, is_staff, is_active, date_joined, password) " \
                f"VALUES ('{username}', '{name}', '{last_name}', '{dni}', '{phone}', '{email}', 1, 0, 0, 1, '{current_datetime}', '{default_password}');\n"

        users_instances.append(sql_line)

    with open(filename, "w") as f:
        f.writelines(users_instances)

    print("Archivo SQL generado: populate_users.sql")

if __name__ == "__main__":
    create_students()