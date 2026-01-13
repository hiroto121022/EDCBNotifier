
import json
import os
import sys
import urllib.request
import urllib.error


class Slack:
    """
    Slack の Webhook でメッセージを送信するクラス
    """

    def __init__(self, webhook_url:str):
        """
        Args:
            webhook_url (str): Slack の Webhook の URL
        """
        print('[Slack] Init called', file=sys.stderr)
        sys.stderr.flush()
        
        self.webhook_url = webhook_url
        print(f'[Slack Debug] Webhook URL set: {webhook_url[:50]}...', file=sys.stderr)
        sys.stderr.flush()


    def sendMessage(self, message:str, image_path:str=None) -> dict:
        """
        Slack の Webhook でメッセージを送信する

        Args:
            message (str): 送信するメッセージの本文
            image_path (str, optional): 送信する画像のファイルパス. Defaults to None.

        Returns:
            dict: ステータスコードとレスポンスが入った辞書
        """
        print('[Slack Debug] sendMessage called', file=sys.stderr)
        sys.stderr.flush()

        # Slack の Incoming Webhook にメッセージを送信
        # ref: https://api.slack.com/messaging/webhooks

        # メッセージペイロードを作成
        payload = {
            'text': message,
            'username': 'EDCBNotifier',
            'icon_url': 'https://raw.githubusercontent.com/tsukumijima/EDCBNotifier/master/EDCBNotifier/EDCBNotifier.png',
        }

        print(f'[Slack Debug] Payload created: {json.dumps(payload, ensure_ascii=False)[:200]}', file=sys.stderr)
        sys.stderr.flush()

        # 画像も送信する場合
        if image_path is not None and os.path.isfile(image_path):
            # Slack の Incoming Webhook は直接画像をアップロードできないため、
            # 画像は外部にホストする必要があります。
            # ここでは画像パスが指定されていても、画像のアップロードはスキップし、
            # テキストのみを送信します。
            # 画像を送信したい場合は、Slack API の files.upload を使用する必要があります。
            pass

        # JSONエンコード
        json_data = json.dumps(payload).encode('utf-8')
        print(f'[Slack Debug] JSON encoded, length: {len(json_data)}', file=sys.stderr)
        sys.stderr.flush()

        # リクエストを作成
        request = urllib.request.Request(
            self.webhook_url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        print('[Slack Debug] Request created', file=sys.stderr)
        sys.stderr.flush()

        # リクエストを送信
        print('[Slack Debug] Sending request...', file=sys.stderr)
        sys.stderr.flush()
        
        try:
            with urllib.request.urlopen(request) as response:
                status_code = response.getcode()
                response_body = response.read().decode('utf-8')
                print(f'[Slack Debug] Response received - Status: {status_code}, Body: {response_body}', file=sys.stderr)
                sys.stderr.flush()
                return {
                    'status': status_code,
                    'response': response_body if response_body else 'ok'
                }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f'[Slack Debug] HTTP Error: {e.code}, Body: {error_body}', file=sys.stderr)
            sys.stderr.flush()
            raise Exception(f'HTTP Error {e.code}: {error_body}')
        except Exception as e:
            print(f'[Slack Debug] Exception occurred: {type(e).__name__}: {str(e)}', file=sys.stderr)
            sys.stderr.flush()
            raise
