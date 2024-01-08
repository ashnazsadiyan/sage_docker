from fastapi import FastAPI, Response
from pydub import AudioSegment
import subprocess
import whisper
from sentence_transformers import SentenceTransformer, util
import os
import asyncio

app = FastAPI()


#  functions
# class Question:
#     def __init__(self, answer: str, start_time: float, end_time: float):
#         self.answer = answer
#         self.start_time = start_time
#         self.end_time = end_time
#         self.expected = ""
#         self.given = ""
#         self.result = 0


async def get_audio(start_time: float, end_time: float, _id: str, identification: str, ):
    audio = await AudioSegment.from_file(f'{identification}.WAV')
    audio_segment = audio[start_time:end_time]
    extracted_file = f"{_id}.mp3"
    audio_segment.export(extracted_file, format='mp3')


async def get_text(file_name: str):
    model = await whisper.load_model("base")
    result = model.transcribe(file_name, fp16=False)
    return result["text"]


# def check_text(expected_answer: str, given_answer: str, question: str):
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     embeddings = model.encode([expected_answer, given_answer], convert_to_tensor=True)
#     cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
#     similarity_score = cosine_score.item()
#     print(f"Similarity Score for question {question}: {similarity_score}")
#     return similarity_score


async def get_score():
    # result = check_text(
    #     "Regularization is a technique that adds a penalty term to the objective function of a machine learning algorithm. It is used to prevent overfitting and to encourage the model to find a simpler and more generalizable solution.",
    #     audio_text, "What is regularization in machine learning?")
    # print(result, 'result')
    print("starting to download")
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', '-i',
        'https://d8cele0fjkppb.cloudfront.net/ivs/v1/624618927537/y16bDr6BzuhG/2023/12/14/11/3/0lm3JnI0dvgo/media/hls/master.m3u8',
        '-b:a', '64k', '657ae0c1ec9a6e346d803180.WAV',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await get_audio(0, 168136, '657ae0c1ec9a6e346d8031901', '657ae0c1ec9a6e346d803180')
    audio_text = await get_text("657ae0c1ec9a6e346d8031901.mp3")
    return f"result-text - f{audio_text}"


@app.get('/ping')
def pint():
    return {"pong": "pong"}


@app.post('/invocations')
async def invoke(response: Response):
    try:
        resulted_text = await get_score()
        return {"testing": resulted_text}
    except Exception as e:
        print(e)
        response.status_code = 500
        return {"message": e}
