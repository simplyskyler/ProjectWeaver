import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="Path to the file to write, relative to working directory",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="Text content to write to the file",
			),
		},
		required=["file_path", "content"],
	),
)

def write_file(working_directory, file_path, content):
	try:
		working_dir_abs = os.path.abspath(working_directory)
		target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
		if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		if os.path.isdir(target_path):
			return f'Error: Cannot write to "{file_path}" as it is a directory'
		os.makedirs(os.path.dirname(target_path), exist_ok=True)
		with open(target_path, "w") as file:
			file.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: {e}"
