import subprocess


def run_command(command):

    try:

        result = subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.STDOUT,
            timeout=30
        )

        return result

    except subprocess.CalledProcessError as e:

        return f"COMMAND FAILED:\n{e.output}"

    except subprocess.TimeoutExpired:

        return "COMMAND TIMED OUT"