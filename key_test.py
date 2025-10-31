from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
key = os.getenv("OPENAI_API_KEY", "")
print("[DEBUG] Using key:", key[:10], "...", key[-4:], "len=", len(key))

client = OpenAI(api_key=key)
try:
    models = client.models.list()
    print("OK: models listed =", len(models.data))
except Exception as e:
    print("ERROR:", e)
