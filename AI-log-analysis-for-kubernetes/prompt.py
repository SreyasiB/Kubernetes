from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable not set"
    )


client = genai.Client(
    api_key=api_key
)


def analyze_incident(data):

    prompt = f"""
    You are an expert Kubernetes SRE.

    Analyze this Kubernetes incident.

    RESOURCE TYPE:
    {data['resource_type']}

    RESOURCE DATA:
    {data['context']}

    Provide:
    1. Root cause in one line
    2. Suggested step by step fixes
    3. Exact kubectl commands
    4. Prevention recommendations
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


    return response.text