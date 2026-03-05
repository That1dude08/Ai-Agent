import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        dir_list = os.listdir(target_dir)

        files_info = []

        for filename in dir_list:
            joint_path = os.path.join(target_dir, filename)
            file_size = os.path.getsize(joint_path)
            dir_check = os.path.isdir(joint_path)
            answer_string = f"- {filename}: file_size={file_size} bytes, is_dir={dir_check}"
            files_info.append(answer_string)
        results = "\n".join(files_info)
        return results
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
        ),
    )
    