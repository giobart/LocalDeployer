import base64
import os.path
import os
import tarfile
import logging
from service.config import DEPLOY_FOLDER,DEPLOYED_APP_FILE, DEPLOY_FOLDER

logger = logging.getLogger("service")
WORKING_DIR = os.getcwd()


def deploy_local(
        project_name,
        startup_command,
        content_zip_file,
        set_as_startup_application=False,
        on_deploy_reboot=False):
    decoded_file_string = base64.b64decode(content_zip_file)
    CURR_PATH = os.path.join(DEPLOY_FOLDER, project_name)

    logger.info("Deploy of app: " + project_name + " STARTED")

    try:
        os.mkdir(CURR_PATH)
    except:
        logger.info('Found Project with same name, OVERRIDING')

    FILE_PATH = os.path.join(CURR_PATH, "codezip.tar.gz")

    # decode and write the package into the deploy folder
    with open(FILE_PATH, "wb+") as zip_file:
        zip_file.write(decoded_file_string)

    # unzip the package
    logger.debug("UNZIPPING BASE64 PORJECT INTO " + CURR_PATH)
    tar = tarfile.open(FILE_PATH, "r:gz")
    tar.extractall(path=CURR_PATH)
    tar.close()

    # Set as startup app: add application into app_list file inside startup_app folder
    if set_as_startup_application:
        logger.info("Setting application as startup application")

        try:
            os.mkdir(DEPLOY_FOLDER)
        except:
            logger.debug('Tried to create new startup_app folder, but was already present.')

        with open(DEPLOYED_APP_FILE, "r+") as app_list_file:
            app_list_string = app_list_file.read()
            new_line = {project_name: startup_command}
            if app_list_string:
                app_dict = eval(app_list_string)
                app_dict.update(new_line)
                app_list_file.truncate(0)
                app_list_file.seek(0)
                app_list_file.write(str(app_dict))
            else:
                app_list_file.write(str(new_line))

    # On deploy reboot
    if on_deploy_reboot:
        logging.info("Rebooting the system")
        os.system('sudo shutdown -r now')

    return True


def deploy_list():
    """create a list of deployd app from the app_list.txt file"""
    apps = {}

    logging.info("Generating app list")

    # read all deployed app and give an index
    with open(DEPLOYED_APP_FILE, "r") as app_list_file:
        app_list = eval(app_list_file.read())
        if app_list:
            for key, val in enumerate(app_list, start=0):
                apps[key] = val

    logging.info(str(apps))
    return apps


def deploy_delete(id):
    """remove the project n. <id>, the id is given by the order of the project name in the app_list file"""

    project_name = ""

    # open app_list file
    with open(DEPLOYED_APP_FILE, "r+") as app_list_file:
        app_list = eval(app_list_file.read())

        # extract project n. id
        project_name = list(app_list.keys())[id]
        logging.info("Deleting project: ["+project_name+"]")

        # remove the project folder
        os.chdir(DEPLOY_FOLDER)
        os.system("rm -rf "+project_name)
        os.chdir(WORKING_DIR)

        # remove entry in the file
        del app_list[project_name]
        app_list_file.truncate(0)
        app_list_file.seek(0)
        app_list_file.write(str(app_list))