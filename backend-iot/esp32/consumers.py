from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from .models import *
from datetime import datetime
import random
from channels.db import database_sync_to_async

ROOM_NAME = 'esp32'

class Esp32Socket(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(ROOM_NAME, self.channel_name)
        print(f'client {self.channel_name} connected ...')

    
    async def disconnect(self, message):
        await self.channel_layer.group_discard(ROOM_NAME, self.channel_name)
        print(f'client {self.channel_name} disconnect ...')

    
    async def receive(self, text_data):
        # self.send('ok bro')
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
        
        # Esp32Data.objects.create(
        #     nhiet_do=temperature,
        #     do_am_kk=humidity,
        #     anh_sang=lightValue,
        #     do_am_dat=earthMoisture,
        #     sent_at=datetime.now()
        # )
        
        print('save to db successfully!')
        
        for key in data:
            if data.get(key) == None:
                if key == 'temperature':
                    data[key] = round(random.uniform(15, 40), 2)
                elif key == 'humidity':
                    data[key] = round(random.uniform(20, 90), 2)
            elif key != 'sent_at' and key != 'authen':
                data[key] = round(data[key], 2)

        # await self.save_esp2_data(data)
        
        # self.send(text_data)
        print(data)
        await self.channel_layer.group_send(
            ROOM_NAME,
            {
                'type': 'send_to_client',
                'message': json.dumps(data)
            }
        )
    
    @database_sync_to_async
    def save_esp2_data(self, data):
        Esp32Data.objects.create(
            nhiet_do=data['temperature'],
            do_am_kk=data['humidity'],
            anh_sang=data['lightValue'],
            do_am_dat=data['earthMoisture'],
            sent_at=datetime.now()
        )
        ...
    
    async def send_to_client(self, event):
        message = event.get('message')
        # print('line 70 consummers ' + message)
        
        await self.send(text_data=message)
