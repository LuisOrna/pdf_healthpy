import os
import tempfile
from flask import Flask, render_template, request, send_file, session, redirect

from handle_upload import validate_and_save
from extract_id import get_document, extract_entities
from process_data import process, get_form_type
from fill_form import fill_pdf

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")


@app.route("/review")
def review():
    members = session.get("members")
    plan = session.get("plan", "")
    if not members:
        return redirect("/")
    return render_template("review.html", members=members, plan=plan)


@app.route("/add_member", methods=["POST"])
def add_member():
    role = request.form.get("role")
    members = session.get("members", [])
    members.append({
        "role": role, "form_type": "djs_a",
        "nombres": "", "apellidos": "", "numero": "",
        "nacimiento": "", "sexo": "",
    })
    session["members"] = members
    return redirect("/review")


@app.route("/upload", methods=["POST"])
def upload():
    # Collect uploaded photos in member order, skipping missing/empty files
    candidates = [("titular", "photo")] + \
                 [("conyuge", "conyuge_foto")] + \
                 [("dependiente", f"dependiente_foto_{i}") for i in range(5)]

    members = []
    for role, field_name in candidates:
        file = request.files.get(field_name)
        if not file or file.filename == "":
            continue

        image_path = validate_and_save(file)
        if not image_path:
            return f"Invalid file for {field_name}. Please upload a JPG or PNG image.", 400

        document = get_document(image_path)
        entities = extract_entities(document)
        os.remove(image_path)

        # Titular always uses djs_a; for others determine by age (fall back if date is malformed)
        if role == "titular" or len(members) == 0:
            form_type = "djs_a"
        else:
            try:
                form_type = get_form_type(entities.get("nacimiento", ""))
            except Exception:
                form_type = "djs_a"

        member = {"role": role, "form_type": form_type}
        member.update(entities)
        members.append(member)

    if not members:
        return "No file uploaded.", 400

    session["members"] = members
    session["plan"] = request.form.get("plan", "")

    return render_template("review.html", members=session["members"], plan=session["plan"])


@app.route("/generate", methods=["POST"])
def generate():
    members = session.get("members", [])
    plan = session.get("plan", "")
    member_index = int(request.form.get("member_index", 0))

    # Reconstruct nacimiento from the 3 split date fields
    dia = request.form.get("dia_nac", "").zfill(2)
    mes = request.form.get("mes_nac", "").zfill(2)
    ano = request.form.get("año_nac", "")
    nacimiento = f"{dia}-{mes}-{ano}" if dia and mes and ano else ""

    verified_data = {
        "nombres":    request.form.get("nombres", ""),
        "apellidos":  request.form.get("apellidos", ""),
        "numero":     request.form.get("numero", ""),
        "nacimiento": nacimiento,
        "sexo":       request.form.get("sexo", ""),
        "plan":       plan,
    }

    # Write user corrections back to session so other members get correct titular data
    members[member_index]["nombres"]    = verified_data["nombres"]
    members[member_index]["apellidos"]  = verified_data["apellidos"]
    members[member_index]["numero"]     = verified_data["numero"]
    members[member_index]["nacimiento"] = verified_data["nacimiento"]
    members[member_index]["sexo"]       = verified_data["sexo"]
    session["members"] = members  # re-assign so Flask detects the change

    t = members[0]
    titular = {
        "nombre": t.get("nombres", "") + " " + t.get("apellidos", ""),
        "cedula": t.get("numero", ""),
    }

    processed_data = process(verified_data)

    if member_index == 0:
        form_type = "djs_a"
    else:
        try:
            form_type = get_form_type(verified_data["nacimiento"])
        except Exception:
            form_type = "djs_a"

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()

    fill_pdf(processed_data, form_type, titular, tmp.name)

    cedula = verified_data["numero"] or "output"
    download_name = f"{cedula}_djs.pdf" if form_type == "djs_a" else f"{cedula}_djsm.pdf"

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
