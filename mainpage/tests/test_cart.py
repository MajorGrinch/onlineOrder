from django.test import TestCase, Client
from django.urls import reverse
from mainpage.models import User
from django.core.serializers.json import DjangoJSONEncoder

class CartUtilTest(TestCase):
    def setUp(self):
        self.client = Client(json_encoder=DjangoJSONEncoder)
        self.user = User.objects.create_user(
            'test',
            'test@gmail.com',
            'testpass'
        )
        self.client.force_login(self.user)

    def test_sync_cart_to_server(self):
        url = reverse('mainpage:syncCart')
        cart = '{"restaurant-1":{"id":"restaurant-1","name":"webster wok","iteminfo_list":{"menu-7":{"price":8,"title":"mushroom qing cai","image":"menu_item/mushroom_qingcai.jpg","quantity":1}},"delivering_fee":7,"subtotal":15}}'
        payload = {'cart': cart}
        rsp = self.client.post(url, data=payload)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.content, b'1')
        self.user.refresh_from_db()
        self.assertEqual(self.user.cart_text, cart)

    def test_sync_cart_from_server(self):
        url = reverse('mainpage:syncCart')
        cart = '{"restaurant-1":{"id":"restaurant-1","name":"webster wok","iteminfo_list":{"menu-7":{"price":8,"title":"mushroom qing cai","image":"menu_item/mushroom_qingcai.jpg","quantity":1}},"delivering_fee":7,"subtotal":15}}'
        self.user.cart_text = cart
        self.user.save()
        rsp = self.client.get(url)
        print(rsp.content)
        self.assertEqual(rsp.content.decode(), cart)
