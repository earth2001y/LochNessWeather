# LochNessWeather

2017年のNASA Space Apps Challenge 東京会場のマープロジェクトで作った[マーストドン](https://marstodon.com/)のネス湖お天気情報botのプログラムです。

OpenWeatherMapからネス湖の気象情報と予報を取得してトゥートします。

## 準備手順

1. [Mastodon.py](https://github.com/halcy/Mastodon.py)をインストールする。
2. 任意のマストドンインスタンスでアカウントをつくる
3. mastodon.setting.templ を mastodon.setting にリネームして、次の値を設定する。
    * api\_base\_url: マストドンインスタンスのURL
    * email: アカウントのメールアドレス
    * passwd: アカウントのパスワード
4. tooter.py の register\_app() を実行して、アプリを登録してクライアントIDを取得する。
    * client\_id に設定したファイルにクライアントIDが記録される。
5. tooter.py の fetch\_token() を実行して、トークンを取得する。
    * access\_token に設定したファイルにトークンが記録される。
6. [OpenWeatherMap](https://openweathermap.org/)でアカウントを作ってAPIアクセスキーを取得する
7. owm.setting.templ を owm.setting にリネームして、次の値を設定する。
    * API\_KEY: APIアクセスキー

## 実行方法

```sh
$ python tooter.py
```

