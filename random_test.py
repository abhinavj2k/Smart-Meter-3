import requests
import math
url='https://capstone-smart-meter.herokuapp.com/val'
while True:
    headers={
      "RECIEVE TIME STAMP":"22",
      "VOLTAGE":"22",
      "CURRENT":"22",
      "PHASE ANGLE":"22",
      "POWER FACTOR":"22",
      "FREQUENCY":"22",
      "POWER":"22",
      "ENERGY":"22",
      "TARIFF":"22",
    }

    #payload=open('random_test.py','rb')

    r=requests.post(url,data=headers)
    print(r.status_code,"\n",r.content)
