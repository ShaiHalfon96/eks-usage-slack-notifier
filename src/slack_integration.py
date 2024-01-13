import ssl
from typing import Any

import certifi
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from tabulate import tabulate

import consts


class SlackIntegration:
    def __init__(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(token=consts.SLACK.BOT_TOKEN, ssl=ssl_context)

    def send_message(self, message, channel_id):
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=message
            )
            print(response)
        except SlackApiError as e:
            print(f"Error sending message to Slack: {e.response['error']}")

    def _send_message(self, message, channel_id, message_type: str = "text"):
        if message_type == "table":
            message = f"```\n{message}\n```"

        self.send_message(message=message, channel_id=channel_id)

    def send_table_message(self, table_headers: list[str], table_data: list[Any], channel_id: str, footnotes: str =None):
        markdown_table = SlackIntegration._create_markdown_table(header=table_headers, data=table_data)
        if footnotes:
            # Combine the table content and footnotes
            markdown_table = markdown_table + "\n\n" + footnotes
        self._send_message(message=markdown_table, channel_id=channel_id, message_type="table")

    @staticmethod
    def _create_markdown_table(header, data):
        markdown_table = tabulate(data, header, tablefmt="pipe")

        return markdown_table