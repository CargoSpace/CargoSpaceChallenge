from channels import Group
from channels.sessions import channel_session
# from .models import Room

@channel_session
def ws_connect(message):
    prefix, contest, user_id = message['path'].strip('/').split('/').split('/')
    # room = Room.objects.get(label=label)
    Group('user-' + user_id).add(message.reply_channel)
    Group('contest-' + contest_id).add(message.reply_channel)
    message.channel_session['user-channel'] = user_id
    message.channel_session['contest-channel'] = contest_id
    Group('user-' + user_id).send({'text': "Welcome to Cargo_ Challenge"})
    Group('contest-' + contest_id).send({'text': "You are now subscribed to the contest submission channel"})


@channel_session
def ws_disconnect(message):
    user_id = message.channel_session['user-channel']
    contest_id = message.channel_session['contest-channel']
    Group('user-'+user_id).discard(message.reply_channel)
    Group('contest-'+contest_id).discard(message.reply_channel)
    

@channel_session
def ws_receive(message):
    # user_id = message.channel_session['user-channel']
    # contest_id = message.channel_session['contest-channel']
    # data = json.loads(message['text'])
    # m = room.messages.create(handle=data['handle'], message=data['message'])
    # Group('chat-'+label).send({'text': json.dumps(m.as_dict())})
    return None