# -*- coding: utf-8 -*-
# vim: set ai et ts=4 sts=4 sw=4 syntax=python:

import json
import time
from Queue import Queue
from flask import Flask, request

app = Flask(__name__)

q = Queue(2)


@app.route("/mailgun/dispense", methods=["POST"])
def dispense():
    """ This function receives the webhook from Mailgun via a forward() route
    """

    text = request.form.get('stripped-text', "")
    subject = request.form.get('subject', "")

    q.put({"text": text, "subj": subject})
    return "ok"


@app.route("/mailgun/read", methods=["GET"])
def forward():
    """ This function dequeues the dispenser request and returns the message body
        and subject to the requester.
    """

    total_time = 0
    timeout = 0.05
    while total_time < 5:
        total_time += timeout
        time.sleep(timeout)
        try:
            item = q.get_nowait()
            if item:
                return json.dumps(item)
        except Exception as e:
            print e

    return json.dumps({})


def run():
    app.run("0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    run()
