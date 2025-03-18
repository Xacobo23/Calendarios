import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from poblar_classrom import create_classrooms
from poblar_fps import create_fps
from poblar_modules import create_modules
from poblar_students import create_students
from poblar_teachers import create_teachers

def main ():
    print("Creando clases...")
    create_classrooms()

    print("Creando FPs...")
    create_fps()

    print("Creando módulos...")
    create_modules()

    print("Creando estudiantes...")
    create_students()

    print("Creando profesores...")
    create_teachers()

if __name__ == "__main__":
    main()