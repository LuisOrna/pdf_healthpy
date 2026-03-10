from extract_id import get_document, extract_entities
from review_data import review_and_complete
from process_data import process
from fill_form import fill_pdf

# Step 1 - Extract
document = get_document("WhatsApp Image 2026-02-28 at 11.25.49.jpeg")
entities = extract_entities(document)

# Step 2 - Review
verified_data = review_and_complete(entities)

# Step 3 - Process
processed_data = process(verified_data)

# Step 4 - Fill PDF
fill_pdf(processed_data, "djs_a.pdf", "filled_form.pdf")