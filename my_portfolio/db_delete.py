import sqlite3

#データベース読み込み
db = sqlite3.connect(
    "db.sqlite3",              #ファイル名
    isolation_level=None,
)

#レコード削除用SQL文
sql = """DELETE FROM dialog_post"""

db.execute(sql)  #sql文を実行
db.close()      #データベースを閉じる