import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from available_functions import available_functions, call_function
from prompts import system_prompt


_ = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
parser = argparse.ArgumentParser(description="Chatbot")
_ = parser.add_argument("user_prompt", type=str, help="User prompt")
_ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

if api_key is None:
    raise RuntimeError("Put your api_key in .env")

def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    res_from_ai = client.models.generate_content(contents=messages, model=model, config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions ]))
   
    if res_from_ai.usage_metadata == None:
        raise RuntimeError("No usage metadata in ai response")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {res_from_ai.usage_metadata.prompt_token_count}")
        print(f"Response tokens: { res_from_ai.usage_metadata.candidates_token_count }")

    if res_from_ai.function_calls:
        print(res_from_ai.function_calls)
        for fc in res_from_ai.function_calls:
            function_call_result = call_function(fc, args.verbose)

            if not function_call_result.parts:
                raise Exception("No valid parts in function_call_result")
            
            if not function_call_result.parts[0].function_response:
                raise Exception("function_response is None") 

            if not function_call_result.parts[0].function_response.response:
                raise Exception("response is None")

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(res_from_ai.text)

if __name__ == "__main__":
    main()
