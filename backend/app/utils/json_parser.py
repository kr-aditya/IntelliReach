import json


def parse_llm_json(raw_output: str) -> dict:
    """
    Parse JSON returned by an LLM.

    Handles common formatting problems such as
    markdown code fences and surrounding text.
    """

    if not raw_output:
        raise ValueError("LLM returned empty output.")

    text = raw_output.strip()

    # ---------------------------------------------------------
    # Remove markdown code fences
    # ---------------------------------------------------------

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # ---------------------------------------------------------
    # Try direct JSON parsing
    # ---------------------------------------------------------

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # ---------------------------------------------------------
    # Try extracting the outer JSON object
    # ---------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]

        try:
            return json.loads(candidate)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"LLM returned malformed JSON: {error}"
            ) from error

    raise ValueError(
        "LLM output did not contain a valid JSON object."
    )