"""
*
* Api for take_out remote
* By Blaise Bromley
*
*
*****must install these libraries*****
*   pip install pyjwt
*   pip install requests
*
"""

from os import access   #this one may be unecessary in python anywhere, idk

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import random, math, time, jwt.utils, requests, json

###########################################################################################
#      Flask API Stuff 
###########################################################################################

app = Flask(__name__)


@app.route("/<button_press>/<password>", methods=["GET"])
def do_stuff(button_press, password):
    with app.app_context():

        button_press = int(button_press)
        if(password == 'Apples123'):
            if(button_press == 5):
                to_return = str(remote_option(random.randint(1,4)))
                return to_return 
            else:
                
                to_return = str(remote_option(button_press))
                return to_return 


@app.route("/check_status/<order_id>", methods=["GET"])
def get_info(order_id):
        with app.app_context():
            return doordash.check_status(order_id)



###########################################################################################
#       Data Classes
###########################################################################################
class Payment_Info():

    name = "Ryan B."
    number = 378282246310005
    ccv = 2273
    billing_address = "518 N. Perry St. Titusville, PA 16354"

    def get_name():
        return Payment_Info.name

    def get_number():
        return Payment_Info.number

    def get_ccv():
        return Payment_Info.ccv

    def get_billing_address():
        return Payment_Info.billing_address


class Delivery_Info():
    
    name = "Ryan B"
    phone_number = "(555) 555-9556"
    address = "Schoenfledt Hall University of Portland, 5000 N. Willamette Dr. Portland OR, 97203"
    
    def get_name():
        return Delivery_Info.name

    def get_phone():
        return Delivery_Info.phone_number

    def get_address():
        return Delivery_Info.address


###########################################################################################
#   Remote Code/Choice Selection
###########################################################################################
def remote_option(id):

    id = int(id)
    
    if(id == 1):
        
        print('in if')
        to_return = order_pizza_hut()
        return to_return

    elif(id == 2):
       
        to_return = order_mcdonalds()
        return to_return
    elif(id ==3):
    
        to_return = order_burger_king()
        return to_return

    elif(id == 4):
       
        to_return = order_taco_bell()
        return to_return



###########################################################################################
#   Specific Orders
###########################################################################################
def order_pizza_hut():
    print('Ordering Pizza Hut')
    
    name = "Pizza Hut"
    address = "5024 Northeast Martin Luther King Junior Boulevard Portland OR"
    phone = "+15032814563"
    instructions = ""

    return doordash.order(address, name, phone, instructions)


def order_mcdonalds():
    print('Ordering McDonalds')

    name = "McDonald's"
    address = "7487 North Ida Avenue Portland OR"
    phone = "+15032893544"
    instructions = "No pickles"

    return doordash.order(address, name, phone, instructions)

def order_burger_king():
    print('Ordering Burger King')
    name = "Burger King"
    address = "11410 Southwest Canyon Road Beavorton OR"
    phone = "+15036266947"
    instructions = ""

    return doordash.order(address, name, phone, instructions)

def order_taco_bell():

    print('Ordering Taco Bell')
    name = "Taco Bell"
    address = "4909 North Lombard Street Portland OR"
    phone = "+15039637965"
    instructions = "Fire Sauce"

    return doordash.order(address, name, phone, instructions)


###########################################################################################
#   Doordash Api Code
#   documentation @: https://developer.doordash.com/en-US/docs/drive/tutorials/get_started
###########################################################################################
class doordash:

    accessKey = {
          "developer_id": "5c1b915b-81e6-477e-9494-03a32e126f6d",
          "key_id": "71157813-141d-46e4-b28c-43adc45a8c18",
          "signing_secret": "vaaIrUwAzFqE2C6yCGyuB3zSGWrKZ4ON4fXdxAoBXm0"
    }
    
    token = jwt.encode(
            {
                "aud": "doordash",
                "iss": accessKey["developer_id"],
                "kid": accessKey["key_id"],
                "exp": str(math.floor(time.time() + 60)),
                "iat": str(math.floor(time.time())),
            },
            jwt.utils.base64url_decode(accessKey["signing_secret"]),
            algorithm="HS256",
            headers={"dd-ver": "DD-JWT-V1"})
    
    endpoint = "https://openapi.doordash.com/drive/v2/deliveries/"
    
    headers = {"Authorization": "Bearer " + token,
                       "Content-Type": "application/json", "Accept-Encoding": "deflate"}


    #create the request body
    def order(b_address, b_name, b_number, b_instructions):
    
        random_bits = random.getrandbits(128)
        delivery_id = "%032x" % random_bits 

        request_body = { 
            "external_delivery_id": delivery_id,
            "pickup_address": b_address,
            "pickup_business_name": b_name,
            "pickup_phone_number": b_number,
            "pickup_instructions": b_instructions,
            "dropoff_address": Delivery_Info.get_address() ,
            "dropoff_business_name": "Ryan's House of Hoes",
            "dropoff_phone_number": Delivery_Info.get_phone(),
            "dropoff_instructions": "Bring to back of the building.",
            }
       
        
        print('Ordering from Doordash...')
        
        #create the delivery
        endpoint = doordash.endpoint
        headers = doordash.headers
        
        #submit the order 
        create_delivery = requests.post(endpoint, headers=headers, json=request_body)
        return request_body["external_delivery_id"] 
       

    #check order standing
    def check_status(order_id):
       
        endpoint = doordash.endpoint
        headers = doordash.headers
        
        #needs try, catch desparately 
        deliver = requests.get(doordash.endpoint + order_id, headers=headers)
        data = json.loads(deliver.text) 
        
        status = data["delivery_status"] 
        eta = data["dropoff_time_estimated"]

        #check if order was created
        if(status == 'arrived_at_dropoff' or status == 'delivered'):
            print('Your order has arrived!')
            return 'Your order has arrived!'
        
        else:
            
            to_return = 'Current Order Status: ' + status + '\nETA: ' + eta + '\n'
            print(to_return)

            return to_return 


app.run(debug=True)                
