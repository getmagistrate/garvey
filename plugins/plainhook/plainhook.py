import os
from errbot import BotPlugin, webhook
from errbot.backends import zulip

class Plainhook(BotPlugin):
    """
    This plugin allows services to POST to a webhook and have the message
    passed through to a channel.
    """

    @webhook(os.environ['PLAINHOOK_BASE_URL'] + "/<stream>/<topic>/")
    def deliver_message_to_topic(self, message, stream, topic):
        """Delivers an arbitrary message to a Zulip topic."""
        topic = zulip.ZulipRoom(stream, stream, topic)
        self.send(topic, message)
        return None  # Returns a 200 
