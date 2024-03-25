import requests
import json
import time
import asyncio
import logging
from .settings import settings
from .gigachat import get_gigachat_message

logger = logging.getLogger(__name__)


SITE_URL = str(settings.SITE_URL)
EMAIL = settings.EMAIL
PASSWORD = settings.PASSWORD


class Bot:
    def __init__(self) -> None:
        return
        self.get_token()

    def read_token(self):
        with open("token.json", "r") as f:
            response = json.loads(f.read())
        # print(response)
        self.token = response["token"]
        self.private_token = response["privatetoken"]

    def get_token(self):
        r = requests.post(
            SITE_URL + "/login/token.php",
            data={
                "username": EMAIL,
                "password": PASSWORD,
                "service": "moodle_mobile_app",
            },
        )
        response = r.json()
        # print(response)
        with open("token.json", "w") as f:
            f.write(json.dumps(response))
        self.token = response["token"]
        self.private_token = response["privatetoken"]

    def api_request(
        self,
        wsfunction: str,
        params: dict = {},
        data: dict = {},
        endpoint: str = SITE_URL + "/webservice/rest/server.php",
    ) -> dict:
        params = {
            "wstoken": self.token,
            "wsfunction": wsfunction,
            "moodlewsrestformat": "json",
            **params,
        }
        r = requests.post(endpoint, params=params, data=data).json()
        # print(r)
        if "errorcode" in r:
            self.get_token()
            r = requests.post(endpoint, params=params, data=data).json()
        return r

    def get_self(self):
        response = self.api_request("core_webservice_get_site_info")
        self.user_id = response["userid"]

    async def send_message(self, promt):
        promt = promt.replace("<b>", "").replace("</b>", "")
        message = "test"
        try:
            message = await get_gigachat_message(promt)
            print(message)
        except Exception as e:
            logger.error(e)
            message = "Error"

        response = self.api_request(
            "core_message_send_messages_to_conversation",
            data={
                "conversationid": 43314,
                "messages[0][text]": f"Answer ChatGPT: {message}",
            },
        )
        logger.info(response)

    async def get_message(self):
        response = self.api_request(
            "core_message_get_conversation_messages",
            data={
                "currentuserid": 12640,
                "convid": 43314,
                "newest": 1,
                "limitnum": 1,
                "limitfrom": 0,
            },
        )
        text = response["messages"][-1]["text"]
        logger.info(text)
        if not "Answer ChatGPT" in text:
            await self.send_message(text)

    def run(self):
        self.read_token()
        while True:
            self.get_message()
            time.sleep(5)


async def running():
    bot = Bot()
    bot.get_token()
    while True:
        try:
            await bot.get_message()
        except Exception as e:
            logger.error(e)
        finally:
            await asyncio.sleep(5)


async def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(running())
