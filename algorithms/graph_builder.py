class GraphBuilder:
    
  @staticmethod
  def build_conflict_graph(courses):
    """Xây dựng danh sách kề (adjacency list) cho các lớp học phần.

    Hai lớp học phần xung đột nếu: - Cùng giảng viên (giang_vien_id) - Cùng lớp
    sinh viên (lop_id)
    """
    adj_list = {course["lop_hp_id"]: set() for course in courses}

    for i in range(len(courses)):
      for j in range(i + 1, len(courses)):
        c1 = courses[i]
        c2 = courses[j]

        is_conflict = False
        # Xung đột giảng viên
        if c1["giang_vien_id"] == c2["giang_vien_id"]:
          is_conflict = True
        # Xung đột lớp sinh viên
        if c1["lop_id"] == c2["lop_id"]:
          is_conflict = True

        if is_conflict:
          adj_list[c1["lop_hp_id"]].add(c2["lop_hp_id"])
          adj_list[c2["lop_hp_id"]].add(c1["lop_hp_id"])

    return adj_list