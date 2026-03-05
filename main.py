import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from google.genai import types
from functions.get_files_info import schema_get_files_info
from call_function import available_functions, call_function
from config import MAX_ITERS

##import prompts
##print("Loaded prompts from:", prompts.__file__)
##print("System prompt is:", repr(system_prompt))

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Key not found")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt,
            temperature=0,)
    )
    if response.usage_metadata is None:
        raise RuntimeError("Meta Data not found")
    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    if not response.function_calls:
        # no function calls, print text as normal
        print(response.text)
        return

    # there are function calls, iterate over them
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
