import os


def get_file_info(working_directory, directory):
    try:
        working_dir_abs = os.path.abspath(working_directory)
    
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))    
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'

        results = [f"Result for '{directory}' directory:"] 
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            results.append(f"- {item}: file_size={size}, is_dir={is_dir}")

        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"
