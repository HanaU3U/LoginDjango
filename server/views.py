from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')

def user_detail_page(request):
    return render(request, 'user_detail.html')

#login
@api_view(['POST'])
def login(request):
    #Obtener datos del request
    username = request.data['username']
    password = request.data['password']

    #Existe usuario
    user = get_object_or_404(User, username=username)


    #Validar contraseña
    if user.check_password(password):
        token,created = Token.objects.get_or_create(user=user)

        #Serializar usuario
        userSerialized = UserSerializer(instance=user)

        #Respuesta
        respuesta = {
            "token": token.key,
            "user": userSerialized.data
        }

        #Retornar respuesta
        return Response(respuesta, status=200)

    respuesta = {
        "error": "Contraseña incorrecta"
    }
    return Response(respuesta, status=400)

#home page despues de logearse
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def userDetail(request):

    #Obtener usuario
    user = request.user

    #Serializar usuario
    serializer = UserSerializer(user)

    #Respuesta
    respuesta = {
        "user": serializer.data
    }

    #Retornar respuesta
    return Response(respuesta, status=200)
