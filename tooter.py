#!/bin/env python
# -*- coding: utf-8 -*- 
import random
from mastodon import Mastodon

# OAuth2クライアント登録
def register_app():
    with open('mastodon.setting','r') as fd:
        for L in fd.readlines():
            exec(L)

    Mastodon.create_app(
        'LochNessWeather_bot',
        to_file = client_id_file,
        api_base_url = api_base_url
    )

# アクセストークン取得
def fetch_token():
    with open('mastodon.setting','r') as fd:
        for L in fd.readlines():
            exec(L)

    mastodon = Mastodon(
        client_id = client_id_file,
        api_base_url = api_base_url
    )
    mastodon.log_in(
        email,
        passwd,
        to_file = access_token_file
    )

# トゥート
def toot(word):
    with open('mastodon.setting','r') as fd:
        for L in fd.readlines():
            exec(L)

    mastodon = Mastodon(
        client_id = client_id_file,
        access_token = access_token_file,
        api_base_url = api_base_url
    )
    print word
    ret = mastodon.toot(word)
    return ret

# 現況
def weather_chatting():
    import owm
    data = owm.getLochNess()

    # 現在の天気
    current = data[sorted(data.keys())[0]]
    info_current = u"現在: %s, %3.1f℃" % (current["weather"],current["temp"])

    toot(info_current)

# 予報
def forecast_chatting():
    import owm
    data = owm.getLochNess()
    toots = []

    # 予報
    for k in sorted(data.keys())[1:5]:
        dt_txt  = data[k]["date"]
        weather = data[k]["weather"]
        temp    = data[k]["temp"]
        info_after = u"%s(予報): %s, %3.1f℃" % (dt_txt, weather, temp)
        toots.append(info_after)

    for t in toots:
        toot(t)

# 天気に一言コメント
def weather_comment():
    import owm
    data = owm.getLochNess()
    t = []

    d = data[sorted(data.keys())[0]]

    temp = d["temp"]
    weather = d["weather"]
    if temp < 0:
        t.append(u"ネッシー観察は寒いので防寒対策が必要です。")
    elif temp < 10:
        t.append(u"ちょっと寒いので寒さに気をつけて。")
    elif temp < 20 and weather == "Clear":
        t.append(u"ネッシー観察日和")
    elif temp < 25 and weather == "Clear":
        t.append(u"気温上昇、薄着のおねーちゃんにネッシーも大喜び。")
    elif temp < 30 and weather == "Clear":
        t.append(u"ネッシーといっしょにネス湖で泳げる。")

    if weather == "Rain":
        t.append(u"傘を忘れずに。")

    toot(''.join(t))

# 雑談
def misc_chatting():
    import os
    import random

    vocabulary = [ u"ネッシーは実在するんだ！！" ]
    if os.path.isfile('vocabulary'):
        with open('vocabulary','r') as fd:
            for L in fd.readlines():
                vocabulary.append(L.rstrip("\n").rstrip("\r"))

    t = []
    n = random.randint(0, len(vocabulary)-1)
    t.append(vocabulary[n])

    # 40%の確率で@を飛ばす
    if random.randint(0,99) < 40:
        reply_to = [ "kawarusosu" ]
        if os.path.isfile('reply_to'):
            with open('reply_to','r') as fd:
                for L in fd.readlines():
                    reply_to.append(L.rstrip("\n").rstrip("\r"))

        n = random.randint(0,len(reply_to)-1)
        t = [ "@%s" % reply_to[n] ] + t

    toot(' '.join(t))


def main():
    import time
    import random
    from datetime import datetime
    from datetime import timedelta

    c = 0
    while True:
        c = c + 1
        if c % 60 == 0:
            # 10分ごとに現在の天気をトゥート
            weather_chatting()

            # 20%の確率でランダムでコメント
            if random.randint(0,99) < 20:
                weather_comment()

        if c % 180 == 0:
            # 30分ごとに現在の天気予報をトゥート
            forecast_chatting()

        if (c - 3) % 18 == 0:
            # 3分ごとに25%の確率でランダムで雑談
            if random.randint(0,99) < 25:
                misc_chatting()

        time.sleep(10)



if __name__ == '__main__':
    import time
    from datetime import datetime
    dn = int(time.mktime(datetime.now().timetuple()))
    random.seed(dn)

    main()


