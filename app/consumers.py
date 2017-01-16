from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http



#handles http
def http_consumer(message):
	response = HttpResponse("Hello world! you asked for %s" % message.content["path"])
	for chunk in AsgiHandler.encode_response(response):
		message.reply_channel.send(chunk)


# used for js console # If you want this back, make sure to change routing.py
#note that ws stands for websocket
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

#used for chat room -- anyone to anyone
# @channel_session
# def ws_connect(message):
#     # Accept connection
# 	message.reply_channel.send({"accept": True})
#     # get room name
# 	room = message.content['path'].strip("/")
#     # Save room in session and add us to the group
# 	print("chatter in {}".format(room))
# 	message.channel_session['room'] = room
# 	Group("chat-%s" % room).add(message.reply_channel)
#
# @channel_session
# def ws_message(message):
#     Group("chat-%s" % message.channel_session['room']).send({
#         "text": message['text'],
#     })
#
# @channel_session
# def ws_disconnect(message):
#     Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

# chat room, only first letters of user names have to match in order to chat

@channel_session_user_from_http
def ws_connect(message):
	message.reply_channel.send({"accept": True})
	# add them to the group based on their username first letter
	Group("chat-%s" % message.user.username[0]).add(message.reply_channel)

@channel_session_user
def ws_message(message):
	Group("chat-%s" % message.user.username[0]).send({
	"text": message["text"]
	})

@channel_session_user
def ws_disconnect(message):
	Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)

@channel_session_user_from_http
def ws_add(message, room):
	Group("chat-%s" % room).add(message.reply_channel)

###########
##Models###
###########
