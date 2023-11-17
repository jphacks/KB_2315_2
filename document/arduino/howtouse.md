# 説明

## [secret.h](../../arduino/include/base_secret.h)

- WiFiのSSIDとパスワードを記述する

## [main.cpp](../../arduino/src/main.cpp)

- update_interval_sec : データを送信する間隔を秒単位で指定する

### データ格納について

- 以下のようなコードで json 出力を記述する
  - 詳しい仕様は [server_spec.md](../../document/common/server_spec.md) を参照
  - この例では，3つのセンサのデータを送信している

  ``` json
  json_doc["Room"] = "{\"temperature\":" + String(RoomTemp) +
                     ",\"humidity\":" + String(RoomHumi) + "}";
  json_doc["Shoe"] = "{\"temperature\":" + String(ShoeTemp) +
                     ",\"humidity\":" + String(ShoeHumi) +
                     ",\"pressure\":" + String(ShoePre) + "}";
  json_doc["Shoe2"] = "{\"temperature\":" + String(Shoe2Temp) +
                      ",\"humidity\":" + String(Shoe2Temp) + "}";
  ```

- オブジェクト
  - キー名（上の例では Room 等）センサの ID となり，重複してはならない
    - temperatue : 温度
    - humidity : 湿度
    - pressure : 気圧
  - これらの値を指定しない場合，サーバ側で float 0.0 として処理される
- センサ数が多い場合，json メモリサイズを超過する可能性がある
  - その場合，以下の2つのメモリサイズを変更する

    - ``` cpp
        StaticJsonDocument<288> json_doc;
        char exporter_plain_json[1536]; 
        ```
