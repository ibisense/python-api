__title__ = 'ibisense-api-python'
__version__ = '0.0.1'

import requests
import urllib
import json

from dateutil import parser
from datetime import date, datetime

from ibisense.models import Sensor, Channel, DataPoint, DataSet


api_key = ""
api_base_url = "https://ibi.io/v1/"

def set_api_key(key):
	global api_key
	api_key = key

class Channels():
	@staticmethod
	def add(suid, channel):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "add/" + api_key + "/sensor/id/" + suid + "/channel/"
		r = requests.post(api_url, data=json.dumps(channel.toJson(), encoding="utf-8"), headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		return Channel(jsonObj = r_json['data'])

	@staticmethod
	def update(suid, channel):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "update/" + api_key + "/sensor/id/" + suid + "/channel/"
		r = requests.post(api_url, data=json.dumps(channel.toJson(), encoding="utf-8"), headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		return Channel(jsonObj = r_json['data'])

	@staticmethod
	def get(cuid):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "get/" + api_key + "/channel/id/" + cuid + "/"
		r = requests.get(api_url)
		r.raise_for_status()
		r_json = json.loads(r.text)
		return Channel(jsonObj = r_json['data'])

	@staticmethod
	def getByAttribute(key, value):
		if not api_key:
			raise ValueError('API key must be set')
		f = {'comparator': 'equal', 'key': key, 'value': value}
		api_url = api_base_url + "get/" + api_key + "/channel/filter/"
		r = requests.post(api_url, data = json.dumps(f, encoding="utf-8"), headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		channels = []
		for c in r_json['data']:
			channel = Channel(jsonObj = c)
			channels.append(channel)
		return channels

	@staticmethod
	def list(suid):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "get/" + api_key + "/sensor/id/" + suid + "/channel/"
		r = requests.get(api_url, headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		channels = []
		for c in r_json['data']:
			channel = Channel(jsonObj = c)
			channels.append(channel)
		return channels

	@staticmethod
	def getSensor(cuid):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "get/" + api_key + "/channel/id/" + cuid + "/sensor/"
		r = requests.get(api_url, headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		sensor = Sensor(jsonObj = r_json['data'])		
		return sensor

	@staticmethod
	def remove(cuid):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "delete/" + api_key + "/channel/id/" + cuid + "/"
		r = requests.get(api_url, headers = {'content-type': 'application/json'})
		r.raise_for_status()
	

class Sensors():
	@staticmethod
	def add(sensor):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "add/" + api_key + "/sensor/id/"
		r = requests.post(api_url, data=json.dumps(sensor.toJson(), encoding="utf-8"), headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		return Sensor(jsonObj = r_json['data'])

	@staticmethod
	def update(sensor):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "update/" + api_key + "/sensor/id/"
		r = requests.post(api_url, data=json.dumps(sensor.toJson(), encoding="utf-8"), headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		return Sensor(jsonObj = r_json['data'])

	@staticmethod
	def get(suid):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "get/" + api_key + "/sensor/id/" + suid + "/"
		r = requests.get(api_url, headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		return Sensor(jsonObj = r_json['data'])

	@staticmethod
	def getByAttribute(key, value):
		if not api_key:
			raise ValueError('API key must be set')
		f = {'comparator': 'equal', 'key': key, 'value': value}
		api_url = api_base_url + "get/" + api_key + "/sensor/filter/"
		r = requests.post(api_url, data = json.dumps(f, encoding="utf-8"), headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		sensors = []
		for s in r_json['data']:
			sensor = Sensor(jsonObj = s)
			sensors.append(sensor)
		return sensors

	@staticmethod
	def getBySerialNumber(serial):
		return

	@staticmethod
	def list():
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "get/" + api_key + "/sensor/"
		r = requests.get(api_url, headers = {'content-type': 'application/json'})
		r.raise_for_status()
		r_json = json.loads(r.text)
		sensors = []
		for s in r_json['data']:
			sensor = Sensor(jsonObj = s)
			sensors.append(sensor)
		return sensors

	@staticmethod
	def remove(suid):
		api_url = api_base_url + "delete/" + api_key + "/sensor/id/" + suid + "/"
		r = requests.get(api_url, headers = {'content-type': 'application/json'})
		r.raise_for_status()

class DataPoints():

	@staticmethod
	def get(cuid, start, end, function = None, interval = None, tz = None):
		if not api_key:
			raise ValueError('API key must be set')
		api_url = api_base_url + "get/" + api_key + "/channel/id/" + cuid + "/data/"
		
		if isinstance(start, (str, unicode)):
			start = parser.parse(start)
		elif isinstance(start, (float, int)):
			start = datetime.fromtimestamp(float(start))
		elif type(start) is  not datetime.date:
			raise TypeError('start must be a datetime.date or a string, not %s' % type(start))

		if isinstance(end, (str, unicode)):
			end = parser.parse(end)
		elif isinstance(end, (float, int)):
			end = datetime.fromtimestamp(float(end))
		elif type(end) is not datetime.date:
			raise TypeError('end must be a datetime.date or a string, not %s' % type(end))

		params = {
			'start': start.isoformat().encode("UTF-8"),
			'end': end.isoformat().encode("UTF-8")
		}

		if function and interval:
			params['function'] = function
			params['interval'] = interval

		if tz:
			params['tz'] = tz

		r = requests.get(api_url, headers = {'content-type': 'application/json'}, params = params)
		
		r.raise_for_status()
		r_json = json.loads(r.text)['data']
		datapoints = []
		for dp in r_json['data']:
			datapoint = DataPoint(jsonObj = dp)
			datapoints.append(datapoint)

		dataset = DataSet(r_json['CUID'], r_json['start'], r_json['end'], r_json['summary'], datapoints)
		return dataset

	@staticmethod
	def add(cuid, datapoints):
		if not api_key:
			raise ValueError('API key must be set')

		api_url = api_base_url + "add/" + api_key + "/channel/id/" + cuid + "/data/"

		r_dps = []
		for datapoint in datapoints:
			r_dps.append(datapoint.toJson())
		r = requests.post(api_url, headers = {'content-type': 'application/json'}, data = json.dumps(r_dps, encoding="utf-8"))
		print json.dumps(r_dps, encoding="utf-8")
		r.raise_for_status()
