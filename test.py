import ibisense
from ibisense.models import DataPoint, Sensor, Channel

import datetime

ibisense.api.set_api_key("635137e5a8bec2eecf06de10df28f6890e4d35194a1b9e59beb728997aad1c26")
#dataset = ibisense.DataPoints.get("hqlu58rd", "2013-01-20T19:20:30.45Z", "2013-05-21T19:20:30.45Z", "avg", "12h", "Europe/Helsinki")
dataset = ibisense.DataPoints.get("hqlu58rd", 1358709630.45, 1369164030.45, "avg", "12h", "Europe/Helsinki")

print dataset.summary
for dp in dataset.datapoints:
	print dp.t, dp.v

sensors = ibisense.Sensors.list()

for s in sensors:
	print s.toJson()

#sensor = ibisense.Sensors.get("MfE3BluU")

#print sensor.toJson()

channel = ibisense.Channels.get("hqlu58rd")

print channel.toJson()

#datapoints = []
#current_datetime = datetime.datetime.now()

#datapoints.append(DataPoint(jsonObj = {"t": current_datetime, "v": 1}))

#sensor = Sensor(name="python_test_sensor")
#print sensor.toJson()
#sensor = ibisense.Sensors.add(sensor)
#print sensor.toJson()

#channel = Channel(name="python_test_channel")
#channel = ibisense.Channels.add(sensor.SUID, channel)

#print channel.toJson()

#print channel.CUID

#for d in datapoints:
#	print d.toJson()

#ibisense.DataPoints.add("mYKrRdWB", datapoints)
