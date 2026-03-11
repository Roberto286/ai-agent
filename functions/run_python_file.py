import os
import subprocess

from google.genai import types
from general_functions import check_directory


def run_python_file(working_directory, file_path, args=None):
    try:
        is_inside, is_dir, target_dir = check_directory(working_directory, file_path)

        if is_inside == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_dir) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]

        if args and len(args):
            command.extend(args)

        completed = subprocess.run(command, timeout=30.00, text=True, cwd=working_directory, capture_output=True)

        result = ""

        if completed.returncode != 0:
            result += f"Process exited with code {completed.returncode}"

        if not completed.stdout and not completed.stderr:
            result += "No output produced"

        if completed.stdout:
            result += f"STDOUT: {completed.stdout}"

        if completed.stderr:
            result += f"STDERR: {completed.stderr}"
        
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file with optional args. Produces STDOUT and STDERR and program output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional args to give to the python program",
            ),

        },
    ),
)
