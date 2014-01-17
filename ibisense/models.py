__title__ = 'ibisense-api-python'
__version__ = '0.0.1'

from dateutil import parser
import datetime
import json

__all__ = ['Sensor', 'Channel', 'DataPoint', 'DataSet']

class Base(object):
    def __init__(self):
        self._data = {}

    def __getrep__(self):
        return {k: v for k, v in self._data.items() if v is not None}

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            class_name = self.__class__.__name__
            raise AttributeError("'{}' object has no attribute '{}'".format(class_name, name))

    def __setattr__(self, name, value):
        if not name.startswith('_') and name not in dir(self.__class__):
            self._data[name] = value
        else:
            super(Base, self).__setattr__(name, value)

    def toJson(self):
        return self.__getrep__()

class Sensor(Base):
    def __init__(self, suid = "", name = "", description = "", access_flag = "public", 
        latitude = 0.0, longitude = 0.0, attributes = {}, channels = [], active = False, 
        activated_at = "", owner_name = "", serial = "", jsonObj = None):
        if jsonObj:
            self._data = jsonObj
        else:
            self._data = {
                'SUID': suid,
                'name': name,
                'description': description,
                'access': access_flag,
                'location' : {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'attributes': attributes,
                'channels': channels,
                'active': active,
                'activated': activated_at,
                'owner_name': owner_name,
                'serial': serial
            }


class Channel(Base):
    def __init__(self, cuid = "", name = "", description = "", 
        attributes = {}, abbreviation = "", unit = "", jsonObj = None):
        if jsonObj:
            self._data = jsonObj
        else:
            self._data = {
                'CUID': cuid,
                'name': name,
                'description': description,
                'attributes': attributes,
                'abbreviation': abbreviation,
                'unit': unit
            }


class DataPoint(Base):
    def __init__(self, t = None, v = None, jsonObj = None):
        if jsonObj:
            if jsonObj['t'] is None or jsonObj['v'] is None:
                raise ValueError('t and v are mandatory')
            if isinstance(jsonObj['t'], (str, unicode)):
                try:
                    jsonObj['t'] = parser.parse(str(jsonObj['t']))
                except ValueError, e:
                    raise e
            elif isinstance(jsonObj['t'], (float, int)):
                jsonObj['t'] = datetime.datetime.fromtimestamp(float(jsonObj['t']) / 1000)
            elif type(jsonObj['t']) is  not datetime.datetime:
                raise TypeError('t must be a datetime.datetime or a string, not %s' % type(jsonObj['t']))

            jsonObj['v'] = float(jsonObj['v'])
            self._data = jsonObj
        else:
            if isinstance(t, (str, unicode)):
                try:
                    t = parser.parse(str(t))
                except ValueError, e:
                    raise e
            elif isinstance(t, (float, int)):
                t = datetime.datetime.fromtimestamp(float(t) / 1000)
            elif type(t) is  not datetime.datetime:
                raise TypeError('t must be a datetime.datetime or a string, not %s' % type(t))
            v = float(v)
            self._data = {
                't': t,
                'v': v
            }

    def toDict(self):
        return {
            't': self._data['t'].isoformat(), 
            'v': self._data['v']
        }

    def toJson(self):
        return json.dumps(self.toDict(), encoding="utf-8")

class DataSet(Base):
    def __init__(self, CUID, start, end, summary, datapoints, jsonObj = None):
        if jsonObj:
            if not jsonObj['CUID'] or not jsonObj['start'] or not jsonObj['end'] or not jsonObj['summary'] or not jsonObj['datapoints']:
                raise ValueError('Mandatory fields are: CUID, start, end, summary, datapoints')
            if isinstance(jsonObj['start'], (str, unicode)):
                jsonObj.start = parser.parse(str(jsonObj['start']))
            elif type(jsonObj['start']) is  not datetime.datetime:
                raise TypeError('start must be a datetime.datetime or a string, not %s' % type(start))

            if isinstance(jsonObj['end'], (str, unicode)):
                jsonObj['end'] = parser.parse(str(jsonObj['end']))
            elif type(jsonObj['end']) is  not datetime.datetime:
                raise TypeError('end must be a datetime.datetime or a string, not %s' % type(end))

            self._data = jsonObj
        else:
            if not CUID or not start or not end or not summary or not datapoints:
                raise ValueError('Mandatory fields are: CUID, start, end, summary, datapoints')

            if isinstance(start, (str, unicode)):
                start = parser.parse(str(start))
            elif type(start) is  not datetime.datetime:
                raise TypeError('start must be a datetime.datetime or a string, not %s' % type(start))

            if isinstance(end, (str, unicode)):
                end = parser.parse(str(end))
            elif type(end) is not datetime.datetime:
                raise TypeError('end must be a datetime.datetime or a string, not %s' % type(end))

            if type(summary) is not dict:
                raise TypeError('summary must be a dict, not %s' % type(summary))

            if type(datapoints) is not list:
                raise TypeError('datapoints must be a list of ibisense.models.DataPoint, not %s' % type(datapoints))

            self._data = {
                'CUID': CUID,
                'start': start,
                'end': end,
                'summary': summary,
                'datapoints': datapoints
            }

    def toJson(self):
        dataset = {
            'CUID': self._data['CUID'],
            'start': self._data['start'].isoformat(),
            'end': self._data['end'].isoformat(),
            'summary': self._data['summary'],
            'datapoints': [x.toDict() for x in self._data['datapoints']]
        }
        return json.dumps(dataset, encoding="utf-8")
