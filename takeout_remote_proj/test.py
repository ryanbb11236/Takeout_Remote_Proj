import random, requests, json, sys
from flask import Response

base = 'http://127.0.0.1:5000/'
password = 'Apples123'
rand = random.randint(1,5)

route1 = base + str(rand) + '/' + password 
route2 = base + '/check_status/' 


if(len(sys.argv) > 1):
    #check order
    reply = requests.get(route2 + sys.argv[1]).text

else:
    #make order
    reply = requests.get(route1).text


print(reply)
   


