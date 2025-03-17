import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from classroom.models import Classroom

def create_classrooms (n = 20):
    classrooms = [Classroom(number=i+11) for i in range(n)]
    Classroom.objects.bulk_create(classrooms)
    print(f'{n} aulas creadas exitosamente')

if __name__ == "__main__":
    create_classrooms()