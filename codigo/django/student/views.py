from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from student.forms import CustomUserChangeForm
from user.models import CustomUser
from fp.models import FP
from module.models import Enrolled
import xml.etree.ElementTree as ET

User = get_user_model()


def send_welcome_email(student):
    subject = "🎉 Bienvenido a FP Gestor 🎉"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [student.email]

    # Mensaje en texto plano (para clientes que no soportan HTML)
    text_content = f"""
    Hola {student.first_name},

    ¡Bienvenido a FP Gestor! Tu cuenta ha sido creada con éxito.

    📌 Tus credenciales de acceso:
    - Usuario: {student.username}
    - Contraseña: abc123. (Por favor, cámbiala tras iniciar sesión)

    🔗 Accede aquí: http://localhost:8000

    Atentamente,
    El equipo de FP Gestor
    """

    # Mensaje en HTML con estilos
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
            <h2 style="color: #2c3e50; text-align: center;">🎉 Bienvenido a FP Gestor 🎉</h2>
            <p>Hola <strong>{student.first_name}</strong>,</p>
            <p>¡Tu cuenta ha sido creada con éxito! Aquí están tus credenciales de acceso:</p>
            <ul>
                <li><strong>Usuario:</strong> {student.username}</li>
                <li><strong>Contraseña:</strong> <span style="color: red;">abc123.</span> (Por favor, cámbiala tras iniciar sesión)</li>
            </ul>
            <p>Puedes acceder a la plataforma desde el siguiente enlace:</p>
            <p style="text-align: center;">
                <a href="https://fpgestor.com/login" style="background-color: #3498db; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">🔗 Iniciar sesión</a>
            </p>
            <p>Atentamente,<br>El equipo de FP Gestor</p>
        </div>
    </body>
    </html>
    """

    # Crear el correo con texto plano y HTML
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_restore_password_email(student):
    subject = "🎉 Contraseña restablecida 🎉"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [student.email]

    # Mensaje en texto plano (para clientes que no soportan HTML)
    text_content = f"""
    Hola {student.first_name},

    Su contraseña ha sido restablecida con éxito. Más abajo se muestra su nueva contraseña.

    📌 Tus credenciales de acceso:
    - Usuario: {student.username}
    - Contraseña: abc123. (Por favor, cámbiala tras iniciar sesión)

    🔗 Accede aquí: http://localhost:8000

    Atentamente,
    El equipo de FP Gestor
    """

    # Mensaje en HTML con estilos
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
            <h2 style="color: #2c3e50; text-align: center;">🎉 Bienvenido a FP Gestor 🎉</h2>
            <p>Hola <strong>{student.first_name}</strong>,</p>
            <p>Su contraseña ha sido restablecida con éxito. Más abajo se muestra su nueva contraseña.</p>
            <ul>
                <li><strong>Usuario:</strong> {student.username}</li>
                <li><strong>Contraseña:</strong> <span style="color: red;">abc123.</span> (Por favor, cámbiala tras iniciar sesión)</li>
            </ul>
            <p>Puedes acceder a la plataforma desde el siguiente enlace:</p>
            <p style="text-align: center;">
                <a href="https://fpgestor.com/login" style="background-color: #3498db; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">🔗 Iniciar sesión</a>
            </p>
            <p>Atentamente,<br>El equipo de FP Gestor</p>
        </div>
    </body>
    </html>
    """

    # Crear el correo con texto plano y HTML
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()

# Vista de Administrador para listar los estudiantes.
def student_list(request):
    # Obtiene los usuarios que no son superusuarios.
    students = User.objects.filter(is_superuser=False).values(
        "id", "dni", "phone", "username", "email", "first_name", "last_name"
    )

    total_students = students.count()

    data = {
        "title": "Alumnos",
        "shortTitle": "estudiante",
        "students": students,
        "totalStudents": total_students,
    }

    return render(request, "student_list.html", data)



