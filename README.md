# 画像ファイル配信アプリ

このアプリは、指定したディレクトリ内の画像ファイルを日付別に配信します。

## インストール

```
$ git clone https://github.com/u1and0/PicServer.git
$ pip install -r requirements.txt
```

## 使用方法

1. 以下のコマンドを実行して、アプリを起動します。

```
$ uvicorn main:app --port 8888 --host 0.0.0.0
```

2. ブラウザで `http://localhost:8888` にアクセスします。

## エンドポイント

- `/index`: 最新の画像ファイル10件を表示します。
- `/{date}`: 指定した日付の画像を表示します。

日付の指定はカレンダーから選択することができます。

## 必要なファイル

- `templates`ディレクトリ: テンプレートHTMLファイルを格納するディレクトリです。
- `static`ディレクトリ: 画像ファイルを格納するディレクトリです。ルートディレ
クトリ以下に配置する必要があります。

## 注意事項

- 画像ファイルは、拡張子が `.jpg` である必要があります。
- `/{date}`エンドポイントでは、指定した日付の画像ファイルのうち、最初に見つかった `.gif` ファイルを表示します。