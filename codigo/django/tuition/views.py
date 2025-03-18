from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from fp.models import FP
from fp.forms import FPForm
from module.models import Module, Enrolled

from django.http import JsonResponse

import xml.etree.ElementTree as ET
import json

from user.models import CustomUser

def my_tuitions (request):
    user = request.user

    fps = FP.objects.filter(modulos__enrolled__student=user).distinct().prefetch_related('modulos')

    data = {
        'title': 'Mis matrículas',
        'fps': fps
    }

    return render(request, 'my_tuitions.html', data)

def select_tuition (request):
    fps = FP.objects.all()

    data = {
        'title': 'Mis matrículas',
        'subTitle': 'Nueva',
        'fps': fps
    }

    return render(request, 'tuition_select.html', data)

def create_tuition (request, fp_id):
    fp_instance = get_object_or_404(FP, id=fp_id)
    modules = []

    if fp_instance is not None:
        modules = fp_instance.modulos.all()

    data = {
        'title': 'Mis matrículas',
        'subTitle': 'Nueva',
        'modules': modules,
        'fp_id': fp_id
    }

    return render(request, 'tuition_create.html', data)

def review_tuition (request, fp_id):
    fp_instance = get_object_or_404(FP, id=fp_id)
    modules = []

    if fp_instance is not None:
        modules = fp_instance.modulos.all()

    fp_instance = get_object_or_404(FP, id=fp_id)

    form = FPForm(instance=fp_instance)

    data = {
        'title': 'Mis matrículas',
        'subTitle': 'Revisar',
        'modules': modules,
        'form': form,
        'fp_id': fp_id
    }

    return render(request, 'tuition_review.html', data)

@csrf_exempt
def make_tuition (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            module_ids = data.get("modules", [])  
            fp_id = data.get("fp_id")  
            
            if not module_ids:
                return JsonResponse({"success": False, "error": "No se enviaron módulos."}, status=400)

            user = request.user

            for module_id in module_ids:
                module = get_object_or_404(Module, id=module_id)
                Enrolled.objects.get_or_create(student=user, module=module, course=module.course)

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Error en el formato JSON."}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=405)


def tuition_import(request):
    if request.method == "POST" and request.FILES:
        xml_file = request.FILES.get("xml_file")

        if not xml_file:
            return JsonResponse({"success": False, "message": "No se ha seleccionado ningún XML."}, status=400)

        try:
            contenido = xml_file.read().decode("utf-8")
            tree = ET.ElementTree(ET.fromstring(contenido))
            root = tree.getroot()
            
            alumnos_node = root.find("Alumnos")
            if alumnos_node is None:
                return JsonResponse({"success": False, "message": "Estructura XML incorrecta. No se encontró <Alumnos>."}, status=400)

            response_data = {"processed_students": []}
            
            for alumno_elem in alumnos_node.findall("Alumno"):
                student_id = alumno_elem.find("ID").text
                matricula_elem = alumno_elem.find("Matricula")
                ciclo_formativo_elem = matricula_elem.find("CicloFormativo")
                course_name = ciclo_formativo_elem.find("Nombre").text  # Nombre del ciclo formativo
                
                # Verificar si el estudiante existe
                try:
                    student = CustomUser.objects.get(id=student_id)
                except CustomUser.DoesNotExist:
                    continue  # Si no existe, omitir y seguir con el siguiente alumno
                
                enrolled_modules = []
                
                for modulo_elem in ciclo_formativo_elem.findall("Modulo"):
                    module_code = modulo_elem.find("Codigo").text
                    
                    try:
                        module = Module.objects.get(code=module_code)
                    except Module.DoesNotExist:
                        continue  # Si el módulo no existe, omitirlo

                    # Verificar si la matrícula ya existe para evitar duplicados
                    _, created = Enrolled.objects.get_or_create(
                        student=student,
                        module=module,
                        defaults={"course": course_name}
                    )
                    
                    if created:
                        enrolled_modules.append(module_code)
                
                response_data["processed_students"].append({
                    "student_id": student_id,
                    "enrolled_modules": enrolled_modules
                })
                response_data["success"] = True
                
            return JsonResponse(response_data, status=201)

        except ET.ParseError as e:
            return JsonResponse({"success": False, "message": f"Error al procesar el XML: {e}"}, status=400)

    return JsonResponse({"success": False, "message": "No se recibió un archivo válido."}, status=400)
    #     if request.FILES:
    #         xml_file = request.FILES.get('Matriculas')
            
    #         if not xml_file:
    #             return JsonResponse({"error": "No se ha encontrado el archivo XML."}, status=400)
            
    #         try:
    #             xml_content = xml_file.read().decode("utf-8")
    #             print("xml cascadf", xml_content)
    #             tree = ET.ElementTree(ET.fromstring(xml_content))
    #             root = tree.getroot()
                
    #             response_data = {"processed_students": []}
                
    #             for alumno_elem in root.find('Alumnos').findall('Alumno'):
    #                 student_id = alumno_elem.find('ID').text
    #                 matricula_elem = alumno_elem.find('Matricula')
    #                 ciclo_formativo_elem = matricula_elem.find('CicloFormativo')
                    
    #                 try:
    #                     student = CustomUser.objects.get(id=student_id)
    #                 except CustomUser.DoesNotExist:
    #                     return JsonResponse({"error": f"No se ha encontrado el alumno con ID {student_id}."}, status=404)
                    
    #                 enrolled_modules = []
                    
    #                 for modulo_elem in ciclo_formativo_elem.findall('Modulo'):
    #                     module_code = modulo_elem.find('Codigo').text
                        
    #                     try:
    #                         module = Module.objects.get(code=module_code)
    #                     except Module.DoesNotExist:
    #                         return JsonResponse({"error": f"No se ha encontrado el módulo con código {module_code}."}, status=404)
                        
    #                     Enrolled.objects.create(student=student, module=module)
    #                     enrolled_modules.append(module_code)
                    
    #                 response_data["processed_students"].append({
    #                     "student_id": student_id,
    #                     "enrolled_modules": enrolled_modules
    #                 })
                
    #             return JsonResponse(response_data, status=201)
                
    #         except ET.ParseError as e:
    #             return JsonResponse({"error": f"Error al procesar el XML: {e}"}, status=400)
        
    #     return JsonResponse({"error": "No se ha subido ningún archivo XML."}, status=400)
    
    # return JsonResponse({"success": False, "message": "No se recibió un archivo válido."})