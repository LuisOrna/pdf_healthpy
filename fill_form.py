import pypdf

def fill_pdf(processed_data, input_pdf, output_pdf):
    reader = pypdf.PdfReader(input_pdf)
    writer = pypdf.PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[0], processed_data)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Done! Check {output_pdf}")