
class RunningJobs():
    """_summary_ : This class is used to store the running jobs in a list.
    """

    def __init__(self):
        self.running_jobs = []

    def add_job(self, job_name):
        self.running_jobs.append(job_name)

    def remove_job(self, job_name):
        self.running_jobs.remove(job_name)

    def get_jobs(self):
        return self.running_jobs
    
    def is_job_running(self, job_name):
        return job_name in self.running_jobs
    
    def get_job_count(self):
        return len(self.running_jobs)
    
    def singleton(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = cls()
        return cls.instance
    
    @classmethod
    def get_instance(cls):
        return cls.singleton(cls)
    
in_progress = RunningJobs.get_instance()