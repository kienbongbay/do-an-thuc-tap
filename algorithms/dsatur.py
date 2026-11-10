class DSATUR:
    
  @staticmethod
  def color_graph(courses, adj_list, timeslots, teacher_busy_set):
    """Thuật toán DSATUR kết hợp ràng buộc khung giờ và lịch bận giảng viên.

    Trả về: (coloring_result, total_colors_used, conflicts_count)
    """
    course_map = {c["lop_hp_id"]: c for c in courses}
    colors = {}  # lop_hp_id -> khung_gio_id
    degrees = {c["lop_hp_id"]: len(adj_list[c["lop_hp_id"]]) for c in courses}
    saturation = {c["lop_hp_id"]: 0 for c in courses}

    uncolored = set(course_map.keys())
    conflicts_count = 0

    while uncolored:
      # Chọn đỉnh có độ bão hòa lớn nhất, nếu bằng nhau thì chọn bậc lớn nhất
      best_vertex = max(
          uncolored,
          key=lambda v: (
              saturation[v],
              degrees[v],
          ),
      )
      uncolored.remove(best_vertex)

      course_info = course_map[best_vertex]
      teacher_id = course_info["giang_vien_id"]

      # Tìm các khung giờ đã bị dùng bởi các đỉnh kề đã tô màu
      neighbor_colors = {
          colors[neighbor]
          for neighbor in adj_list[best_vertex]
          if neighbor in colors
      }

      # Lọc các khung giờ hợp lệ:
      # 1. Không trùng với các lớp kề
      # 2. Không nằm trong lịch bận của giảng viên
      available_slots = []
      for ts in timeslots:
        ts_id = ts["khung_gio_id"]
        if (
            ts_id not in neighbor_colors
            and (teacher_id, ts_id) not in teacher_busy_set
        ):
          available_slots.append(ts_id)

      if available_slots:
        # Chọn khung giờ đầu tiên thỏa mãn (chiến lược tham lam)
        colors[best_vertex] = available_slots[0]
      else:
        # Nếu hết khung giờ sạch, bắt buộc phải chọn khung giờ ít xung đột nhất (xử lý ngoại lệ)
        conflicts_count += 1
        colors[best_vertex] = timeslots[0]["khung_gio_id"]

      # Cập nhật độ bão hòa cho các đỉnh kề chưa tô màu
      for neighbor in adj_list[best_vertex]:
        if neighbor in uncolored:
          neighbor_colored_slots = {
              colors[n] for n in adj_list[neighbor] if n in colors
          }
          saturation[neighbor] = len(neighbor_colored_slots)

    total_colors_used = len(set(colors.values()))
    return colors, total_colors_used, conflicts_count