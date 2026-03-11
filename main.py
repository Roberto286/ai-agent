import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from available_functions import available_functions, call_function
from config import DEFAULT_MODEL, MAX_CONVERSATION_TURNS
from prompts import system_prompt


def configure_chatbot():
    """Configures the chatbot, loads environment variables, and parses arguments."""
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in .env file.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot powered by Google Gemini.")
    parser.add_argument(
        "user_prompt", type=str, help="The initial user prompt for the chatbot."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output to show token counts and function responses.",
    )

    args = parser.parse_args()

    return client, DEFAULT_MODEL, args


def _print_verbose_output(args, res_from_ai):
    """Prints verbose output if enabled."""
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if res_from_ai.usage_metadata:
            print(f"Prompt tokens: {res_from_ai.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {res_from_ai.usage_metadata.candidates_token_count}"
            )
        else:
            print("No usage metadata available.")


def main():
    client, model_name, args = configure_chatbot()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for turn in range(MAX_CONVERSATION_TURNS):
        res_from_ai = client.models.generate_content(
            contents=messages,
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )

        if not res_from_ai.candidates:
            print("No candidates returned from AI. Ending conversation.")
            break

        candidate_content = res_from_ai.candidates[
            0
        ].content  # Assuming we always take the first candidate
        if candidate_content:
            messages.append(candidate_content)

        _print_verbose_output(args, res_from_ai)

        if not res_from_ai.function_calls:
            print("Response:")
            print(res_from_ai.text)
            return  # Conversation ends with a text response

        # Handle function calls
        function_responses = []
        for function_call in res_from_ai.function_calls:
            print(
                f"Calling function: {function_call.name} with args: {function_call.args}"
            )
            result = call_function(function_call, args.verbose)

            # Check if result parts and function response are valid
            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                print(
                    f"Warning: Empty or invalid function response for {function_call.name}. Skipping."
                )
                continue  # Skip this function response and continue if others are present

            function_response_part = result.parts[0]
            if args.verbose:
                print(
                    f"-> Function response: {function_response_part.function_response.response}"
                )
            function_responses.append(function_response_part)

        if function_responses:  # Only append if there were valid function responses
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print("No valid function responses were generated. Ending conversation.")
            break  # No valid function responses, so we can't continue the conversation meaningfully

    print(
        f"Exceeded maximum conversation turns ({MAX_CONVERSATION_TURNS}). Ending conversation."
    )
    sys.exit(1)  # Indicate an abnormal exit if max turns reached without a clear end


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
