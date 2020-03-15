from datetime import timedelta
from timeloop import Timeloop
import logging
from service.config import DEPLOYED_APP_FILE,DEPLOY_FOLDER,LOGGER_LEVEL
import os

time_loop = Timeloop()
running_jobs = {}
WORKING_DIR = os.getcwd()
logger = logging.getLogger("service")


@time_loop.job(interval=timedelta(seconds=10))
def check_startup_jobs():
    """Run all projects that are not yet in running state.
    This function read the app_list file and check periodically if there are new projects to boot"""

    #open the jobs file and export the list of the new jobs
    job_file = open(DEPLOYED_APP_FILE, "r")
    job_file_content = job_file.read()
    all_jobs = {}
    if job_file_content:
        all_jobs = eval(job_file_content)

    # select the missing jobs to run
    job_to_run = {k: all_jobs[k] for k in set(all_jobs) - set(running_jobs)}

    # for each new job, execute the startup command
    for key in job_to_run:
        try:
            logger.info("starting job: "+ key + " | With command: "+ job_to_run[key])
            #cahnge directory to deploy directory and execute the given startup command
            os.chdir(os.path.join(DEPLOY_FOLDER, key))
            os.system(job_to_run[key] + " &")
            os.chdir(WORKING_DIR)
            running_jobs[key] = job_to_run[key]
        except Exception as err:
            logger.error("Failed to run job: "+job_to_run[key]+" error message: "+str(err))


