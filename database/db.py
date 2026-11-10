import mysql.connector
from mysql.connector import Error


def get_connection():
  """Tạo kết nối tới cơ sở dữ liệu MySQL qlyTKB"""
  try:
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123321",  # Điền chính xác mật khẩu MySQL của bạn vào đây
    database="qlyTKB",
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci",
)
    if connection.is_connected():
      return connection
  except Error as e:
    print(f"Lỗi kết nối cơ sở dữ liệu MySQL: {e}")
  return None