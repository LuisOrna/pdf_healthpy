from google.cloud import documentai
import os


MIME_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "pdf": "application/pdf",
}


def get_document(image_path):
    client = documentai.DocumentProcessorServiceClient()
    processor_name = "projects/200035178392/locations/us/processors/90b68fbc0cdfb602"

    ext = image_path.rsplit(".", 1)[-1].lower()
    mime_type = MIME_TYPES.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_content = f.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=mime_type
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


