# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, request

import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

text_to_speech = TextToSpeechV1(
        username='8e026862-5979-4d19-99df-148e233cf27c',
        password='y0KU6bWAmYNb',
        x_watson_learning_opt_out=True)  # Optional flag

voiceData = text_to_speech.voices()
voices = []
for voice in text_to_speech.voices()["voices"]:
    voices.append({"name":voice["name"],"description":voice["description"]})

import OSC

c = OSC.OSCClient()
c.connect(('127.0.0.1', 8001))

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):

    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

@app.route('/api/speak', methods=["POST"]) 
def GenerateWav():
    result = request.get_json()
    print "Attempting to convert '%s' to speech using voice '%s'"%(result['text'], result['voice'])
    with open(join('/Users/philboltt/src/babbler/static', 'output.wav'),'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(result["text"], accept='audio/wav', voice=result["voice"]))
    print "Audio file written to disk"

    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/speak/url")
    oscmsg.append('http://127.0.0.1/static/output.wav')
    c.send(oscmsg)

    print "OSC message dispatched"

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/voiceData')
def GetVoiceData():
    return jsonify(results=voiceData)

@app.route('/api/voices')
def GetVoices():
    return jsonify(results=voices)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=int(port))
