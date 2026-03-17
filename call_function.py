
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
	function_declarations=[
		schema_get_files_info,
		schema_get_file_content,
		schema_run_python_file,
		schema_write_file
	]
)

def call_function(function_call, verbose=False):
	function_name=function_call.name or ""
	function_map = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python_file": run_python_file,
		"write_file": write_file
	}
	functions=function_map

	args=dict(function_call.args) if function_call.args else {}
	args["working_directory"]="./calculator"

	if function_name not in functions:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Unknown function: {function_name}"},
				)
			],
		)


	if verbose:
		print(f"Calling function: {function_call.name}({function_call.args})")
	else:
		print(f" - Calling function: {function_call.name}")

	function_result=functions[function_name](**args)
	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
			name=function_name,
			response={"result": function_result},
			)
		],
	)
