from flask import Blueprint, request
from server.service.deploy_utils.fs_deployer_util import deploy_local

deploy = Blueprint('deploy_utils', __name__)


@deploy.route('/is_alive', methods=['GET'])
def ping_service():
    """utility method used from the client to understood if the service is alive or not"""
    return "", 200


@deploy.route("/new_deploy", methods=['POST'])
def new_deploy():
    """
    Method invoked to trigger a new deploy.

        Expected payload:

        {
            "PROJECT_NAME":"My_Awsome_Project",
            "BASE64_ZIP": "base64 encoded .tar.gz file containing the project to deploy",
            "SET_AS_STARTUP_APPLICATION": True/False,
            "STARTUP-COMMAND":"python helloword.py (or wathever)",
            "ON_DEPLOY_REBOOT": True/False
        }

        This method will put the source code in a new folder named as the project_name in the configured deploy
        directory and will set up the startup script if needed.
        Nb. the deploy directory is the one in the config.py file

    """

    payload = request.get_json()

    # check if payload well formed
    validitycheck = payload is not None and 'PROJECT_NAME' in payload

    if validitycheck:

        # check flags
        set_as_startup_application = False
        if 'SET_AS_STARTUP_APPLICATION' in payload:
            set_as_startup_application = payload['SET_AS_STARTUP_APPLICATION']

        on_deploy_reboot = False
        if 'ON_DEPLOY_REBOOT' in payload:
            on_deploy_reboot = payload['ON_DEPLOY_REBOOT']

        # deploy_utils content
        result = deploy_local(payload['PROJECT_NAME'], payload['STARTUP-COMMAND'], payload['BASE64_ZIP'],
                              set_as_startup_application, on_deploy_reboot)

        if result:
            return "", 200
        else:
            return "", 400
