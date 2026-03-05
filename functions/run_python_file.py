import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(abs_file_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif abs_file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
            command.extend(args) 

        completed_process = subprocess.run(
            command,              # the list you built: ["python", abs_file_path, ...]
            cwd=working_dir_abs,  # run from the working directory
            capture_output=True,  # capture stdout/stderr
            text=True,            # decode to strings
            timeout=30,           # seconds
        )
        output_parts = []

        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not completed_process.stdout and not completed_process.stderr:
            output_parts.append("No output produced")
        else:
            if completed_process.stdout:
                output_parts.append(f"STDOUT:\n{completed_process.stdout}")
            if completed_process.stderr:
                output_parts.append(f"STDERR:\n{completed_process.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python File",
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
        required=["file_path"]
        ),
    )