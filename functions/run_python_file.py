import os
import subprocess
schema_run_python_file= {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "required":["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "filepath to python file",
                },
                "args":{
                    "type": "array",
                    "items":{
                        "type":"string",
                    },
                    "description": "arguments to pass onto the python file",
                }

            },
        },
    },
}
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_dir)== False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.endswith(".py")== False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        Completed_Process = subprocess.run(command,cwd=working_dir_abs,capture_output=True,text=True,timeout=30)
        output = []
        if Completed_Process.returncode != 0:
            output.append(f"Process exited with code {Completed_Process.returncode}")
        if Completed_Process.stderr=="" and Completed_Process.stdout == "":
            output.append("No output produced")
        if Completed_Process.stderr!="":
            output.append(f"STDERR:{Completed_Process.stderr}")
        if Completed_Process.stdout != "":
            output.append(f"STDOUT:{Completed_Process.stdout}")
        return '\n'.join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
