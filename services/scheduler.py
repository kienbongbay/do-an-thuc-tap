import time
from algorithms.dsatur import DSATUR
from algorithms.graph_builder import GraphBuilder
from algorithms.room_assignment import RoomAssignment
from database.repository import Repository


class Scheduler:

  @staticmethod
  def run_scheduling():
    print("--- BẮT ĐẦU QUÁ TRÌNH TỰ ĐỘNG XẾP LỊCH ---")
    start_time = time.time()

    # 1. Lấy dữ liệu từ Database
    courses = Repository.get_all_classes_to_schedule()
    rooms = Repository.get_available_rooms()
    timeslots = Repository.get_available_timeslots()
    teacher_busy = Repository.get_teacher_busy_slots()
    room_busy = Repository.get_room_busy_slots()

    if not courses:
      print("Không có lớp học phần nào cần xếp lịch!")
      return False

    if not timeslots:
      print("Chưa có dữ liệu khung giờ trong database!")
      return False

    if not rooms:
      print("Chưa có dữ liệu phòng học trong database!")
      return False

    # 2. Xây dựng đồ thị xung đột
    print("Đang xây dựng đồ thị xung đột...")
    adj_list = GraphBuilder.build_conflict_graph(courses)

    # 3. Chạy thuật toán tô màu đồ thị DSATUR
    print("Đang thực thi thuật toán DSATUR tô màu đồ thị...")
    colors_result, total_colors, conflicts = DSATUR.color_graph(
        courses, adj_list, timeslots, teacher_busy
    )

    # 4. Gán phòng học
    print("Đang thực hiện gán phòng học...")
    schedule_data = RoomAssignment.assign_rooms(
        courses, colors_result, rooms, room_busy
    )

    # Tính thời gian xử lý (ms)
    elapsed_time_ms = int((time.time() - start_time) * 1000)

    # 5. Lưu kết quả vào Database
    history_data = {
        "so_mau_su_dung": total_colors,
        "so_xung_dot": conflicts,
        "thoi_gian_xu_ly_ms": elapsed_time_ms,
    }

    print(
        f"Xếp lịch thành công! Số khung giờ sử dụng: {total_colors}, Số xung"
        f" đột giải quyết: {conflicts}, Thời gian: {elapsed_time_ms}ms"
    )

    success = Repository.save_timetable(schedule_data, history_data)
    return success