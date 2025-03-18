import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appHorario.settings")
django.setup()

from fp.models import FP
from module.models import Module

modules_by_fp = {
    "Desarrollo de Aplicaciones Multiplataforma": {
        1: ["Sistemas informáticos", "Bases de datos", "Programación", "Lenguajes de marcas", "Entornos de desarrollo", "FOL"],
        2: ["Acceso a datos", "Desarrollo de interfaces", "Programación multimedia", "Programación de servicios", "Sistemas de gestión", "Proyecto", "Empresa", "FCT"],
    },
    "Desarrollo de Aplicaciones Web": {
        1: ["Sistemas informáticos", "Bases de datos", "Programación", "Lenguajes de marcas", "Entornos de desarrollo", "FOL"],
        2: ["Desarrollo web cliente", "Desarrollo web servidor", "Despliegue web", "Diseño de interfaces", "Proyecto", "Empresa", "FCT"],
    },
    "Administración de Sistemas Informáticos en Red": {
        1: ["Implantación SO", "Planificación redes", "Hardware", "Gestión BD", "Lenguajes de marcas", "FOL"],
        2: ["Administración SO", "Servicios de red", "Aplicaciones web", "Administración BD", "Seguridad", "Proyecto", "Empresa", "FCT"],
    },
    "Ciberseguridad en Entornos de las Tecnologías de la Información": {
        1: ["Fundamentos SO", "Planificación redes", "Gestión BD", "Ciberseguridad", "Legislación", "FOL"],
        2: ["Seguridad sistemas", "Análisis forense", "Hacking ético", "Proyecto", "Empresa", "FCT"],
    },
    "Big Data e Inteligencia Artificial": {
        1: ["Sistemas informáticos", "Bases de datos", "Programación", "Estadística", "Entornos de desarrollo", "FOL"],
        2: ["Big data", "Machine learning", "Procesamiento datos", "Sistemas inteligentes", "Proyecto", "Empresa", "FCT"],
    },
}

color_palette = ["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#A833FF", "#FFC300", "#00CED1"]

def generate_code():
    return ''.join(random.choices("0123456789", k=4))

def create_modules (filename="scripts_sql/poblar_modulos.sql"):
    with open(filename, "w") as f:
        for fp_name, courses in modules_by_fp.items():
            for course, modules in courses.items():
                for module_name in modules:
                    code = generate_code()
                    color = random.choice(color_palette)
                    initials = "".join([word[0] for word in module_name.split()]).upper()
                    sql_line = f"INSERT INTO module_module (code, name, color, initials, course, fp_id) VALUES ('{code}', '{module_name}', '{color}', '{initials}', {course}, (SELECT id FROM fp_fp WHERE short_name='{fp_name}'));\n"
                    f.write(sql_line)

    print("Archivo SQL generado: populate_modules.sql")
    
if __name__ == "__main__":
    create_modules()