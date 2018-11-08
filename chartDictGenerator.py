import json
from pprint import pprint
from random import randint
import string

# Letters of alphabet
letters = list(string.ascii_uppercase)

chartDict = {}

for i in range(1, 25):
	if i % 2 == 0:
		chartType = "col"
	else:
		chartType = "bar"

	if i <= 8:
		data = [{"Name": letters[i], "Value": randint(1,101)} for i in range(3)]
		chartDict[i] = {"type": chartType, "data": data}

	if i > 8 and i <= 16:
		data = [{"Name": letters[i], "Value": randint(1,101)} for i in range(5)]
		chartDict[i] = {"type": chartType, "data": data}

	if i > 16 and i <= 24:
		data = [{"Name": letters[i], "Value": randint(1,101)} for i in range(8)]
		chartDict[i] = {"type": chartType, "data": data}	


with open('chartDict.py','w') as file:
	file.write("chartDict = "+str(chartDict))

pprint(chartDict)