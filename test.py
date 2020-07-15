As pointed out by @dtc the main problem was I was overlooking execution stopping on the flaskApp.run() line. From this post

Start a flask application in separate thread

the easy solution is to use a separate thread.

Complete working example:

server:

# server_and_cam.py

import numpy as np
import cv2
from flask import Flask, jsonify, request
import threading

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

flaskApp = Flask(__name__)

def main():

    threading.Thread(target=flaskApp.run).start()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        keyPress = cv2.waitKey(10)
        if keyPress == ord('q'):
            break
        # end if

    # end while

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
# end function

@flaskApp.route('/post_number', methods=['POST'])
def post_number():
    if request.json is None:
        print('error, request.json is None')
    # end if

    if not 'number' in request.json:
        print('error, \'number\' is not in request.json')
    # end if

    numReceived = request.json['number']
    print('numReceived = ' + str(numReceived))

    return jsonify({'number': numReceived}), 201
# end function

if __name__ == '__main__':
    main()
client:

# client.py

import requests
import json
import time

numToSend = 0

while True:
    time.sleep(1)

    # set the url
    url = 'http://localhost:5000/post_number'

    # configure headers
    headers = {'Content-type': 'application/json'}

    # build the data and put into json format
    data = {'number': str(numToSend)}
    data_json = json.dumps(data)

    # send message to server via POST
    response = requests.post(url, headers=headers, data=data_json)
    # print response code
    print('response = ' + str(response))

    numToSend += 1
# end while
