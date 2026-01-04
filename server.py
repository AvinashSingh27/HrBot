from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from clients.rq_client import queue
from queues.worker import process_query



app= FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get('/')
def root():
    return {"status":'Server is up and runnign'}

 
@app.post('/chat') # Let decorate the function
def chat(
        query: str = Query(..., description="The chat query of user")
):
    # We nned to enqueue this query into the queue
    job = queue.enqueue(process_query,query)   # this is not the result this is the id of the job, you simply said go into the line
    return {"status":"queued","job_id":job.id}  # this job might be in queueu or might be in processing state

@app.post('/job-status') 
def get_result(
        job_id: str = Query(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}