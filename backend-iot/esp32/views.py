from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import json
from .models import *
import jwt
from datetime import datetime
from security import Bcrypt
from backend_weather_iot.base_view import BaseView
from backend_weather_iot.settings import Pagination
from django.db import connection

# Create your views here.

class DataDrive(BaseView):
    def get(self, request: HttpRequest):
        access_token = request.headers['Authorization'].split(' ')[1]
        if jwt.valid_token(access_token) == False:
            res = json.dumps({
                "statusCode": 401,
                "message": "Unauthorize!"
            })
            return HttpResponse(res, content_type='application/json', status=401)
        
        cursor = connection.cursor()
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')
        page = Pagination.get('CURRENT_PAGE') if request.GET.get('page') == None else int(request.GET.get('page'))
        item_in_page = Pagination.get('ITEM_IN_PAGE') if request.GET.get('iip') == None else int(request.GET.get('iip'))
        pages_in_webview = Pagination.get('PAGES_IN_WEBVIEW') if request.GET.get('piwv') == None else int(request.GET.get('piwv'))
        totalRecords = None
        
        if start_date == None and end_date != None:
            res = json.dumps({
                "statusCode": 400,
                "message": "Start date is not null"
            })
            
            return HttpResponse(res, content_type='application/json', status=400)
        
        if start_date != None and end_date == None:
            res = json.dumps({
                "statusCode": 400,
                "message": "End date is not null"
            })
            
            return HttpResponse(res, content_type='application/json', status=400)
        
        if start_date != None and end_date != None:
            try:
                year, month, day = start_date.split('T')[0].split('-')
                hour, minute, = start_date.split('T')[1].split(':')
                datetime(int(year), int(month), int(day), int(hour), int(minute))
            except Exception as error:
                res = json.dumps({
                    "statusCode": 400,
                    "message": f"Start date param is wrong format: {error}"
                })        
                return HttpResponse(res, content_type='application/json', status=400)
            
            try:
                year, month, day = end_date.split('T')[0].split('-')
                hour, minute, = end_date.split('T')[1].split(':')
                datetime(int(year), int(month), int(day), int(hour), int(minute))
            except Exception as error:
                res = json.dumps({
                    "statusCode": 400,
                    "message": f"End date param is wrong format: {error}"
                })        
                return HttpResponse(res, content_type='application/json', status=400)
            
            start_date = f"{start_date.split('T')[0]} {start_date.split('T')[1]}:00.000000"
            end_date = f"{end_date.split('T')[0]} {end_date.split('T')[1]}:59.999999"
            
            if datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f'):
                res = json.dumps({
                    "statusCode": 400,
                    "message": "Start date not great than End date"
                })        
                return HttpResponse(res, content_type='application/json', status=400)
            
            cursor.execute(
                f"select * from esp32_data where sent_at >= %s  and sent_at <= %s order by sent_at desc offset {(page - 1) * item_in_page} limit {item_in_page}",
                [f"{start_date}", f"{end_date}"]
            )
            records = cursor.fetchall()
            
            cursor.execute(
                "select count(*) as total from esp32_data where sent_at >= %s  and sent_at <= %s",
                [f"{start_date}", f"{end_date}"]
            )
            totalRecords = cursor.fetchone()[0]
        
        if start_date == None and end_date == None:
            cursor.execute(
                f"select * from esp32_data order by sent_at desc offset {(page - 1) * item_in_page} limit {item_in_page}"
            )
            records = cursor.fetchall()
            
            cursor.execute(
                "select count(*) as total from esp32_data"
            )
            totalRecords = cursor.fetchone()[0]
        
        data = []
        index = 1
        for item in records:
            data.append({
                "STT": index,
                "nhietDo": item[1],
                "doAmKhongKhi": item[2],
                "anhSang": item[3],
                "doAmDat": item[4],
                "sentAt": item[5].strftime("%d-%m-%Y %H:%M:%S")
            })
            index += 1
        
        totalPages = totalRecords // item_in_page if totalRecords % item_in_page == 0 else totalRecords // item_in_page + 1
        start_page = page - (page % pages_in_webview if page % pages_in_webview != 0 else pages_in_webview) + 1
        end_page = start_page + pages_in_webview - 1 if start_page + pages_in_webview - 1 <= totalPages else totalPages

        res = json.dumps({
            "dataOfPage": list(data),
            "totalRecords": totalRecords,
            "totalPages": totalPages,
            "startPage": start_page,
            "endPage": end_page
        })
        return HttpResponse(res, content_type='application/json', status=200)
