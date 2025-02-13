# tech0_posapp_back

- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

- uvicorn main:app --reload
- uvicorn app:app --reload --port 8080

- deactivate

# DB構築

- brew services start mysql

- MySQL サーバーを停止
brew services stop mysql

- 安全モードで起動（認証スキップ）
mysqld_safe --skip-grant-tables &

- MySQL にログイン
mysql -u root

- 新しいパスワードでログインを試行
mysql -u root -p

- ログイン（パスワード付き）
mysql --user=root --password

- MySQL サーバー起動コマンド
killall mysqld
brew services start mysql
brew services stop mysql
