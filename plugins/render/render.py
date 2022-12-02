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
        if data["status"] in ("live", "deactivated", "build_failed", "update_failed", "canceled"):
            self.stop_poller(self.poll_deploy, args=(service_id, service_name, deploy_id))
            self.send(self.topic, f"Render deploy **{deploy_id}** for service **{service_name}** finished with status {data['status']}.")

        # FIXME handle errors
        # FIXME say who initiated the deployment
        # FIXME stop the github deployment

    @botcmd
    def deploy_celery(self, msg, args):
        """
        Deploys the magistrate/main branch to production on Render
        to the magistrate-prod-celery service.
        """
        service_id = "srv-ca1ac5r97ejf9sopna10"
        service_name = "magistrate-prod-celery"
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
        message = f"Render deploy **{data['id']}** for service **{service_name}** initiated (status: {data['status']})."
        if msg.to == self.topic:
            return message
        else:
            self.send(self.topic, message)
            return "OK. See #engineering for status updates."
