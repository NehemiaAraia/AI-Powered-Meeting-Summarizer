import boto3
import json
s3 = boto3.client('s3')
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)
def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    print(f"Processing file: {file_key} from bucket: {bucket_name}")
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = obj['Body'].read().decode('utf-8')
    if file_key.endswith('.json'):
        transcript_data = json.loads(file_content)
        print("Transcript data structure:", json.dumps(transcript_data, indent=2))
        transcript_text = transcript_data['results']['transcripts'][0]['transcript']
    elif file_key.endswith('.txt'):
        transcript_text = file_content
    else:
        raise ValueError(f"Unsupported file type: {file_key}")
    prompt = f"""Human: Analyze this meeting transcript and provide a structured summary following these guidelines:
1. Key Decisions: List the main decisions made
2. Action Items: List specific tasks assigned and their owners
3. Important Deadlines: Highlight any mentioned deadlines or dates
4. Main Discussion Points: Summarize the core topics discussed
5. Follow-up Items: Note any items requiring future discussion
Please format the output clearly with headers and bullet points. Remove any small talk, greetings, or irrelevant chitchat.
Transcript:
{transcript_text}\n\nAssistant:"""
    response = bedrock_runtime.invoke_model(
        modelId='anthropic.claude-v2',
        body=json.dumps({"prompt": prompt, "max_tokens_to_sample": 500}),
        contentType='application/json',
        accept='application/json'
    )
    summary_output = json.loads(response['body'].read().decode())
    summary_text = summary_output['completion']
    output_filename = file_key.split('.')[0] + '-summary.txt'
    s3.put_object(
        Bucket='summarized-meeting-test',
        Key=output_filename,
        Body=summary_text.encode('utf-8')
    )
    return {
        'statusCode': 200,
        'body': f'Summary saved successfully for {file_key}'
    }
