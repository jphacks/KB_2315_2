# サーバの仕様

## エンドポイント

- "<http://host/data>"

## データ形式

- 以下に示す Json 形式で出力する

    ``` json
    {
        "sensor0": "{
            \"temperature\":9.256178477569232,
            \"humidity\":92.36585602151631,
            \"pressure\":911.9604060527855
        }",
        "sensor1": "{
            \"temperature\":18.856169180463702,
            \"humidity\":30.715207330240812,
            \"pressure\":966.3004798556474
        }",
        "sensor2": "{
            \"temperature\":24.253366648363514,
            \"humidity\":68.07229821318646,
            \"pressure\":1001.118000638555
        }"
    }
    ```

- オブジェクト
  - キー名（上の例では sensor0 等）センサの ID となり，重複してはならない
  - temperatue : 温度
  - humidity : 湿度
  - pressure : 気圧

- オブジェクト数は可変であり，Python・C++ ともに同様の設計がされている
  - それぞれの実装において留意点がある場合は，各言語のドキュメントに記載する
