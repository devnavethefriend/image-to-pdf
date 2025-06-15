import os
import uuid
from flask import Flask, request, render_template, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def images_to_pdf(image_paths, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4
    temp_files = []

    for path in image_paths:
        with Image.open(path) as img:
            img = img.convert("RGB")
            ratio = min(page_width / img.width, page_height / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

            # Generate a unique temporary filename
            temp_img_path = f"temp_{uuid.uuid4().hex}.jpg"
            img.save(temp_img_path)
            temp_files.append(temp_img_path)

            x = (page_width - new_size[0]) / 2
            y = (page_height - new_size[1]) / 2
            c.drawImage(temp_img_path, x, y, width=new_size[0], height=new_size[1])
            c.showPage()

    c.save()

    # Clean up all temp images after saving the PDF
    for temp_file in temp_files:
        os.remove(temp_file)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("images")  # Correct way to handle multiple files
        image_paths = []

        for file in files:
            if file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_paths.append(filepath)

        if image_paths:
            output_pdf = os.path.join(app.config['OUTPUT_FOLDER'], "output.pdf")
            images_to_pdf(image_paths, output_pdf)

            for img in image_paths:
                os.remove(img)

            return redirect(url_for("download_pdf"))
    return render_template("index.html")

@app.route("/download")
def download_pdf():
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], "output.pdf"), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
