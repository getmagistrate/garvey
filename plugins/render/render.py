import os
import requests
from errbot import BotPlugin, botcmd
from errbot.backends import zulip

class Render(BotPlugin):
    """
    This plugin allows users to interact with Magistrate's primary hosting provider,
    Render.
    """
    topic = zulip.ZulipRoom("engineering", "engineering", "news")

    def poll_deploy(self, service_id, service_name, deploy_id):

        url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}"

        headers = {
            "authorization": "Bearer " + os.environ["RENDER_API_KEY"],
            "accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        if response.status_code != 200:
            self.stop_poller(self.poll_deploy, args=(service_id, service_name, deploy_id))
            message = f"Render deploy for service **{service_name}** with deploy id `{deploy_id}` had an **error** while polling for its status: {data['message']}."
            self.send(self.topic, message)

        elif data["status"] not in ("created", "build_in_progress", "update_in_progress"):
            self.stop_poller(self.poll_deploy, args=(service_id, service_name, deploy_id))
            message = f"Render deploy for service **{service_name}** with deploy id `{deploy_id}` finished with status `{data['status']}`."
            self.send(self.topic, message)


    def _deploy(self, msg, service_id, service_name):
        url = f"https://api.render.com/v1/services/{service_id}/deploys"
        payload = {"clearCache": "do_not_clear"}
        headers = {
            "authorization": "Bearer " + os.environ["RENDER_API_KEY"],
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if response.status_code != 201:
            return f"The deploy failed for the following reason: {data['message']}"

        self.start_poller(10, self.poll_deploy, times=100, args=(service_id, service_name, data['id']))
        message = f"Render deploy for service **{service_name}** initiated with deploy id `{data['id']}` and status `{data['status']}`. Initiator was @**{msg.frm.fullname}**."
        
        if msg.to == self.topic:
            return message
        else:
            self.send(self.topic, message)
            return "OK. See #**engineering>news** for status updates."

    @botcmd
    def deploy_web(self, msg, args):
        """Deploys the magistrate/main branch to production on Render to the magistrate-prod-web service."""
        service_id = os.environ["RENDER_WEB_SERVICE_ID"]
        service_name = "magistrate-prod-web"
        return self._deploy(msg, service_id, service_name)

    @botcmd
    def deploy_celery(self, msg, args):
        """Deploys the magistrate/main branch to production on Render to the magistrate-prod-celery service."""
        service_id = os.environ["RENDER_CELERY_SERVICE_ID"]
        service_name = "magistrate-prod-celery"
        return self._deploy(msg, service_id, service_name)
