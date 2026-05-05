from flask import Flask, render_template, request, redirect
import pymysql
from config import Config
from utils.s3_upload import upload_file

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASS,
        database=Config.DB_NAME
    )

@app.route("/")
def index():
    return render_template("index.html")

# ========================
# 1. PENGAJUAN SURAT
# ========================
@app.route("/pengajuan", methods=["GET", "POST"])
def pengajuan():
    if request.method == "POST":
        nama = request.form["nama"]
        jenis = request.form["jenis"]
        file = request.files["file"]

        file_url = upload_file(file)

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO pengajuan (nama, jenis, file_url, status)
            VALUES (%s, %s, %s, %s)
        """, (nama, jenis, file_url, "Diproses"))

        db.commit()
        db.close()

        return redirect("/")

    return render_template("pengajuan.html")


# ========================
# 2. PENGADUAN
# ========================
@app.route("/pengaduan", methods=["GET", "POST"])
def pengaduan():
    if request.method == "POST":
        isi = request.form["isi"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO pengaduan (isi) VALUES (%s)", (isi,))
        db.commit()
        db.close()

        return redirect("/")

    return render_template("pengaduan.html")


# ========================
# 3. TRACKING
# ========================
@app.route("/tracking")
def tracking():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM pengajuan")
    data = cursor.fetchall()

    db.close()
    return render_template("tracking.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)