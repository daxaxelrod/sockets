from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session


#handles http
def http_consumer(message):
	response = HttpResponse("Hello world! you asked for %s" % message.content["path"])
	for chunk in AsgiHandler.encode_response(response):
		message.reply_channel.send(chunk)


# used for js console # If you want this back, make sure to change routing.py
# def ws_message(message):
# 	#message packet have a text key for their textual data
# 	# message.reply_channel.send({
# 	#	"text": message.content["text"],
# 	#	})
#
# 	#send the message to a group instead
# 	Group("chat").send({
# 	"text": "[user] %s" % message.content["text"],
# 	})
#
#
# def ws_add(message):
# 	message.reply_channel.send({"accept":True})
# 	Group("chat").add(message.reply_channel)
#
# def ws_disconnect(message):
# 	Group("chat").discard(message.reply_channel)
#

#used for chat room
@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # get room name
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

@channel_session
def ws_message(message):
    Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
    })

@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
