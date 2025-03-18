import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from classroom.models import Classroom

def create_classrooms (n = 20, filename="scripts_sql/poblar_clases.sql"):
    with open(filename, "w") as f:
        for i in range(20):
            f.write(f"INSERT INTO classroom_classroom (number) VALUES ({i+11});\n")

    print("Archivo SQL generado: populate_classrooms.sql")

if __name__ == "__main__":
    create_classrooms()