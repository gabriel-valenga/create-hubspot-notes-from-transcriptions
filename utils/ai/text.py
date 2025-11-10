import requests
from utils.aws.ssm.parameter_store import parameter_store

def summarize_text(text: str) -> str:
    hugging_face_token = parameter_store.get_valid_token("HUGGINGFACE_TOKEN")
    response = requests.post(
        "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers={"Authorization": f"Bearer {hugging_face_token}"},
        json={"inputs": text},
    )
    try:
        return response.json()[0]["summary_text"]
    except Exception:
        return "Error generating summary."
