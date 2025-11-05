import requests
from ..aws.ssm.parameter_store import get_valid_token

def summarize_text(text: str) -> str:
    hugging_face_token = get_valid_token("HUGGINGFACE_TOKEN")
    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers={"Authorization": f"Bearer {hugging_face_token}"},
        json={"inputs": text},
    )
    try:
        return response.json()[0]["summary_text"]
    except Exception:
        return "Error generating summary."
