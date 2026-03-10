#Dependencies
import pypdf

#Reading
reader = pypdf.PdfReader("djs_a.pdf")
fields = reader.get_fields()

for field_name in fields:
    print(field_name)
    