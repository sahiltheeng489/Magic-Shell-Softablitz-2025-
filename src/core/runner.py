import subprocess

class CommandRunner:
    def run(self, command):
        # Run the system command and capture the output and error
        try:
            completed_process = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=True
            )
            return completed_process.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr
