import asyncio
import json

from channels.consumer import AsyncConsumer
from task_plan.model_utils import get_vote_count_for_task, vote_for_task
from task_plan.models import Vote


class TaskConsumer(AsyncConsumer):
  
  async def websocket_connect(self, event):
    self.task_code = self.scope['url_route']['kwargs']['task_code']
    self.group_name = 'task_%s' % (self.task_code)
    
    await self.channel_layer.group_add(
      self.group_name,
      self.channel_name
    )
    
    await self.send({
      "type": "websocket.accept"
    })
  
  async def websocket_receive(self, event):
    data = event.get('text', None)
    data = json.loads(data)
    user = self.scope["user"]
    task_data = data["data"]

    if data["event"] == "UPDATE":
      loop = asyncio.get_event_loop()
      await loop.create_task(vote_for_task(task_data["task_code"], task_data["new_choice"], user))

    count = await get_vote_count_for_task(task_data["task_code"])

    msg = {
      "event" : "update", 
      "count" : count
    }
    
    await self.channel_layer.group_send(
      self.group_name,
      {
        "type": "count_update",
        "text": json.dumps(msg)
      })
  
  async def count_update(self, event):
    await self.send({
      "type": 'websocket.send',
      'text': event['text']
    })
  
  async def websocket_disconnect(self, event):
    print('disconnected', event)