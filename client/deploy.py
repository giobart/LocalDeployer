import requests
import tarfile
import os
import base64
import sys, getopt
import json
from tabulate import tabulate
from config import TARGET_FOLDER, REMOTE_MACHINES, DEPLOY_DESCRIPTOR_NAME

deploy_new = {
    "PROJECT_NAME": "",
    "BASE64_ZIP": "",
    "SET_AS_STARTUP_APPLICATION": False,
    "STARTUP-COMMAND": "",
    "ON_DEPLOY_REBOOT": False
}


def send_deploy(project_name, file_path, set_as_startup_application, startup_command, on_deploy_reboot, receiver):
    """ Send the configured deploy files to a remote machine  """
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


def deploy(deploy_folder, deploy_machine):
    """ Read deploy descriptor of a given project and deploy it to the given machine.
    It calls send_deploy to contact the remote machine"""

    print(" ")
    print("_.-^-._.-*> Local Deployer <*-._.-^-._")

    # Fetch deploy descriptor file
    with open(os.path.join(deploy_folder, DEPLOY_DESCRIPTOR_NAME), "r") as deploy_descriptor_file:
        deploy_descriptor = json.loads(deploy_descriptor_file.read())
        project_name = deploy_descriptor['PROJECT_NAME']
        set_as_startup_application = deploy_descriptor['SET_AS_STARTUP_APPLICATION']
        startup_command = ""
        on_deploy_reboot = False
        if set_as_startup_application:
            startup_command = deploy_descriptor['STARTUP_COMMAND']
            on_deploy_reboot = deploy_descriptor['ON_DEPLOY_REBOOT']

    # Print deploy resume
    print(tabulate(
        [
            ["Deploy of the project: ", deploy_folder],
            ["Project Name: ", project_name],
            ["Deploy machine: ", deploy_machine]
        ]))

    # Send the deploy to remote machine
    send_deploy(
        project_name=project_name,
        file_path=deploy_folder,
        set_as_startup_application=set_as_startup_application,
        startup_command=startup_command,
        on_deploy_reboot=on_deploy_reboot,
        receiver=deploy_machine
    )


def print_help():
    print("_.-^-._.-*> Local Deployer <*-._.-^-._")
    print("Usage: \n")
    print("#deploy project in the folder <input-folder> into remote machine with id <remote-di>")
    print("deploy.py -i <input-folder> -r <remote-id> \n")
    print("#list all the current configured remote machines")
    print("deploy.py -l \n")
    print("#list all the deployed applications")
    print("deploy.py -a \n")
    print("#Delete a deploy in a remote machine")
    print("deploy.py -d <deploy-id> -r <remote-id> \n")
    print("_.-^-._.-*><*-._.-^-._.-*><*-._.-^-._")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:r:l")
    except getopt.GetoptError:
        print
        'deploy.py -i <input-folder> -r <remote-id>'
        sys.exit(2)

    deploy_folder = ""
    deploy_machine = -1
    list = False

    # Fetch command line argument
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            exit()

        # If -l (list) argument, give configured device list from config file
        if opt == '-l':
            print("####### Remote configured machines #######")
            print(tabulate(enumerate(REMOTE_MACHINES, start=0), headers=['Remote Id', 'Hostname/IP']))
            exit()

        # Save input deploy folder and output remote machine
        elif opt == '-i':
            deploy_folder = arg
        elif opt == '-r':
            deploy_machine = REMOTE_MACHINES[int(arg)]

    # If deploy folder and deploy machine given => start new deploy
    if deploy_folder and deploy_machine:
        deploy(deploy_folder, deploy_machine)
    # If deploy machine or deploy folder missing -> error
    else:
        print("You must give -i (input folder) and -r (remote machine)")
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
