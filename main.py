import os
import sys
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
    for _ in range(20):
        res_from_ai = client.models.generate_content(
            contents=messages,
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )

        if res_from_ai.candidates:
            for candidate in res_from_ai.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not res_from_ai.usage_metadata:
            raise RuntimeError("No usage metadata in ai response")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {res_from_ai.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {res_from_ai.usage_metadata.candidates_token_count}"
            )

        if not res_from_ai.function_calls:
            print("Response:")
            print(res_from_ai.text)
            return

        if res_from_ai.function_calls:
            print(res_from_ai.function_calls)
            function_responses = []

            for function_call in res_from_ai.function_calls:
                result = call_function(function_call, args.verbose)
                if (
                    not result.parts
                    or not result.parts[0].function_response
                    or not result.parts[0].function_response.response
                ):
                    raise RuntimeError(
                        f"Empty function response for {function_call.name}"
                    )
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
                function_responses.append(result.parts[0])

            messages.append(types.Content(role="user", parts=function_responses))

    sys.exit(1)


if __name__ == "__main__":
    main()
