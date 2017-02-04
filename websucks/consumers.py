from channels import Group
from channels.sessions import channel_session
import logging
import json
import uuid
from contest import lib

@channel_session
def ws_connect(message):
    prefix, contest_id, user_id = message['path'].strip('/').split('/')
    
    if user_id and user_id != "AnonymousUser":
        Group('user-' + user_id).add(message.reply_channel)
        message.channel_session['user-channel'] = user_id
        Group('user-' + user_id).send({'text': json.dumps({
            "response": "welcome to Cargo Space Challenge",
            "messageType": "info"
        })})
        Group('user-' + user_id).send({'text': json.dumps({
            "response": lib.getUserSubmission(user_id, contest_id),
            "messageType": "submissions"
        })})
        logging.info("%s joined", user_id)
    
    if contest_id:
        Group('contest-' + contest_id).add(message.reply_channel)
        message.channel_session['contest-channel'] = contest_id
        Group('contest-' + contest_id).send({'text': json.dumps({
            "response": "You are now subscribed to the contest submission channel",
            "messageType": "info"
        })})
        Group('contest-' + contest_id).send({'text': json.dumps({
            "response": lib.getAllSubmissions(contest_id),
            "messageType": "all_submissions"
        })})


@channel_session
def ws_disconnect(message):
    prefix, contest_id, user_id = message['path'].strip('/').split('/')
    if user_id and user_id != "AnonymousUser":
        user_id = message.channel_session['user-' + user_id]
        Group('user-'+user_id).discard(message.reply_channel)
        logging.info("%s left", user_id)
    if contest_id:
        contest_id = message.channel_session['contest-'+ contest_id]
        Group('contest-'+contest_id).discard(message.reply_channel)
    

@channel_session
def ws_receive(message):
    # user_id = message.channel_session['user-channel']
    # contest_id = message.channel_session['contest-channel']
    # data = json.loads(message['text'])
    # m = room.messages.create(handle=data['handle'], message=data['message'])
    # Group('chat-'+label).send({'text': json.dumps(m.as_dict())})
    return None

def sendSubmissionStatus(user_id, submission):
    Group('user-' + user_id).send({'text': json.dumps({
        "response": submission,
        "messageType": "submission"
    })})
    return None