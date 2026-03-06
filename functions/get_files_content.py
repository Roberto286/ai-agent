from config import MAX_CHARS
from general_functions import check_directory

def get_file_content(working_directory, file_path):
    try:
        is_inside, is_dir, target_dir = check_directory(working_directory, file_path) 

        if is_inside == False:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')

        if is_dir:
            raise Exception(f'File not found or is not a regular file: "{file_path}"')

        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters"]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
