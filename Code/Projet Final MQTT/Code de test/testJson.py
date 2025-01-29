import json

print("{timestamp:1730993154,NomEsp32:enigmeTest1,JsonData:{sw1:1,sw2:0,btn1:0}}")
print(json.loads('{"timestamp":1730993154,"NomEsp32":"enigmeTest1","JsonData":{"sw1":1,"sw2":0,"btn1":0}}'))