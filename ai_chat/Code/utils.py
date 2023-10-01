
def extract_from_response(output: str):
    """
    Extracts primary intent, secondary intent, entities, and specialist agent from the raw LLM output.
    """
    lines = output.strip().split("\n")
    extracted_data = {
        "primary_intent": "",
        "secondary_intent": [],
        "entities": [],
        "specialist_agent": ""  # New field
    }

    for line in lines:
        if "Primary Intent:" in line:
            extracted_data["primary_intent"] = line.split("Primary Intent:")[1].strip()
        elif "Secondary Intent:" in line:
            # Splitting by comma to extract multiple secondary intents, if present
            secondary_intents = line.split("Secondary Intent:")[1].strip().split(", ")
            extracted_data["secondary_intent"] = [intent.strip() for intent in secondary_intents]
        elif "Entities:" in line:
            entities = line.split("Entities:")[1].strip().split(", ")
            extracted_data["entities"] = [entity.strip() for entity in entities]
        elif "Specialist Agent:" in line:  # New condition
            extracted_data["specialist_agent"] = line.split("Specialist Agent:")[1].strip()

    #logger.info(f"Extracted primary intent: {extracted_data['primary_intent']}, secondary intent: {extracted_data['secondary_intent']}, entities: {extracted_data['entities']}, specialist agent: {extracted_data['specialist_agent']}.")
    return extracted_data