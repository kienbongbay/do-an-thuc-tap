from database.repository import Repository
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Bắt buộc có secret_key để dùng flash message

Repository.clear_schedule()


@app.route("/")
def index():
  schedule_list = Repository.get_all_timetable()
  return render_template("index.html", schedules=schedule_list)


@app.route("/add-schedule", methods=["POST"])
def add_schedule():
  ten_giang_vien = request.form.get("ten_giang_vien")
  mon_hoc_id = request.form.get("mon_hoc_id")
  ten_mon_hoc = request.form.get("ten_mon_hoc")
  so_tiet = request.form.get("so_tiet")
  thu_trong_tuan = request.form.get("thu_trong_tuan")
  phong_hoc = request.form.get("phong_hoc")
  tiet_bat_dau = request.form.get("tiet_bat_dau")

  result = Repository.add_custom_schedule(
      ten_giang_vien,
      mon_hoc_id,
      ten_mon_hoc,
      so_tiet,
      thu_trong_tuan,
      phong_hoc,
      tiet_bat_dau,
  )

  # Nếu kết quả trả về không phải True (tức là có lỗi/trùng lịch), đẩy thông báo ra web
  if result is not True:
    flash(result, "danger")
  else:
    flash("Thêm lịch học thành công!", "success")

  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(debug=True)