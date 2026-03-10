def review_and_complete(entities):
    # Fields we expect, with fallback to empty string if not found
    fields = {
        "nombres":    entities.get("nombres", ""),
        "apellidos":  entities.get("apellidos", ""),
        "numero":     entities.get("numero", ""),
        "nacimiento": entities.get("nacimiento", ""),
        "sexo":       entities.get("sexo", ""),
        "plan":       entities.get("plan", "")
    }

    print("\n--- Review client data (press Enter to keep current value) ---\n")

    reviewed = {}
    for field, current_value in fields.items():
        user_input = input(f"{field}: [{current_value}] ")
        reviewed[field] = user_input if user_input.strip() != "" else current_value

    return reviewed


# Test
if __name__ == "__main__":
    from extract_id import get_document, extract_entities

    document = get_document("WhatsApp Image 2026-02-28 at 11.25.49.jpeg")
    entities = extract_entities(document)
    verified_data = review_and_complete(entities)

    print("\n--- Verified data ---")
    for key, value in verified_data.items():
        print(f"{key}: {value}")
