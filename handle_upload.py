import os
import tempfile

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}


def validate_and_save(file):
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        return None

    tmp = tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False)
    file.save(tmp.name)
    tmp.close()

    return tmp.name