def student_add(request):
    if request.method == "POST":
        print("¡Es POST!")  # <-- Verifica si esto aparece en la consola
    else:
        print("No es POST")
        request.method = "POST"  # <-- Cambia el método de la solicitud a POST

    form = CustomUserChangeForm(request.POST or None, request.FILES or None)  # Asegúrate de que request.FILES esté incluido.
    if request.method == "POST":
        # Primero, comprobamos si se ha subido un archivo XML
        if request.FILES:

            xml_file = request.FILES['xml_file']

            try:
                # Intentamos parsear el archivo XML
                tree = ET.parse(xml_file)
                root = tree.getroot()


                # Iteramos sobre los elementos <Alumno> dentro de <Alumnos>
                for alumno_elem in root.find('Alumnos').findall('Alumno'):
                    # Extraemos los datos de cada alumno
                    username = alumno_elem.find('ID').text  # El ID del alumno se usa como nombre de usuario
                    email = alumno_elem.find('Email').text
                    dni = alumno_elem.find('DNI').text
                    phone = alumno_elem.find('Telefono').text
                    first_name = alumno_elem.find('Nombre').text
                    last_name = alumno_elem.find('Apellido').text
                    

                    # Creamos un nuevo objeto CustomUser con los datos del alumno
                    student = CustomUser(
                        username=username,
                        email=email,
                        dni=dni,
                        phone=phone,
                        first_name=first_name,
                        last_name=last_name,
                    )

                    student.set_password('abc123.')  # Asigna una contraseña predeterminada
                    student.save()

                messages.success(request, "Estudiantes añadidos correctamente desde el XML.")
                return redirect("student_list")

            except ET.ParseError as e:
                # Si hay un error en el parseo del XML, lo mostramos
                messages.error(request, "Error al procesar el archivo XML.")
                return redirect("student_add")

        # Si no se sube un archivo XML, procesamos el formulario manual
        elif form.is_valid():
            student = form.save(commit=False)
            student.set_password('abc123.')  # Asigna una contraseña predeterminada
            student.save()

            messages.success(request, "Estudiante añadido correctamente.")

            send_welcome_email(student)

            return redirect("student_list")
        else:
            messages.error(request, "Error al añadir el estudiante.")

    # Si no es un POST o si el formulario no es válido, simplemente cargamos la página
    data = {
        "title": "Añadir Estudiante",
        "form": form,
        "type": "Alumnos",
        "identifier": 'Nuevo',
        'id': '-'
    }

    return render(request, "student_add.html", data)



def student_edit(request, student_id):
    student = get_object_or_404(get_user_model(), id=student_id)
    fps = FP.objects.filter(modulos__enrolled__student=student).distinct()

    dni = student.dni

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=student)  
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Estudiante actualizado correctamente.')
            return redirect("student_list")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Error en el campo {field.label}: {error}")
            messages.error(request, "Error al actualizar el estudiante.")
    else:
        form = CustomUserChangeForm(
            instance=student,
            initial={
                "apel1": student.last_name.split()[0] if student.last_name else "",
                "apel2": student.last_name.split()[1] if len(student.last_name.split()) > 1 else "",
                "loginEmail": student.username,
            },
        )

    data = {
        "title": "Editar Estudiante",
        "type": "Alumnos",
        "form": form,
        "student_id": student_id,
        'dni': dni,
        'fps': fps
    }
    return render(request, "student_edit.html", data)

@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        student = get_object_or_404(CustomUser, id=student_id)

        student.delete()

        return redirect('student_list')
    
    return redirect('student_list')

@csrf_exempt
def restore_password(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(get_user_model(), id=student_id)
        
        student.set_password('abc123.')
        student.restart_password = True
        student.save()

        messages.success(request, f'La contraseña de {student.username} ha sido restablecida con éxito!')

        send_restore_password_email(student)

        return redirect('student_list')

    return redirect('student_list')

def student_fp_edit (request, student_id, fp_id):
    student = get_object_or_404(get_user_model(), id=student_id)

    fp_instance = get_object_or_404(FP, id=fp_id)
    asociated_modules = []

    if fp_instance is not None:
        asociated_modules = fp_instance.modulos.all()

    student_dni = student.dni

    data = {
        'title': 'Editar matrícula',
        'student_dni': student_dni,
        'fp': fp_instance,
        'student': student,
        'modules': asociated_modules
    }

    return render(request, 'student_fp_edit.html', data)

    
