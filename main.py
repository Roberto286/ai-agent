import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"

if api_key is None:
    raise RuntimeError("Put your api_key in .env")

def main():
    res_from_ai = client.models.generate_content(contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.", model=model)
   
    if res_from_ai.usage_metadata == None:
        raise RuntimeError("No usage metadata in ai response")

    print(f"Prompt tokens: {res_from_ai.usage_metadata.prompt_token_count}")
    print(f"Response tokens: { res_from_ai.usage_metadata.candidates_token_count }")
    print(res_from_ai.text)

if __name__ == "__main__":
    main()
