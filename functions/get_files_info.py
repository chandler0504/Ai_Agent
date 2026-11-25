import os
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir== False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            output_list = []
            for filename in os.listdir(target_dir):
                filepath = os.path.join(target_dir,filename)
                name = filename
                file_size = os.path.getsize(filepath)
                is_dir = os.path.isdir(filepath)
                output_list.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
            output_str="\n".join(output_list)
            return output_str
        else:
            return f'Error: "{directory}" is not a directory'

    except Exception as e:
        return f"Error: {e}"
