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

## [dh_visualizer.py](../../src/run/dh_visualizer.py)

- センサデータの CSV ファイルから，グラフを表示する
  - リアルタイム表示には，csv_exporter.py も実行する必要がある
- Dash Plotly 製ビジュアライザ
  - 1画面に収まる
  - 新しい CSV を利用するには，サーバを再起動する必要がある

### 実行

    - `python src/run/dh_visualizer.py`

## [st_visualizer.py](../../src/run/st_visualizer.py)

- センサデータの CSV ファイルから，グラフを表示する
  - リアルタイム表示には，csv_exporter.py も実行する必要がある

- Stremlit Plotly 製ビジュアライザ
  - 画面がきれい
  - 新しい CSV を Ctrl-R のウインドウ読み込みで利用できる

### 実行

    - `streamlit run src/run/st_visualizer.py`
