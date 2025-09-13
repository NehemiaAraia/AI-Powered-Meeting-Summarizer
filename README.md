<p align="center">
  <h1 align="center">AI Powered Meeting Summarizer</h1>
  <p align="center">
    For this project, I built an AI-powered meeting summarizer using AWS services like Bedrock, Transcribe, Lambda, and S3. It automatically transcribes meeting audio and generates concise summaries with key discussion points, enabling teams to quickly catch up on missed meetings and reference important next steps.<br />
  </p>
</p>

## Features


- **Python**
- **Amazon Bedrock**
- **Amazon Transcribe**
- **AWS Lambda**
- **Amazon Cloudwatch**
- **Amazon S3**
- **AWS IAM**



## Step 1.
To begin this project, I created three S3 buckets: one for raw audio uploads, one for the Transcribed audio outputs, and one for the complete AI summaries. After, I built a dedicated IAM role with least-privilege permissions for S3, Transcribe, Bedrock, and CloudWatch Logs, ensuring that the automation ran securely.

<img width="3000" height="1700" alt="Audio to transcript bucket" src="https://github.com/user-attachments/assets/63cbaefd-bfd2-4539-ae05-351517986631" />


## Step 2
I created two Lambda functions to handle the workflow. The first Lambda function automatically triggers when a new audio file is uploaded to the bucket, passing it to Amazon Transcribe to generate a transcript. The second Lambda function takes the transcript and calls Amazon Bedrock to summarize the key points into a short, readable summary.



## Step 3
To simulate a real world example, I set up two IAM users. One user, representing a manager, had read and write access to the audio bucket so they could upload recordings. The other user, representing an employee, had read only access to the summaries bucket so they could view the final output but not upload anything. I tested this setup by logging in as the employee and confirming they could access the summary file but were denied upload permissions.



## Step 4
I later configured the first Lambda function to accept all audio file formats like .mp3, .wav, and more instead of being hardcoded to only allow .mp4 files which I orginally did, which made the system more flexible and realistic. After, I set up S3 event triggers so that uploading a file will automatically trigger the first Lambda function, and when a transcript is generated, it triggers the second Lambda function.

<img width="3024" height="1824" alt="transcripted audio" src="https://github.com/user-attachments/assets/51650eaa-5a0f-4691-a839-6b5f15b77a8e" />

## Step 5
For the first function, it took the uploaded audio file, validated it, and then called Amazon Transcribe’s StartTranscriptionJob API. The transcript output was saved in the transcript bucket. Once a transcript appeared in the bucket, the second Lambda function ran automatically. I included a custom summarization prompt within my lambda code that told Bedrock to output key decisions, action items, deadlines, and discussion points while filtering out unneccessary conversitation. The generated summary was then saved in the summaries bucket for review.



## Step 6
I uploaded a sample audio file to simulate a real meeting and observed the full process as it transcribed and summarized the recording before storing it in the summaries bucket. I then logged in as the employee IAM user to verify they could view the final summary file but could not upload anything, confirming the access controls worked as intended. To finalize the project, I applied S3 Block Public Access, enabled server-side encryption, and configured CloudTrail logging to track API activity and file access events, making the solution secure and audit ready.

<img width="3024" height="1708" alt="final result" src="https://github.com/user-attachments/assets/3bc7c152-8725-42c2-a9a3-da97e7bdf635" />







