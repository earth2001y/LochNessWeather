#!/bin/env python
# -*- coding: utf-8 -*- 

def parse_weather(response):
    import json

    data = {}
    resj = ''
    for L in response.readlines():
        resj = resj + L
    res = json.loads(resj)

    dt      = int(res['dt'])
    dttxt   = ''
    temp    = float(res['main']['temp']) - 273.15
    weather = res['weather'][0]['main']
    data[dt] = { 'date': dttxt, 'temp': temp, 'weather': weather }

    return data


def parse_forecast(response):
    import json

    data = {}
    resj = ''
    for L in response.readlines():
        resj = resj + L
    res = json.loads(resj)
    for d in res['list']:
        dt      = int(d['dt'])
        dttxt   = d['dt_txt']
        temp    = float(d['main']['temp']) - 273.15
        weather = d['weather'][0]['main']
        data[dt] = { 'date': dttxt, 'temp': temp, 'weather': weather }

    return data


def getLochNess():
    import os
    import json
    import time
    import urllib
    import urllib2
    from datetime import datetime
    from datetime import timedelta

    cache_file = 'LochNess.cache'
    dn = int(time.mktime(datetime.now().timetuple()))
    ct = int(os.stat(cache_file).st_mtime) if os.path.isfile(cache_file) else 0
    if ct < dn - 600:
        # キャッシュが無い OR 古いので、Webからフェッチする

        with open('owm.setting','r') as fd:
            for L in fd.readlines():
                exec(L)

        weather_url  = "%s/weather?q=Loch Ness,uk&APPID=%s" % (BASE_URL,API_KEY)
        forecast_url = "%s/forecast?q=Loch Ness,uk&APPID=%s" % (BASE_URL,API_KEY)

        # query
        weather_response  = urllib2.urlopen(weather_url)
        forecast_response = urllib2.urlopen(forecast_url)

        weather_data  = parse_weather(weather_response)
        forecast_data = parse_forecast(forecast_response)

        data = {}
        for k in weather_data.keys():
            data[k] = weather_data[k]
        for k in forecast_data.keys():
            data[k] = forecast_data[k]

        jstr = json.dumps(data)
        with open(cache_file,'w') as fd:
            fd.write(jstr)

    else:
        # キャッシュを参照
        data = {}
        with open(cache_file,'r') as fd:
            jstr = ""
            for L in fd.readlines():
                jstr = jstr + L

        data = json.loads(jstr)

    return data


if __name__ == '__main__':
    data = getLochNess()
    for k in sorted(data.keys()):
        print data[k]

