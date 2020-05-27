import requests

class zibal:

    def __init__(self, merchant, callback_url):
        self.merchant = merchant
        self.callback_url = callback_url


    def request(self, amount, order_id=None, mobile=None , description=None , multiplexingInfos=None, allowedCards=None, feeMode=None, percentMode=None):
        data = {}
        data['merchant'] = self.merchant
        data['callbackUrl'] = self.callback_url
        data['amount'] = amount
        if order_id:
            data['orderId'] = order_id
        if mobile:
            data['mobile'] = mobile
        if description:
            data['description'] = description
        if allowedCards:
            data['allowedCards'] = allowedCards
        if feeMode:
            data['feeMode'] = feeMode
        if percentMode:
            data['percentMode'] = percentMode

        response = self.postTo('request', data)
        return response

    def verify(self, trackId):
        data = {}
        data['merchant'] = self.merchant
        data['trackId'] = trackId
        return self.postTo('verify', data)

    def postTo(self, path, parameters):

        url = "https://gateway.zibal.ir/v1/" + path

        response = requests.post(url = url, json= parameters)

        return response.json()

    def request_result(self, result):
        switcher = {
            100: "با موفقیت تایید شد.",
            102: "merchant یافت نشد.",
            103: "Mamerchant غیرفعالrch",
            104: "merchant نامعتبر",
            201: "قبلا تایید شده.",
            105: "amount بایستی بزرگتر از 1,000 ریال باشد.",
            106: "callbackUrl نامعتبر می‌باشد. (شروع با http و یا https)",
            113: "amount مبلغ تراکنش از سقف میزان تراکنش بیشتر است.",
        }
        return switcher.get(result, "خطا در پرداخت")

    def verify_result(self, result):
        switcher = {
            100: "با موفقیت تایید شد.",
            102: "merchant یافت نشد.",
            103: "Mamerchant غیرفعالrch",
            104: "merchant نامعتبر",
            201: "قبلا تایید شده.",
            202: "سفارش پرداخت نشده یا ناموفق بوده است.",
            203: "trackId نامعتبر می‌باشد.",
        }
        return switcher.get(result, "خطا در پرداخت")