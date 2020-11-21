from . import pusher_client


def Chat(chat_to, message):
    pusher_client.trigger('chat'+str(chat_to), 'newMessage'+str(chat_to),
                          {'message': message})


def Received(chat_session, sender):
    pusher_client.trigger('chat'+str(sender), 'Received'+str(sender),
                          {'chat_session': chat_session})


def Seen(chat_session, sender):
    pusher_client.trigger('chat'+str(sender), 'Seen'+str(sender),
                          {'chat_session': chat_session})


def Video(uri, userId, peerId):
    pusher_client.trigger("video-chat-" + uri, 'client-user-id-'+str(userId),
                          {'userId': userId, "peerId": peerId})
