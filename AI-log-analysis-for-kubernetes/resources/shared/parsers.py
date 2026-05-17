import re


def extract_events_section(describe_output):

    match = re.search(
        r"Events:\n(.*)",
        describe_output,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return "No Events section found"