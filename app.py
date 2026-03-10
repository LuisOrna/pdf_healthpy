import os
import tempfile
from flask import Flask, render_template, request, send_file

from handle_upload import validate_and_save
from extract_id import get_document, extract_entities
from process_data import process
from fill_form import fill_pdf

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("photo")
    if not file:
        return "No file uploaded.", 400

    image_path = validate_and_save(file)
    if not image_path:
        return "Invalid file. Please upload a JPG or PNG image.", 400

    document = get_document(image_path)
    entities = extract_entities(document)
    os.remove(image_path)

    return render_template("review.html", data=entities)


@app.route("/generate", methods=["POST"])
def generate():
    verified_data = {
        "nombres":    request.form.get("nombres", ""),
        "apellidos":  request.form.get("apellidos", ""),
        "numero":     request.form.get("numero", ""),
        "nacimiento": request.form.get("nacimiento", ""),
        "sexo":       request.form.get("sexo", ""),
        "plan":       request.form.get("plan", ""),
    }

    processed_data = process(verified_data)

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()

    fill_pdf(processed_data, "djs_a.pdf", tmp.name)

    cedula = verified_data["numero"] or "output"
    return send_file(
        tmp.name,
        as_attachment=True,
        download_name=f"{cedula}_djs.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
