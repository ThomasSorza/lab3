from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
#filtering results pag. imports
from django.core.paginator import Paginator
from django.http import JsonResponse

# Query para buscar un usuario por documento y contraseña
def get_user(document, password):
    try:
        user = None
        if Users.objects.get(document=int(document), password=password) is not None:
            user = Users.objects.get(document=int(document), password=password)
        return user
    except Users.DoesNotExist:
        return None

@api_view(['POST'])
@csrf_exempt
def login(request):
    # Obtener el documento y la contraseña de los datos de la solicitud
    document = request.data.get('document')
    password = request.data.get('password')

    # Utilizar la función get_user para buscar al usuario
    user = get_user(document, password)

    if user is not None:

        # Generar un token de autorización (JSON Web Token)
        refresh = RefreshToken.for_user(user)

        # Obtener el token de acceso (JWT)
        access_token = str(refresh.access_token)

        # Construir una respuesta con el token JWT
        response_data = {
            'access_token': access_token,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        # Si no se encuentra un usuario, responder con un mensaje de error y código 401 (No autorizado)
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def test_token(request):
    return Response({})

#Filtering---------------
def filtering_results(text_to_search):
    try:
        filtered_users = Users.objects.filter(
            first_name__icontains=text_to_search
        ) | Users.objects.filter(
            last_name__icontains=text_to_search
        ) | Users.objects.filter(
            type_document__icontains=text_to_search
        ) | Users.objects.filter(
            document__icontains=text_to_search
        ) | Users.objects.filter(
            birthday_icontains=text_to_search
        ) | Users.objects.filter(
            phone_number__icontains=text_to_search
        ) | Users.objects.filter(
            address__icontains=text_to_search
        )

        serialized_users = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type_document': user.type_document,
            'document': user.document,
            'birthday': user.birthday.strftime('%Y-%m-%d'),
            'phone_number': user.phone_number,
            'is_active': user.is_active,
            'register_date': user.register_date.strftime('%Y-%m-%d %H:%M:%S'),
            'address': user.address,
            'role': user.role.rol_name if user.role else None,
            'user_image': user.user_image,
        } for user in filtered_users]
        
    except Users.DoesNotExist:
        return JsonResponse({'message': 'Usuario no encontrado'}, status=404)

from django.utils.translation import gettext as _
from datetime import date, datetime
import pandas as pd
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from azure.communication.email import EmailClient

def registered_today(xls_content):
    try:
        today = date.today()
        users_today = Users.objects.filter(register_date__date=today)

        data = {
            _('ID'): [user.id for user in users_today],
            _('First Name'): [user.first_name for user in users_today],
            _('Last Name'): [user.last_name for user in users_today],
            _('Type Document'): [user.type_document for user in users_today],
            _('Document'): [user.document for user in users_today],
            _('Birthday'): [user.birthday.strftime('%Y-%m-%d') for user in users_today],
            _('Phone Number'): [user.phone_number for user in users_today],
            _('Is Active'): [user.is_active for user in users_today],
            _('Register Date'): [user.register_date.strftime('%Y-%m-%d %H:%M:%S') for user in users_today],
            _('Address'): [user.address for user in users_today],
            _('Role'): [user.role.rol_name if user.role else None for user in users_today],
            _('Password'): [user.password for user in users_today],
            _('User Image'): [user.user_image for user in users_today],
        }

        df = pd.DataFrame(data)

        df.to_excel(xls_content, index=False, engine='openpyxl')
        xls_content.seek(0)
        return xls_content

    except Exception as ex:
        raise ex

def main():
    try:
        xls_content = BytesIO()
        xls_content = registered_today(xls_content)

        connection_string = "endpoint=https://comms-mails.unitedstates.communication.azure.com/;accesskey=6XK80TBbfIlS5Lb6Tj+o+KYWqrU3SvY394gtqXihEw13FLyWdbXq4HYMjhg2/XwWgc+OFg07C4igjgjNXL0yfQ=="
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@03142165-1801-4965-bae1-42453af8a6c5.azurecomm.net",
            "recipients":  {
                "to": [{"address": "edward.sosa@uptc.edu.co" }],
            },
            "content": {
                "subject": f"USUARIOS CREADOS {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "plainText": "Lista de usuarios el día de hoy",
            },
            "attachments": [{
                "content": xls_content.getvalue(),
                "filename": f"users_today_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }]
        }

        poller = client.begin_send(message)
        result = poller.result()

    except Exception as ex:
        print(ex)
#main()

#TODO: Implementar la función para cambiar la contraseña de un usuario
# debe devolver un código 200 si la contraseña se cambió correctamente (para mostrar en el front )
@api_view(['POST'])
def change_user_img_url(request):
    return Response({})
