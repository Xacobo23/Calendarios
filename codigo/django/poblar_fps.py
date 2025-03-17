import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from fp.models import FP, FPType

def generate_unique_codes (count):
    return random.sample(range(1000, 9999), count)

def create_fps ():
    fps = [
        {"name": "Ciclo Superior en Desarrollo de Aplicaciones Web Ordinal", "short_name": "Desarrollo de Aplicaciones Web", "fp_type": FPType.SUPERIOR.name, "duration": 2, "initials": "DAW"},
        {"name": "Ciclo Superior en Desarrollo de Aplicaciones Multiplataforma Ordinal", "short_name": "Desarrollo de Aplicaciones Multiplataforma", "fp_type": FPType.SUPERIOR.name, "duration": 2, "initials": "DAM"},
        {"name": "Ciclo Superior en Administración de Sistemas Informáticos en Red Ordinal", "short_name": "Administración de Sistemas Informáticos en Red", "fp_type": FPType.SUPERIOR.name, "duration": 2, "initials": "ASIR"},
        {"name": "Ciclo Medio en Administración de Sistemas Microinformáticos y Redes Ordinal", "short_name": "Administración de Sistemas Microinformáticos y Redes", "fp_type": FPType.MEDIO.name, "duration": 2, "initials": "SMR"},
        {"name": "Curso de Especialización en Big Data e Inteligencia Artificial Ordinal", "short_name": "Big Data e Inteligencia Artificial", "fp_type": FPType.CURSO_ESPECIALIZACION.name, "duration": 1, "initials": "CEBDIA"},
        {"name": "Curso de Especialización en Ciberseguridad en Entornos de las Tecnologías de la Información Ordinal", "short_name": "Ciberseguridad en Entornos de las Tecnologías de la Información", "fp_type": FPType.CURSO_ESPECIALIZACION.name, "duration": 1, "initials": "CECETI"},
    ]

    codes = generate_unique_codes(len(fps))

    fp_instances = [
        FP(
            code=str(codes[i]),
            name=fp["name"],
            description=f"Descripción del ciclo {fp['name']}",
            fp_type=fp["fp_type"],
            short_name=fp["short_name"],
            duration=fp["duration"],
            initials=fp["initials"]
        )
        for i, fp in enumerate(fps)
    ]

    FP.objects.bulk_create(fp_instances)
    print(f"{len(fps)} FPs creados exitosamente.")

if __name__ == "__main__":
    create_fps()