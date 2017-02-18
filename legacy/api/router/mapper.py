from legacy.api.handler.job_handler import Job, JobList


mappers = [
    (JobList, '/api/v1.0/jobs'),
    (Job, '/api/v1.0/jobs/<string:id>'),
]
