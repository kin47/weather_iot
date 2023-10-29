from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from datetime import datetime

class Esp32Socket(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(f'client {self.channel_name} {self.channel_layer} connected ...')

    
    def disconnect(self, message):
        print('client disconnect ...')

    
    def receive(self, text_data):
        # print(text_data)
        data: dict = json.loads(text_data)
        if data.get('authen') == None:
            print('authen failed!')
            return
        
        if data.get('authen') != 'from esp32 N17-IoT':
            print('authen failed!')
            return
        
        data: dict = json.loads(text_data)
        temperature = round(data.get('temperature'), 2) if data.get('temperature') != None else None
        humidity = round(data.get('humidity')) if data.get('humidity') != None else None
        lightValue = round(data.get('lightValue')) if data.get('lightValue') != None else None
        earthMoisture = round(data.get('earthMoisture')) if data.get('earthMoisture') != None else None
        
        print(temperature, humidity, lightValue, earthMoisture)
        # self.save_to_db(temperature, humidity, lightValue, earthMoisture)
        
        Esp32Data.objects.create(
            nhiet_do=temperature,
            do_am_kk=humidity,
            anh_sang=lightValue,
            do_am_dat=earthMoisture,
            sent_at=datetime.now()
        )
        print('save to db successfully!')
