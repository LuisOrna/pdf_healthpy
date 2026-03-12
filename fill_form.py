import os
import pypdf
from pypdf.generic import RectangleObject, NameObject

_HERE = os.path.dirname(os.path.abspath(__file__))


def _resolve_indirect_rects(writer):
    """
    Walk all page annotations and replace any /Rect stored as an IndirectObject
    with a direct RectangleObject. Fixes a pypdf bug where appearance stream
    generation crashes on PDFs that store /Rect as indirect references.
    """
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


def fill_pdf(processed_data, form_type, titular, output_pdf):
    """
    Fill a DJS PDF form and write it to output_pdf.

    processed_data  — dict of the member's own processed fields (from process_data.process())
    form_type       — "djs_a" (adult) or "djs_m" (minor); selects the template automatically
    titular         — dict with "nombre" and "cedula" of the plan holder (titular)
    output_pdf      — file path for the generated PDF

    Field logic:
      djs_a: titular = plan holder's name, declarante = member's full name
      djs_m: titular = plan holder's name, menor = minor's full name,
             cedula_titular = plan holder's CI
    """
    template = os.path.join(_HERE, form_type + ".pdf")

    if form_type == "djs_a":
        fields = dict(processed_data)
        fields["titular"] = titular["nombre"]
        fields["declarante"] = processed_data["titular"]
    else:
        fields = dict(processed_data)
        fields["titular"] = titular["nombre"]
        fields["menor"] = processed_data["titular"]
        fields["cedula_titular"] = titular["cedula"]

    reader = pypdf.PdfReader(template)
    writer = pypdf.PdfWriter()
    writer.append(reader)
    _resolve_indirect_rects(writer)
    writer.update_page_form_field_values(writer.pages[0], fields)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Done! Check {output_pdf}")
