class RoomAssignment:

  @staticmethod
  def assign_rooms(courses, colors_result, rooms, room_busy_set):
    """Gán phòng học cho từng lớp học phần dựa vào khung giờ đã tô màu.

    Trả về: danh sách các bản ghi hoàn chỉnh cho TKB.
    """
    course_map = {c["lop_hp_id"]: c for c in courses}
    sorted_rooms = sorted(rooms, key=lambda r: r["suc_chua"])

    schedule_results = []
    booked_room_slots = set(
        (rb["phong_id"], rb["khung_gio_id"]) for rb in room_busy_set
    )

    for lop_hp_id, khung_gio_id in colors_result.items():
      course = course_map[lop_hp_id]
      si_so = course["si_so_du_kien"]
      loai_yeu_cau = course["loai_phong_yeu_cau"]

      assigned_room_id = None

      # Ưu tiên 1: Tìm phòng đúng loại yêu cầu và đủ sức chứa, chưa bị bận
      for room in sorted_rooms:
        if (
            room["loai_phong"] == loai_yeu_cau
            and room["suc_chua"] >= si_so
            and (room["phong_id"], khung_gio_id) not in booked_room_slots
        ):
          assigned_room_id = room["phong_id"]
          booked_room_slots.add((room["phong_id"], khung_gio_id))
          break

      # Ưu tiên 2: Tìm phòng loại khác đủ sức chứa
      if not assigned_room_id:
        for room in sorted_rooms:
          if (
              room["suc_chua"] >= si_so
              and (room["phong_id"], khung_gio_id) not in booked_room_slots
          ):
            assigned_room_id = room["phong_id"]
            booked_room_slots.add((room["phong_id"], khung_gio_id))
            break

      if not assigned_room_id and rooms:
        assigned_room_id = rooms[0]["phong_id"]

      schedule_results.append({
          "lop_hp_id": lop_hp_id,
          "khung_gio_id": khung_gio_id,
          "phong_id": assigned_room_id,
      })

    return schedule_results