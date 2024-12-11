from dotenv import load_dotenv
import os
import psycopg2
import json
from datetime import datetime

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")



try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=dbname,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]  # 컬럼 이름 가져오기
    data = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        for key, value in row_dict.items():
            if isinstance(value, datetime):
                row_dict[key] = value.isoformat()  # datetime 객체를 ISO 형식으로 변환
        data.append(row_dict)

    print(json.dumps(data, indent=4))

except Exception as error:
    print(f"Error: {error}")

finally:
    if connection:
        cursor.close()
        connection.close()