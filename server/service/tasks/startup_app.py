from datetime import timedelta
from timeloop import Timeloop
from server.service.config import DEPLOYED_APP_FILE
import os

time_loop = Timeloop()

running_jobs = {}


@time_loop.job(interval=timedelta(10))
def check_startup_jobs():
    """Run all projects that are not yet in running state"""

    #open the jobs file
    job_file = open(DEPLOYED_APP_FILE, "r")
    all_jobs = eval(job_file.read())

    # select the missing jobs to run
    job_to_run = {k: all_jobs[k] for k in set(all_jobs) - set(running_jobs)}

    # for each new job, execute the startup command
    for key in job_to_run:
        running_jobs[key] = job_to_run[key]
        os.system(job_to_run[key] + " &")

