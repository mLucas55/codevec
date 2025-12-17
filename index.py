from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)