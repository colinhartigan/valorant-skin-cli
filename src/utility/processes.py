import psutil

class Processes:

    @staticmethod
    def is_program_already_running():
        processes = []
        for proc in psutil.process_iter():
            processes.append(proc.name())

        if len([proc for proc in processes if proc == "valorant-skin-cli.exe"]) > 2:
            return True

        return False