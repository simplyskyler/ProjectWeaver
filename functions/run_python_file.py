import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
	name="run_python_file",
	description="Executes a specified Python file within the working directory and returns its output",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="Path to the Python file to run, relative to the working directory",
			),
			"args": types.Schema(
				type=types.Type.ARRAY,
				items=types.Schema(
					type=types.Type.STRING,
				),
				description="Optional list of arguments to pass to the Python script",
			),
		},
		required = ["file_path"],
	),
)

def run_python_file(working_directory, file_path, args=None):
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
		valid_target = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

		if not valid_target:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

		if not os.path.isfile(target_path):
			return f'Error: "{file_path}" does not exist or is not a regular file'

		if not file_path.endswith(".py"):
			return f'Error: "{file_path}" is not a Python file'
		
		command = ["python", target_path]
		if args:
			command.extend(args)

		completed_sp = subprocess.run(
			command,
			capture_output=True,
			text=True,
			timeout=30
		)
		
		if completed_sp.returncode != 0:
			return f"Process exited with code {completed_sp.returncode}"
		
		if not completed_sp.stdout and not completed_sp.stderr:
			return f"No output produced"
		
		else:
			return f'STDOUT: {completed_sp.stdout}\nSTDERR: {completed_sp.stderr}'

	except Exception as e:
		return f"Error: executing Python file: {e}"
