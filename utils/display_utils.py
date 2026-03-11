def print_verbose_output(args, res_from_ai):
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
