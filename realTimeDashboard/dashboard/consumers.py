import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .domain.data_domain import DataDomain


class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'dashboard'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        initial_data = list(DataDomain.get_all().values())
        self.send_dash_data(initial_data)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None):
        if text_data:
            form_data = json.loads(text_data)
            label = form_data['label']
            value = form_data['value']

            DataDomain.add_or_update(label, value)

            updated_data = list(DataDomain.get_all().values())
            self.send_dash_data(updated_data)

    def send_dash_data(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'update_dashboard',
                'data': data
            }
        )

    def update_dashboard(self, event):
        updated_data = event['data']
        self.send(text_data=json.dumps({
            'type': 'dash_data',
            'data': updated_data
        }))
