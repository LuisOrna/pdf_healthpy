import pypdf
from pypdf.generic import RectangleObject, NameObject


def _resolve_indirect_rects(writer):
    for page in writer.pages:
        if "/Annots" not in page:
            continue
        for annot_ref in page["/Annots"]:
            try:
                annot = annot_ref.get_object()
                rect = annot.get("/Rect")
                if rect is None:
                    continue
                rect = rect.get_object() if hasattr(rect, "get_object") else rect
                coords = [
                    float(c.get_object() if hasattr(c, "get_object") else c)
                    for c in rect
                ]
                annot.update({NameObject("/Rect"): RectangleObject(coords)})
            except Exception:
                pass


def fill_anexo(titular_nombre, cedula, plan, output_pdf):
    """
    Fill anexo.pdf with plan holder data and write to output_pdf.

    titular_nombre — full name (nombres + apellidos) of the titular
    cedula         — cedula number of the titular
    plan           — plan name
    output_pdf     — file path for the generated PDF
    """
    fields = {
        "titular": titular_nombre,
        "cedula":  cedula,
        "Plan":    plan,
    }

    reader = pypdf.PdfReader("anexo.pdf")
    writer = pypdf.PdfWriter()
    writer.append(reader)
    _resolve_indirect_rects(writer)
    writer.update_page_form_field_values(writer.pages[0], fields)

    with open(output_pdf, "wb") as f:
        writer.write(f)
