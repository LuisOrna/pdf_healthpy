from google.cloud import documentai
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pdf2-488718-0bc3349786f4.json"

def get_document(image_path):
    client = documentai.DocumentProcessorServiceClient()
    processor_name = "projects/200035178392/locations/us/processors/90b68fbc0cdfb602"
    
    with open(image_path, "rb") as f:
        image_content = f.read()
    
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="image/jpeg"
    )
    
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )
    
    result = client.process_document(request=request)
    return result.document


def extract_entities(document):
    entities = {}
    for entity in document.entities:
        entities[entity.type_] = entity.mention_text
    return entities


# Test
if __name__ == "__main__":
    document = get_document("WhatsApp Image 2026-02-28 at 11.25.49.jpeg")
    entities = extract_entities(document)
    print(entities)