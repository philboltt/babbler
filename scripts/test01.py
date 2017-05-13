# coding=utf-8
import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

text_to_speech = TextToSpeechV1(
    username='8e026862-5979-4d19-99df-148e233cf27c',
    password='y0KU6bWAmYNb',
    x_watson_learning_opt_out=True)  # Optional flag

print(json.dumps(text_to_speech.voices(), indent=2))

with open(join(dirname(__file__), '../resources/output.wav'),
          'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize('Hello fellow future realities robots.  What are you doing with your hololens.', accept='audio/wav',
                                  voice="en-GB_KateVoice"))

print(
    json.dumps(text_to_speech.pronunciation(
        'Watson', pronunciation_format='spr'), indent=2))

print(json.dumps(text_to_speech.customizations(), indent=2))