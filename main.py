import os
from dotenv import load_dotenv
from google import genai
import argparse

from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

if api_key is None:
    raise RuntimeError("Put your api_key in .env")

def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    res_from_ai = client.models.generate_content(contents=messages, model=model)
   
    if res_from_ai.usage_metadata == None:
        raise RuntimeError("No usage metadata in ai response")

    print(f"Prompt tokens: {res_from_ai.usage_metadata.prompt_token_count}")
    print(f"Response tokens: { res_from_ai.usage_metadata.candidates_token_count }")
    print(res_from_ai.text)

if __name__ == "__main__":
    main()
