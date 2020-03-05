import requests
import tarfile
import os
import base64
from config import TARGET_FOLDER

deploy_new = {
    "PROJECT_NAME": "",
    "BASE64_ZIP": "",
    "SET_AS_STARTUP_APPLICATION": False,
    "STARTUP-COMMAND": "",
    "ON_DEPLOY_REBOOT": False
}


def execute_deploy(project_name, file_path, set_as_startup_application, startup_command, on_deploy_reboot, receiver):
    # zip the project folder
    tar_path = os.path.join(TARGET_FOLDER, project_name) + ".tar.gz"
    os.system("rm " + tar_path)  # delete tar if already present
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(file_path, arcname=os.path.basename(file_path))
    tar_file = open(tar_path, "rb")

    # encode zip as base64
    encoded = base64.b64encode(tar_file.read()).decode("utf-8")

    # build request json
    deploy_new["BASE64_ZIP"] = encoded
    deploy_new["PROJECT_NAME"] = project_name
    deploy_new["SET_AS_STARTUP_APPLICATION"] = set_as_startup_application
    deploy_new["STARTUP-COMMAND"] = startup_command
    deploy_new["ON_DEPLOY_REBOOT"] = on_deploy_reboot

    # send request
    print(deploy_new)
    response = requests.post(url=receiver, json=deploy_new)
    print(str(response))


if __name__ == "__main__":
    execute_deploy(
        project_name="test",
        file_path="<Path to file>",
        set_as_startup_application=True,
        startup_command="<startup command>",
        on_deploy_reboot=False,
        receiver="http://0.0.0.0:20002/new_deploy"
    )
