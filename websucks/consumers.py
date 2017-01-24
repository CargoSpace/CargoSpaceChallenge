from channels import Group
from channels.sessions import channel_session
import logging
import json
import uuid
from contest import lib

@channel_session
def ws_connect(message):
    prefix, user_id, contest_id = message['path'].strip('/').split('/')
    if user_id is None or contest_id is None:
        return
    
    Group('user-' + user_id).add(message.reply_channel)
    Group('contest-' + contest_id).add(message.reply_channel)
    message.channel_session['user-channel'] = user_id
    message.channel_session['contest-channel'] = contest_id
    
    Group('user-' + user_id).send({'text': json.dumps({
        "response": "welcome to Cargo Space Challenge",
        "messageType": "info"
    })})
    Group('user-' + user_id).send({'text': json.dumps({
        "response": lib.getUserSubmission(user_id, contest_id),
        "messageType": "submissions"
    })})
    Group('contest-' + contest_id).send({'text': json.dumps({
        "response": "You are now subscribed to the contest submission channel",
        "messageType": "info"
    })})
    logging.info("%s joined", user_id)


@channel_session
def ws_disconnect(message):
    user_id = message.channel_session['user-channel']
    contest_id = message.channel_session['contest-channel']
    Group('user-'+user_id).discard(message.reply_channel)
    Group('contest-'+contest_id).discard(message.reply_channel)
    logging.info("%s left", user_id)
    

@channel_session
def ws_receive(message):
    # user_id = message.channel_session['user-channel']
    # contest_id = message.channel_session['contest-channel']
    # data = json.loads(message['text'])
    # m = room.messages.create(handle=data['handle'], message=data['message'])
    # Group('chat-'+label).send({'text': json.dumps(m.as_dict())})
    return None