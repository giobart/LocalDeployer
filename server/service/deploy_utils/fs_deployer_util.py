import base64
import os.path
import tarfile

from server.service.config import DEPLOY_FOLDER


def deploy_local(
        project_name,
        startup_command,
        content_zip_file,
        set_as_startup_application=False,
        on_deploy_reboot=False):
    decoded_file_string = base64.b64decode(content_zip_file)
    CURR_PATH = os.path.join(DEPLOY_FOLDER, project_name)
    FILE_PATH = os.path.join(CURR_PATH, "codezip.tar.gz")

    # decode and write the package into the deploy folder
    with open(FILE_PATH, "w") as zip_file:
        zip_file.write(decoded_file_string)

    # unzip the package
    tar = tarfile.open(FILE_PATH, "r:gz")
    tar.extractall()
    tar.close()

    # Set as startup app
    if set_as_startup_application:
        with open("startup_app/app_list.txt", "w+") as app_list:
            app_list = app_list.read()
            new_line = {project_name: startup_command}
            if not app_list:
                app_dict = eval(app_list)
                app_dict.update(new_line)
                app_list.write(str(app_dict))
            else:
                app_list.write(str(new_line))

    #On deploy reboot
    #TODO