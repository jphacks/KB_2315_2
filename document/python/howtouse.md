# 説明

## 共通

- 吐き出される config.toml に設定を行う
  - Python 製シミュレータを用いる場合
    - `client_ip = "localhost`
  - Arduino を用いる場合
    - `client_ip = "Arduino の IP"`

## [sample_server.py](../../src/run/sample_server.py)

- Arduino のセンサ出力をを模倣して，出力するサーバ

### 実行

    - `python src/run/data_sampler.py`

## [csv_exporter.py](../../src/run/csv_exporter.py)

- Arduino のセンササーバからの出力を取得して，CSV ファイルに出力する

### 実行

    - `python src/run/csv_exporter.py`

## [visualizer.py](../../src/run/visualizer.py)

- Arduino のセンササーバからの出力を取得して，CSVファイルに出力 & グラフを表示する

### 実行

    - `python src/run/visualizer.py`
