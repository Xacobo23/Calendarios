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

def create_students (n=500):
    users_instances = []
    existing_usernames = set(CustomUser.objects.values_list("username", flat=True))  
    default_password = make_password("abc123.")  

    for _ in range(n):
        name = random.choice(NAMES)
        last_name = random.choice(LAST_NAMES)
        dni = generate_dni()
        phone = generate_phone()
        username = generate_unique_username(name, last_name, existing_usernames)
        email = f"{username}@iessanclemente.net"

        user = CustomUser(
            username=username,
            first_name=name,
            last_name=last_name,
            dni=dni,
            phone=phone,
            email=email,
            restart_password=True,
            is_superuser=False,
            is_staff=False,
            password=default_password  
        )
        
        try:
            user.full_clean()
            users_instances.append(user)
        except Exception as e:
            print(f"Error al validar usuario {username}: {e}")

    CustomUser.objects.bulk_create(users_instances)
    print(f"{len(users_instances)} usuarios creados exitosamente.")

if __name__ == "__main__":
    create_students()