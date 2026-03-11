import os

from google.genai import types
from general_functions import check_directory


def write_file(working_directory, file_path, content):
    try: 
       is_inside, is_dir, target_dir = check_directory(working_directory, file_path)

       if is_inside == False:
           return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

       if is_dir:
           return f'Error: Cannot write to "{file_path}" as it is a directory'

       os.makedirs(os.path.dirname(target_dir), exist_ok=True)

       with open(target_dir, mode="w") as f:
           f.write(content)

       return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
       return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file at a given path with given content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory of the file to be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file",
            ),
 
        },
    ),
)
