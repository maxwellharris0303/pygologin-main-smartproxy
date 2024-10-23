import whisper
import re
import aiohttp
import tempfile
import asyncio
from selenium_driverless import webdriver
from selenium_driverless.webdriver import Chrome, Target
from selenium_driverless.types.by import By
from selenium_driverless.types.webelement import NoSuchElementException
import typing

# audio_file_path = "tmp3xjhmx2l.wav"
# print('Audio path is: ' + audio_file_path)

# use whisper to transcribe speech to text
import whisper

model = whisper.load_model("base")
result = model.transcribe("123.wav", fp16=False)
matches = re.findall(r'\d', result['text'])
solution = matches[-6:]
print(solution)
