import os
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    
    storage_client = storage.Client()
    
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        print(f"Uploading {source_file_name} to bucket {bucket_name}...")
        blob.upload_from_filename(source_file_name)
        print("Upload successful!")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Get configuration from Environment Variables
    # These will be set in the Kubernetes Deployment YAML
    BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    FILE_NAME = "hello_gke.txt"
    
    # 1. Create a quick dummy file to upload
    with open(FILE_NAME, "w") as f:
        f.write("Hello! This file was uploaded from a GKE Pod using Workload Identity.")

    # 2. Upload it
    if BUCKET_NAME:
        upload_blob(BUCKET_NAME, FILE_NAME, f"uploads/{FILE_NAME}")
    else:
        print("Error: GCS_BUCKET_NAME environment variable not set.")