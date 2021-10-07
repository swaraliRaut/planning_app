import asyncio
import json
import redis
from channels.consumer import AsyncConsumer
from django.conf import settings
from task_plan.models import Vote
from task_plan.model_utils import vote_for_task, get_vote_count_for_task


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port = settings.REDIS_PORT, db = 0, decode_responses=True)

#Class to handle websocket communication with multiple channels.
class TaskConsumer(AsyncConsumer):
  
  async def websocket_connect(self, event):
    self.task_code = self.scope['url_route']['kwargs']['task_code']
    self.group_name = 'task_' + self.task_code

    await self.channel_layer.group_add(
      self.group_name,
      self.channel_name
    )
    
    await self.send({
      "type": "websocket.accept"
    })
  
  async def load_data_in_redis(self, task_code):
    count = await get_vote_count_for_task(task_code)
    redis_instance.set(self.group_name, json.dumps(count))
    return count

  async def websocket_receive(self, event):
    data = event.get('text', None)
    data = json.loads(data)
    user = self.scope["user"]
    task_data = data["data"]

    if data["event"] == "START":
      count = await self.load_data_in_redis(task_data["task_code"])

    if data["event"] == "UPDATE":
      loop = asyncio.get_event_loop()
      loop.create_task(vote_for_task(task_data["task_code"], task_data["new_choice"], user))

      count = redis_instance.get(self.group_name)
      if count == None:
        count = await self.load_data_in_redis(task_data["task_code"])
      else:
        count = json.loads(count)
        count[task_data["new_choice"]] = int(count[task_data["new_choice"]]) + 1
        count[task_data["current_choice"]] = int(count[task_data["current_choice"]]) - 1

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