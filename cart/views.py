from multiprocessing import context
from django.shortcuts import render
from rest_framework import generics , permissions , status
from rest_framework.views import APIView
from .serializers import CartSerializer, CartItemSerializer  #TransactionSerializer
from .models import Cart, CartItem , Transaction
from rest_framework.response import Response
from rest_framework.request import Request
import json
import requests
from IPython.display import IFrame



class CartListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartSerializer
    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

class CartItemCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartItemSerializer
    def get_queryset(self):
        queryset = CartItem.objects.filter(cart__user=self.request.user)
        return queryset




class checkout(APIView):

    # PAYMOB STEP 1

    def post(self, request):
        url = "https://accept.paymob.com/api/auth/tokens"

        payload = json.dumps({
            "api_key": "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaU1UWTFPREExTnpjd01pNHdPRGczTVRVaUxDSndjbTltYVd4bFgzQnJJam94TmpReU16UXNJbU5zWVhOeklqb2lUV1Z5WTJoaGJuUWlmUS55M1kyTjluelZ1elFpWkt4Vk8yMjVObHJIbFBrUURHLTBWUnlVMVpRelNPNkJFZzUzbC0tcEowemxUeUt3M3NqMUJYOE14SjkzRjV1cWt6TDFRMXJ0Zw=="
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        token = response.json()['token']
        #######
        data = request.data
        cart_id = data['cart_id']
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
        amount = 0
        for cart_item in cart_items:
            amount += cart_item.product.price * cart_item.quantity
        amount =  Cart.objects.get(user = request.user).total_price * 100
        currency = "EGP"
        shipping_info = {
            "name": data['name'],
            "phone": data['phone'],
            "address": data['address'],
            "city": data['city'],
            "country": data['country'],
            "postal_code": data['postal_code'],
        }

        # PAYMOB step 2 : Order Registration API
        url2 = "https://accept.paymobsolutions.com/api/ecommerce/orders"
        querystring = {"token": token}
        payload = {
            "delivery_needed": True,

            "merchant_id": "164234",
            "amount_cents": amount,
            "currency": currency,
            "items": [],

        }
        headers = {
            'Content-Type': 'application/json'
        }
        modified_payload = json.dumps(payload)
        response = requests.request("POST", url2, headers=headers, data=modified_payload, params=querystring)
        response = response.json()

        # get order id from response
        order_id = response['id']

        
        
        url = "https://accept.paymobsolutions.com/api/acceptance/payment_keys"
        querystring = {"token": token}
        payload = {
            "amount_cents": amount,
            "currency": response['currency'],
            "card_integration_id": 1946955,
            "order_id": order_id,
             "billing_data": {
                "apartment": "803", 
                "email": "claudette09@exa.com", 
                "floor": "42", 
                "first_name": "Clifford", 
                "street": "Ethan Land", 
                "building": "8028", 
                "phone_number": "+86(8)9135210487", 
                "shipping_method": "PKG", 
                "postal_code": "01898", 
                "city": "Jaskolskiburgh", 
                "country": "CR", 
                "last_name": "Nicolas", 
                "state": "Utah"
            }, 
        }
        headers = {
            "content-type": "application/json"
        }
        modified_payload = json.dumps(payload)
        response = requests.post(url, data=modified_payload, headers=headers, params=querystring)
        response = response.json()
        token = response['token']

        

        
        url_iframe = f'https://accept.paymob.com/api/acceptance/iframes/363518?payment_token={token}'
        


        if Response.status_code == 200:
             Transaction.objects.create(
                cart = cart,
                amount = amount,
                order_id = order_id, )

       
        
     

            

        return Response({"iframe": url_iframe , "response " : response}, status=status.HTTP_200_OK ,)





    
            
            
        

  
        



        
    


            




        
    






 

        



