import google.generativeai as genai
from utils.aws.ssm.parameter_store import parameter_store

class TextSummarizer():

    def __init__(self):
        genai_api_key = parameter_store.get_parameter("google_ai_studio_gen_api_key")
        genai.configure(api_key=genai_api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
        self.chat = self.model.start_chat()


    def summarize_text(self, text: str) -> str:
        response = self.chat.send_message(f"Summarize this text: {text}")
        print(response.text)
        return response.text

