from flask import Blueprint, request
from server.service.deploy_utils.fs_deployer_util import deploy_local

deploy = Blueprint('deploy_utils', __name__)



@deploy.route('/is_alive',methods=['GET'])
def ping_service():
    #utility method used from the client to understood if the service is alive or not
    return 200

@deploy.route("/new_deploy",methods=['POST'])
def new_deploy():

    payload = request.get_json()

    #check if payload well formed
    validitycheck = payload is not None and 'PROJECT_NAME' in payload

    if validitycheck:

        #check flags
        set_as_startup_application = False
        if 'SET_AS_STARTUP_APPLICATION' in payload:
            set_as_startup_application=True

        on_deploy_reboot = False
        if 'ON_DEPLOY_REBOOT' in payload:
            on_deploy_reboot=True


        #deploy_utils content
        result = deploy_local(payload['PROJECT_NAME'],payload['STARTUP-COMMAND'],payload['BASE64_ZIP'],set_as_startup_application,on_deploy_reboot)

        if result:
            return 200
        else:
            return 400
