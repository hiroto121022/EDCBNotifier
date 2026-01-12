
import io
import json
import os
import requests


class Slack:
    """
    Slack の Webhook でメッセージを送信するクラス
    """

    def __init__(self, webhook_url:str):
        """
        Args:
            webhook_url (str): Slack の Webhook の URL
        """

        self.webhook_url = webhook_url


    def sendMessage(self, message:str, image_path:str=None) -> dict:
        """
        Slack の Webhook でメッセージを送信する

        Args:
            message (str): 送信するメッセージの本文
            image_path (str, optional): 送信する画像のファイルパス. Defaults to None.

        Returns:
            dict: ステータスコードとエラーメッセージが入った辞書
        """

        # Slack の Incoming Webhook にメッセージを送信
        # ref: https://api.slack.com/messaging/webhooks

        # メッセージペイロードを作成
        payload = {
            'username': 'EDCBNotifier',
            'icon_url': 'https://raw.githubusercontent.com/tsukumijima/EDCBNotifier/master/EDCBNotifier/EDCBNotifier.png',
            'text': message,
        }

        # 画像も送信する場合
        if image_path is not None and os.path.isfile(image_path):
            # Slack の Incoming Webhook は直接画像をアップロードできないため、
            # 画像は外部にホストする必要があります。
            # ここでは画像パスが指定されていても、画像のアップロードはスキップし、
            # テキストのみを送信します。
            # 画像を送信したい場合は、Slack API の files.upload を使用する必要があります。
            pass

        # Webhook を送信
        response = requests.post(self.webhook_url, json=payload)

        # 失敗した場合はエラーメッセージを取得
        if response.status_code != 200:
            try:
                message = response.text
            except:
                message = 'Unknown error'
        else:
            message = 'Success'

        # ステータスコードとエラーメッセージを返す
        return {
            'status': response.status_code,
            'message': message,
        }
