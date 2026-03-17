import os, argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
	raise RuntimeError("No key found.")

parser = argparse.ArgumentParser(description="Weaver")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("user_prompt", type=str, help="Please enter prompt")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
	model='gemini-2.5-flash',
	contents=messages,
	config=types.GenerateContentConfig(
		tools=[available_functions],
		system_instruction=system_prompt,
		temperature=0
	)
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

def main():
	if not response.usage_metadata:
		raise RuntimeError("Likely failed API request. Try again later?")
	verbose=args.verbose	

	if verbose:
		print(f"User prompt: {args.user_prompt}")
		print(f"Prompt tokens: {prompt_tokens}")
		print(f"Response tokens: {response_tokens}")
		
	else:
		print(response.text)

	function_results_list = []
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
		function_results_list.append(result.parts[0])

if __name__ == "__main__":
    main()
