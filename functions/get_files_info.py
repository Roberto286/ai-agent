import os

from general_functions import check_directory


def get_file_info(working_directory, directory):
    try:
        is_inside, is_dir, target_dir = check_directory(working_directory, directory) 
        results = [f"Result for '{directory}' directory:"] 
 
        if is_inside == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if is_dir == False: 
            return f'Error: "{target_dir}" is not a directory'


        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            results.append(f"- {item}: file_size={size}, is_dir={is_dir}")

        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"
