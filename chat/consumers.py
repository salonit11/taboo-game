import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(self.roomGroupName, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.roomGroupName, self.channel_layer)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get("type", "")
        message = text_data_json["message"]
        username = text_data_json["username"]
        
        if event_type == "team-joined":
            username = text_data_json.get("username", "")
            teamname = text_data_json.get("teamname", "")
            
            await self.channel_layer.group_send(
				self.roomGroupName,
				{
					"type": "team_joined",
					"username": username,
					"teamname": teamname,
				},
			)
        elif event_type=="update-describer":
            teamname = text_data_json.get("teamname", "")
            await self.channel_layer.group_send(
				self.roomGroupName, {
					"type": "update_describer",
					"username": username,  # The username of the new describer
					"teamname": teamname,  # The team name where the describer is
				},
			)
        elif event_type=="round-start":
            teamname = text_data_json.get("teamname", "")
            time_remaining = text_data_json.get("timer", "")
            wordlist = text_data_json.get("wordlist", "")
            await self.channel_layer.group_send(
				self.roomGroupName, {
					"type": "round_start",
					"username": username,  # The username of the new describer
					"teamname": teamname,  # The team name where the describer is
					"time_remaining": time_remaining,  
					"wordlist":wordlist
				},
			)
        elif event_type=="round-over":
            teamname = text_data_json.get("teamname", "")
            time_remaining = text_data_json.get("timer", "")
            await self.channel_layer.group_send(
				self.roomGroupName, {
					"type": "round_over",
					"username": username,  # The username of the new describer
					"teamname": teamname,  # The team name where the describer is
				},
			)
        else:
            teamname = text_data_json.get("teamname", "")
            await self.channel_layer.group_send(
				self.roomGroupName,
				{"type": "sendMessage", "username": username, "message": message,"teamname":teamname},
			)

    async def Auth_room(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        room_code = text_data_json["room_code"]

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(
            text_data=json.dumps({"type":"chat-message","message": message, "username": username,"teamname":event['teamname']})
        )

    async def team_joined(self, event):
        username = event["username"]
        teamname = event["teamname"]
        await self.send(
            text_data=json.dumps({"type":"team-joined","username": username, "teamname": teamname})
        )
    async def update_describer(self, event):
    # Broadcast the describer update to all connected clients in the room
        await self.send(text_data=json.dumps({
			"type": "update_describer",
			"username": event["username"],
            "guessingteam": event["teamname"],
			"teamname": event["teamname"],
		}))
    async def round_start(self, event):
    # Broadcast the describer update to all connected clients in the room
        await self.send(text_data=json.dumps({
            "type":"round-start",
			"time_remaining": event["time_remaining"],
			"username":event['username'],
			"teamname":event['teamname'],
			"wordlist":event["wordlist"],
			
		}))
    async def round_over(self, event):
        await self.send(text_data=json.dumps({
            "type":"round-over",
			"username":event['username'],
			"teamname":event['teamname'],
			
		}))
