import json
from pprint import pprint, pformat
from random import randint
import string

# Letters of alphabet
letters = list(string.ascii_uppercase)

chartDict = { 0: {'data': [{'Name': 'A', 'Value': 66},
               {'Name': 'B', 'Value': 77},
               {'Name': 'C', 'Value': 52},
               {'Name': 'D', 'Value': 32},
               {'Name': 'E', 'Value': 11}],
      'q1': 1,
      'q2': 5,
      'type': 'bar'}}

for i in range(1, 25, 2):

    if i <= 8:
        q1 = randint(1,3)
        q2 = randint(1,3)
        data = [{"Name": letters[i], "Value": randint(1,100)} for i in range(3)]
        chartDict[i] = {"type": "col", "q1": q1, "q2": q2, "data": data}
        chartDict[i+1] = {"type": "bar", "q1": q1, "q2": q2, "data": data}

    if i > 8 and i <= 16:
        q1 = randint(1, 5)
        q2 = randint(1, 5)
        data = [{"Name": letters[i], "Value": randint(1,100)} for i in range(5)]
        chartDict[i] = {"type": "col", "q1": q1, "q2": q2, "data": data}
        chartDict[i + 1] = {"type": "bar", "q1": q1, "q2": q2, "data": data}

    if i > 16 and i <= 24:
        q1 = randint(1, 8)
        q2 = randint(1, 8)
        data = [{"Name": letters[i], "Value": randint(1,100)} for i in range(8)]
        chartDict[i] = {"type": "col", "q1": q1, "q2": q2, "data": data}
        chartDict[i + 1] = {"type": "bar", "q1": q1, "q2": q2, "data": data}

with open('chartDict.py','w') as file:
    file.write("chartDict = "+str(pformat(chartDict)))

pprint(chartDict)