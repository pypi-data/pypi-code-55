# coding:UTF-8
import requests


class MouseError(Exception):
    """
    マウス操作に関する例外クラス
    """
    pass


class Mouse(object):
    """
    マウス操作用クラス
    """
    def __init__(self, api_key, url="https://www.osumoi-stdio.com/maze/v1"):
        self.URL = url
        self.API_KEY = api_key
        self.token = None
        self.now_vec = 1
        self.max_turn = 0
        self.max_step = 0

    def start(self, map_id):
        """
        ゲーム開始時に一回だけ呼び出す。本APIを呼び出すと
        実行履歴が新規に作成される
        :param map_id: 迷路のID
        :return: なし
        :例外: MouseError
        """
        req_url = "{}/start/{}/{}".format(self.URL, self.API_KEY, map_id)
        r = requests.get(req_url)
        data = r.json()
        if data['error_code'] != 0:
            raise MouseError(data)
        else:
            self.token = data['token']
            self.max_turn = data["turn"]
            self.max_step = data["step"]

    def sensor(self):
        """
        マウスの進行方向の前と左右の壁情報を取得する
        :return: [左の壁の有無,前の壁の有無,右の壁の有無] 壁がある場合1, 無い場合0
        :例外: MouseError
        """
        req_url = "{}/sensor/{}".format(self.URL, self.token)

        r = requests.get(req_url)
        data = r.json()
        if data['error_code'] != 0:
            raise MouseError(data)

        return data['sensor']

    def turn_left(self):
        """
        マウスの進行方向を90°左に向ける
        :return: {"status": "OK", "error_code": 0, "message": "正常", "turn": 実行後のターン数, "step": 実行後のステップ数}
        :例外: MouseError
        """
        req_url = "{}/turn_left/{}".format(self.URL, self.token)
        r = requests.get(req_url)
        data = r.json()
        if data['error_code'] != 0:
            raise MouseError(data)

        return data

    def turn_right(self):
        """
        マウスの進行方向を90°右に向ける
        :return: {"status": "OK", "error_code": 0, "message": "正常", "turn": 実行後のターン数, "step": 実行後のステップ数}
        :例外: MouseError
        """
        req_url = "{}/turn_right/{}".format(self.URL, self.token)
        r = requests.get(req_url)
        data = r.json()
        if data['error_code'] != 0:
            raise MouseError(data)
        return data

    def go_straight(self):
        """
        1マス進む
        :return: {"status": "OK", "error_code": 0, "message": "正常", "turn": 実行後のターン数, "step": 実行後のステップ数}
        :例外: MouseError
        """
        req_url = "{}/go_straight/{}".format(self.URL, self.token)
        r = requests.get(req_url)
        data = r.json()
        if data['error_code'] != 0:
            raise MouseError(data)

        return data

    def is_goal(self):
        """
        ゴールのマスにいると1,ゴール以外のマスにいる場合は0を返す
        :return: 0 or 1
        :例外: MouseError
        """
        req_url = "{}/is_goal/{}".format(self.URL, self.token)
        r = requests.get(req_url)
        data = r.json()
        if data['error_code'] != 0:
            raise MouseError(data)
        return data['goal']