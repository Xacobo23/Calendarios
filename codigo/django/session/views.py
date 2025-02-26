import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Session
from module.models import Module
from classroom.models import Classroom
from django.views.decorators.http import require_POST

#FUCKKKK hai que meterlle unha clase, diria de indicar a clase no modulo e pista

@csrf_exempt  # This decorator disables CSRF protection for this view, typically used for API calls
@require_POST  # Ensures only POST requests are handled
def add_sessions(request):
    try:
        # Parse the incoming JSON data
        session_data = json.loads(request.body)

        # Start a transaction to ensure atomicity
        with transaction.atomic():
            # Loop through each session entry in the JSON data
            for session_key, data in session_data.items():
                # Extract the data from the JSON object
                module_id = data.get('moduleId')
                position = data.get('position')
                session_id = data.get('sessionId')  # This can be null, which means create a new session
                day = data.get('day')
                classroom_id = data.get('classRoomId') #pode ser null tamen

                if module_id is None:
                    # If moduleId is null, we need to delete the session if sessionId is provided
                    if session_id:
                        try:
                            session = Session.objects.get(id=session_id)
                            session.delete()  # Delete the session
                        except Session.DoesNotExist:
                            return JsonResponse({"error": f"Session with ID {session_id} not found"}, status=400)
                    else:
                        return JsonResponse({"error": "Module ID is null, but no session ID provided to delete"}, status=400)
                else:
                    # If module_id exists, proceed with creating or updating the session
                    try:
                        module = Module.objects.get(id=module_id)
                    except Module.DoesNotExist:
                        return JsonResponse({"error": f"Module with ID {module_id} does not exist"}, status=400)

                    if classroom_id:
                        try:
                            classroom = Classroom.objects.get(id=classroom_id)
                        except Classroom.DoesNotExist:
                            return JsonResponse({"error": f"Classroom with ID {classroom_id} does not exist"}, status=400)
                    else:
                        classroom = None

                    if session_id:
                        # If session_id exists, update the session
                        try:
                            session = Session.objects.get(id=session_id)
                            session.module = module
                            session.position = position
                            session.week_day = day
                            session.class_id = classroom
                            session.save()
                        except Session.DoesNotExist:
                            return JsonResponse({"error": f"Session with ID {session_id} not found"}, status=400)
                    else:
                        # If session_id is null, create a new session
                        new_session = Session(
                            module=module,
                            position=position,
                            week_day=day,
                            class_id=classroom
                        )
                        new_session.save()

            # If no errors occur, commit the transaction
            return JsonResponse({"success": "Sessions updated/created successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
