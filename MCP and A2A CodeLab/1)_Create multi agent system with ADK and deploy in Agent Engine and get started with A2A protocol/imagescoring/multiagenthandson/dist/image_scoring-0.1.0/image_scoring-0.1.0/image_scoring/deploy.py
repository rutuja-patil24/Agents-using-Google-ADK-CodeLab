# Change the content of the following. Look for #change this comment
import vertexai
from .agent import root_agent
import os
import glob # To easily find the wheel file

PROJECT_ID = "the-byway-473000-u5"  # ✅ your project
LOCATION = "us-central1"            # ✅ region
STAGING_BUCKET = "gs://next-demo-storage1-us-central1"  # ✅ new bucket

from vertexai import agent_engines

vertexai.init(
   project=PROJECT_ID,
   location=LOCATION,
   staging_bucket=STAGING_BUCKET,
)

remote_app = agent_engines.create(
   agent_engine=root_agent,
   requirements=open(os.path.join(os.getcwd(), "requirements.txt")).readlines()+["./dist/image_scoring-0.1.0-py3-none-any.whl"],#change this to your local location
   extra_packages=[
       "./dist/image_scoring-0.1.0-py3-none-any.whl", # change this to your location
   ]
)

print(remote_app.resource_name)