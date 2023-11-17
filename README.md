# kb-2315-2

## 説明

- ローカルデバッガ

## 使い方

### 環境構築

1. VSCode で [workspace](./.vscode/KB_2315_2.code-workspace) を開く

   - GUI の場合：
     - 「ファイル」 → 「ファイルでワークスペースを開く」
   - ターミナルの場合
     - `code ./.vscode/KB_2315_2.code-workspace`

2. Python の依存関係のインストール
   - Rye の場合
     - `rye sync`
   - python の場合
     - `python -m venv .venv`
     - `source .venv/bin/activate`
     - `pip install -r requirements.lock -r requirements-dev.lock`
