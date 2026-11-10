from database.db import get_connection


class Repository:

  @staticmethod
  def get_all_timetable():
    conn = get_connection()
    if not conn:
      return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
            SELECT * FROM thoi_khoa_bieu_chi_tiet 
            ORDER BY thu_trong_tuan, tiet_bat_dau
        """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

  @staticmethod
  def add_custom_schedule(
      ten_giang_vien,
      mon_hoc_id,
      ten_mon_hoc,
      so_tiet,
      thu_trong_tuan,
      phong_hoc,
      tiet_bat_dau,
  ):
    conn = get_connection()
    if not conn:
      return "Không thể kết nối cơ sở dữ liệu!"
    
    cursor = conn.cursor(dictionary=True)
    try:
      mon_hoc_id = str(mon_hoc_id).strip()
      so_tiet = int(so_tiet)
      thu_trong_tuan = int(thu_trong_tuan)
      tiet_bat_dau = int(tiet_bat_dau)
      tiet_ket_thuc = tiet_bat_dau + so_tiet - 1

      # 1. Kiểm tra xung đột kỹ lưỡng
      check_query = """
                SELECT * FROM thoi_khoa_bieu_chi_tiet 
                WHERE thu_trong_tuan = %s 
                  AND (phong_hoc = %s OR ten_giang_vien = %s OR mon_hoc_id = %s)
                  AND NOT (tiet_ket_thuc < %s OR tiet_bat_dau > %s)
            """
      cursor.execute(
          check_query,
          (
              thu_trong_tuan,
              phong_hoc,
              ten_giang_vien,
              mon_hoc_id,
              tiet_bat_dau,
              tiet_ket_thuc,
          ),
      )
      conflicts = cursor.fetchall()

      if conflicts:
        return "Khung giờ này đã được sắp xếp môn học (hoặc trùng phòng/giảng viên/mã môn) trước đó!"

      # 2. INSERT vào CSDL
      insert_query = """
                INSERT INTO thoi_khoa_bieu_chi_tiet 
                (ten_giang_vien, mon_hoc_id, ten_mon_hoc, so_tiet, thu_trong_tuan, phong_hoc, tiet_bat_dau, tiet_ket_thuc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
      cursor.execute(
          insert_query,
          (
              ten_giang_vien,
              mon_hoc_id,
              ten_mon_hoc,
              so_tiet,
              thu_trong_tuan,
              phong_hoc,
              tiet_bat_dau,
              tiet_ket_thuc,
          ),
      )
      conn.commit()
      return True
    except Exception as e:
      print(f"Lỗi: {e}")
      conn.rollback()
      return f"Lỗi hệ thống: {e}"
    finally:
      cursor.close()
      conn.close()

  @staticmethod
  def clear_schedule():
    conn = get_connection()
    if not conn:
      return
    cursor = conn.cursor()
    try:
      cursor.execute("TRUNCATE TABLE thoi_khoa_bieu_chi_tiet")
      conn.commit()
    except Exception as e:
      print(f"Lỗi: {e}")
    finally:
      cursor.close()
      conn.close()