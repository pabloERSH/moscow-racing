import json
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Avg
from asgiref.sync import async_to_sync
from .models import Cars, Rates


class RatingConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'ratings'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        if self.scope["user"].is_authenticated:
            text_data_json = json.loads(text_data)
            value = text_data_json['userRating']
            car_id = text_data_json['carId']

            car = Cars.objects.get(id=car_id)
            user = self.scope["user"]
            if Rates.objects.filter(car=car, user=user).exists():
                Rates.objects.filter(car=car, user=user).update(rate=value)
            else:
                new_rate = Rates.objects.create(rate=value, user=user, car=car)
                new_rate.save()

            avg_sum = Rates.objects.filter(car=car).aggregate(Avg('rate'))['rate__avg']
            cnt = Rates.objects.filter(car=car).count()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'newRating': round(avg_sum, 2),
                    'newCount': cnt,
                    'carId': car_id,
                    'type': 'click_rating'
                }
            )
        else:
            self.send(text_data=json.dumps({
                'message': 'Чтобы оставить отзыв, нужно авторизироваться!!!',
                'type': 'error'
            }))

    def click_rating(self, event):
        newrating = event['newRating']
        newcount = event['newCount']
        car_id = event['carId']
        self.send(text_data=json.dumps({
            'newRating': newrating,
            'newCount': newcount,
            'carId': car_id,
            'type': 'rating'
        }))
