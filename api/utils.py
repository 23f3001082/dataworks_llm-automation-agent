def execute_shell(command):
    if "rm" in command or "delete" in command:
        raise PermissionError("Deletion operations are not allowed.")
    return subprocess.run(command, shell=True, capture_output=True, text=True)