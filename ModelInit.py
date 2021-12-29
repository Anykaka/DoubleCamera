import SonyCommand


def model_init(sony_command):
    sony_command.sony_command("getFNumber")  # 以下三个都是命令
    sony_command.sony_command("getIsoSpeedRate")
    sony_command.sony_command("getShutterSpeed")

    sony_command.sony_command("getAvailableFNumber")  # 以下三个都是命令
    sony_command.sony_command("getAvailableIsoSpeedRate")
    sony_command.sony_command("getAvailableShutterSpeed")
