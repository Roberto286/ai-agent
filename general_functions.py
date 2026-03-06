import os


def is_outside_working_directory(working_directory, directory):
    working_dir_abs = os.path.abspath(working_directory)
    
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))    
        
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs


    return valid_target_dir, os.path.isdir(target_dir), target_dir

        
