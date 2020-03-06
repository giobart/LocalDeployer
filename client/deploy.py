import requests
import tarfile
import os
import base64
import sys, getopt
from tabulate import tabulate
from config import TARGET_FOLDER,REMOTE_MACHINES

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


def print_help():
    print("_.-^-._.-*> Local Deployer <*-._.-^-._")
    print("Usage:")
    print("#deploy project in the folder <input-folder> into remote machine with id <remote-di>")
    print("deploy.py -i <input-folder> -r <remote-id>")
    print("#list all the current configured remote machines")
    print("deploy -l")
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

    for opt, arg in opts:
        if opt == '-h':
            print_help()

        # If -l (list) argument, give configured device list from config file
        if opt == '-l':
            print("####### Remote configured machines #######")
            print(tabulate(enumerate(REMOTE_MACHINES, start=0), headers=['Remote Id', 'Hostname/IP']))
            exit()

        # Save input deploy folder and output remote machine
        elif opt == '-i':
            deploy_folder = arg
        elif opt == '-r':
            deploy_machine = arg

    if deploy_folder and deploy_folder:
        print(" ")
        print("_.-^-._.-*> Local Deployer <*-._.-^-._")
        print(tabulate([["Deploy of the project : ", deploy_folder], ["Deploy machine: ", REMOTE_MACHINES[int(deploy_machine)]]]))
        # TODO: call deploy function
    else:
        print("You must give -i (input folder) and -r (remote machine)")
        print_help()



if __name__ == "__main__":
    main(sys.argv[1:])
