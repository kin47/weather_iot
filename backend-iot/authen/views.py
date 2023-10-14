from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import json
from .models import *
import jwt
from datetime import datetime
from security import Bcrypt
from backend_weather_iot.base_view import BaseView
import re
from django.core.mail import send_mail
import random
from backend_weather_iot.settings import EMAIL_HOST_USER


def index(request: HttpRequest):
    return render(request, 'authen/index.html')


def getUserFromToken(accessToken: str) -> User:
        user_session = UserSession.objects.filter(access_token=accessToken)
        if len(user_session) == 0:
            return None
        
        return user_session[0].id_user


def valid(regex: str, sample: str) -> bool:
    if sample == None:
        return False

    result = re.findall(regex, sample)
    if len(result) != 1:
        return False
    
    return result[0] == sample


class MissingPassword(BaseView):
    def post(self, request: HttpRequest):
        missingPasswordDTO: dict = json.loads(request.body)
        email = missingPasswordDTO.get('email')
        user = User.objects.filter(email=email)
        if len(user) == 0:
            res = json.dumps({
                "statusCode": 400,
                "message": "Email is not exist!"
            })
            return HttpResponse(res, content_type='application/json', status=400)
        
        user = user[0]
        characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890@#$%^&+='
        newPassword = ''
        for i in range(8):
            newPassword += random.choice(characters)
        
        user.password = Bcrypt.hashpw(newPassword)
        user.save()
        send_mail(
            'Mật khẩu mới từ N17-IoT PTIT',
            f'Mật khẩu mới của bạn là: {newPassword}\nHãy đăng nhập vào hệ thống và đổi lại mật khẩu nhé!',
            EMAIL_HOST_USER,
            [email]
        )
        
        res = json.dumps({
            "statusCode": 200,
            "message": "Sent new password successfully!"
        })
        return HttpResponse(res, content_type='application/json', status=200)


class Logout(BaseView):
    def get(self, request: HttpRequest):
        accessToken = request.headers['Authorization'].split(' ')[1]
        session = UserSession.objects.filter(access_token=accessToken)
        if len(session) == 0:
            res = json.dumps({
                "statusCode": 400,
                "message": "Invalid Token!"
            })
            return HttpResponse(res, content_type='application/json', status=400)
        
        session = session[0]
        session.delete()
        res = json.dumps({
            "statusCode": 200,
            "message": "Logout successfully!"
        })
        return HttpResponse(res, content_type='application/json', status=200)


class Register(BaseView):
    def post(self, request: HttpRequest):
        registerDTO: dict = json.loads(request.body)
        regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        regexPassword = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=])(?=.*[0-9]).{8,}$'
        if valid(regexEmail, registerDTO.get('email')) == False:
            res = json.dumps({
                "statusCode": 400,
                "message": "Wrong Email Format!"
            })
            return HttpResponse(res, content_type='application/json', status=400)

        if valid(regexPassword, registerDTO.get('password')) == False:
            res = json.dumps({
                "statusCode": 400,
                "message": "Wrong Password Format!"
            })
            return HttpResponse(res, content_type='application/json', status=400)
        
        if registerDTO.get('password') != registerDTO.get('confirm-password'):
            res = json.dumps({
                "statusCode": 400,
                "message": "Wrong Confirm Password Format!"
            })
            return HttpResponse(res, content_type='application/json', status=400)
        
        user = User.objects.filter(email=registerDTO.get('email'))
        if len(user) == 1:
            res = json.dumps({
                "statusCode": 400,
                "message": "Email already exists!"
            })
            return HttpResponse(res, content_type='application/json', status=400)
        
        user = User(
            email=registerDTO.get('email'),
            password=Bcrypt.hashpw(registerDTO.get('password')),
            username=registerDTO.get('username'),
            is_admin=False
        )
        user.save()
        
        payload = {
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "iat": round(datetime.now().timestamp()),
            "admin": user.is_admin
        }
        access_token = jwt.generate_token(payload)
        UserSession.objects.create(access_token=access_token, id_user=user)
        res = json.dumps({ "accessToken": access_token })
        return HttpResponse(content=res, content_type='application/json', status=201)


class Login(BaseView):
    def post(self, request: HttpRequest):
        loginDTO = json.loads(request.body)
        user = User.objects.filter(email=loginDTO['email'])
        if len(user) > 0:
            user = user[0]
            if Bcrypt.checkpw(loginDTO['password'], user.password) == True:
                user_session = UserSession.objects.filter(id_user=user.id)
                if len(user_session) > 0:
                    res = json.dumps({
                        "statusCode": 401,
                        "message": "Account is being logged in elsewhere"
                    })
                    return HttpResponse(res, content_type='application/json', status=401)
                
                payload = {
                    "sub": user.id,
                    "email": user.email,
                    "username": user.username,
                    "iat": round(datetime.now().timestamp()),
                    "admin": user.is_admin
                }
                access_token = jwt.generate_token(payload)
                UserSession.objects.create(access_token=access_token, id_user=user)
                res = json.dumps({ "accessToken": access_token })
                return HttpResponse(content=res, content_type='application/json', status=200)
            else:
                res = json.dumps({ "statusCode": 401, "message": 'Password is incorrect' })
                return HttpResponse(content=res, content_type='application/json', status=401)
        else:
            res = json.dumps({ "statusCode": 401, "message": 'Email is not exsist' })
            return HttpResponse(content=res, content_type='application/json', status=401)


class Me(BaseView):
    def get(self, request: HttpRequest):
        accessToken = request.headers['Authorization'].split(' ')[1]
        
        if jwt.valid_token(accessToken) == False:
            return HttpResponse(json.dumps({
                "statusCode": 401,
                "message": "Invalid Token"
            }), content_type='application/json', status=401)
        
        user = getUserFromToken(accessToken)
        if user == None:
            return HttpResponse(json.dumps({
                "statusCode": 401,
                "message": "Information of Token is not correct"
            }), content_type='application/json', status=401)
        
        user_response = {
            "username": user.username,
            "email": user.email
        }
        return HttpResponse(json.dumps(user_response), content_type='application/json', status=200)


class RefreshToken(BaseView):
    def get(self, request: HttpRequest):
        accessToken: str = request.headers['Authorization'].split(' ')[1]
        header, payload, signature = accessToken.split('.')
        signature_correct = jwt.hmacSha256(f'{header}.{payload}')
        if signature != signature_correct:
            return HttpResponse(json.dumps({
                "statusCode": 401,
                "message": "Invalid Token"
            }), content_type='application/json', status=401)
        
        user = getUserFromToken(accessToken)
        if user == None:
            return HttpResponse(json.dumps({
                "statusCode": 401,
                "message": "Information of Token is not correct"
            }), content_type='application/json', status=401)
        
        payload = {
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "iat": round(datetime.now().timestamp()),
            "admin": user.is_admin
        }
        access_token = jwt.generate_token(payload)
        UserSession.objects.update(access_token=access_token, id_user=user)
        res = json.dumps({ "accessToken": access_token })
        return HttpResponse(content=res, content_type='application/json', status=200)