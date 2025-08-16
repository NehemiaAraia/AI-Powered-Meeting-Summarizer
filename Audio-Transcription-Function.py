import json
import urllib.parse
import boto3
import uuid
transcribe = boto3.client('transcribe')
def lambda_handler(event, context):
    print("Lambda triggered. Event:", json.dumps(event))
    # Extract bucket and key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    print(f"Processing file: s3://{bucket}/{key}")

     # Add check for existing jobs here
    try:
        # Check if job already exists
        existing_jobs = transcribe.list_transcription_jobs(
            JobNameContains=key
        )
        if existing_jobs['TranscriptionJobSummaries']:
            print(f"Transcription job already exists for {key}")
            return {
                'statusCode': 200,
                'body': json.dumps(f"Transcription job already exists for {key}")
            }
        
    # Generate a unique job name to avoid collision
    job_name = f"transcription-{uuid.uuid4()}"
    # Input file S3 URI
    media_uri = f"s3://{bucket}/{key}"
    try:
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName='meeting-transcript-test'
        )
        print(f"Started Transcription Job: {job_name}")
        import pprint
        pprint.pprint(response)
    except Exception as e:
        print(f"Error starting transcription job: {str(e)}")
        raise e
    return {
        'statusCode': 200,
        'body': json.dumps(f"Transcription job '{job_name}' started successfully.")
    }
