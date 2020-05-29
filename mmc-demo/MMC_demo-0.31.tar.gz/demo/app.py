import tkinter as tk
from tkinter import ttk

import requests

class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Intelligent text analysis')
        self.width = 800
        self.height = 600
        self.language_var = tk.StringVar()
        self.key_var = tk.StringVar()
        self.doc_sentiment_var = tk.StringVar()

        # Azure订阅的endpoint与subscription_key
        self.endpoint = 'https://rdtextdemo.cognitiveservices.azure.com/'
        self.subscription_key = '295d69ee9ad84ca2a51aabce9dfaa83b'

        # 窗口居中显示
        self.window.geometry(self.cal_size())
        self.window.resizable(width=False, height=False)
        self.create_frames()

    def mainloop(self):
        self.window.mainloop()

    def cal_size(self):
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        return '%dx%d+%d+%d' % (self.width, self.height, (screenwidth-self.width)/2, (screenheight-self.height)/2)

    def create_frames(self):
        #创建frame容器
        frm_lt = tk.Frame(width=400, height=540)
        frm_lb = tk.Frame(width=400, height=60)
        frm_rt = tk.Frame(width=400, height=600)

        frm_lt.grid(row=0, column=0, padx=3, pady=3)
        frm_lb.grid(row=1, column=0)
        frm_rt.grid(row=0, column=1, rowspan=2, padx=3, pady=3)

        #添加文本框
        self.content = tk.Text(frm_lt, bg='white', width = 55, height=40,wrap=tk.WORD)
        self.content.insert(tk.INSERT, '输入你要分析的文字')
        self.content.grid(row=0,column=0,padx=3,pady=3)

        #添加按钮
        btn_send = tk.Button(frm_lb, text='分 析', width = 8, command=lambda:self.analysis_func(self.content.get('1.0',tk.END)))
        btn_send.grid(row=0,column=0,padx=80,pady=5)
        btn_cancel = tk.Button(frm_lb, text='取 消', width = 8,command=self.window.quit)
        btn_cancel.grid(row=0,column=1,sticky='E',pady=5)

        #添加结果显示
        result_frame = tk.LabelFrame(frm_rt, text="分析结果", labelanchor="n",font=("黑体", 16), width=260)
        result_frame.grid(row=0, column =0, padx=5, pady=5)

        result_language = tk.Label(result_frame,text = '语言:',font=("微软雅黑", 12),fg='blue')
        result_language.grid(row=2,column=0,padx=5,pady=5, sticky=tk.W)

        language_value = tk.Label(result_frame,textvariable=self.language_var,wraplength=260, justify = 'left',font=("微软雅黑", 12))
        language_value.grid(row=2,column=1,padx=5,pady=5, sticky =tk.W)

        s1 = ttk.Separator(result_frame, orient='horizontal')
        s1.grid(row=3, column=0, columnspan=2, sticky = tk.EW)

        result_keyword = tk.Label(result_frame,text = '关键短语:',font=("微软雅黑", 12), fg='blue')
        result_keyword.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        key_value = tk.Label(result_frame,textvariable =self.key_var,wraplength=260, justify='left',font=("微软雅黑", 12))
        key_value.grid(row=4, column=1, padx=5, pady=5)

        s2 = ttk.Separator(result_frame, orient='horizontal')
        s2.grid(row=5, column=0, columnspan=2, sticky = tk.EW)

        result_sentiment = tk.Label(result_frame,text = '情绪:',font=("微软雅黑", 12), fg='blue')
        result_sentiment.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

        # document = tk.Label(result_frame,text = '文档',wraplength=260, justify='left',font=("黑体", 10))
        # document.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        self.doc_sentiment = tk.Label(result_frame,textvariable =self.doc_sentiment_var,wraplength=260, justify='left',font=("微软雅黑", 12))
        self.doc_sentiment.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # s3 = ttk.Separator(result_frame, orient='horizontal')
        # s3.grid(row=8, column=1, sticky = tk.EW)

        self.language_var.set('中文')
        self.key_var.set('关键词1，关键词2，关键词3，关键词4，关键词5，关键词6')
        self.doc_sentiment_var.set('中立')

        #固定容器大小
        frm_lt.grid_propagate(0)
        frm_lb.grid_propagate(0)
        frm_rt.grid_propagate(0)

    def requests_post(self,url):
        input_text = self.content.get('1.0',tk.END)
        documents = {"documents": [{"id": "1", "text": input_text}]}
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        response = requests.post(url, headers=headers, json=documents)
        response.raise_for_status()
        return response

    def get_language(self):
        language_api_url = self.endpoint + "/text/analytics/v2.1/languages"
        languages = self.requests_post(language_api_url).json()
        self.language_var.set(languages["documents"][0]["detectedLanguages"][0]["name"])

    def get_keyword(self):
        keyphrase_url = self.endpoint + "/text/analytics/v2.1/keyphrases"
        keywords = self.requests_post(keyphrase_url).json()
        keywords_list = keywords["documents"][0]["keyPhrases"]
        self.key_var.set(','.join(keywords_list))

    def get_sentiment(self):
        sentiment_url = self.endpoint + "/text/analytics/v2.1/sentiment"
        sentiments = self.requests_post(sentiment_url).json()
        score = (sentiments["documents"][0]["score"])
        sent =''
        if score >=0.7:
            sent ='积极'
            self.doc_sentiment['fg']='green'
        elif score >= 0.3:
            sent = "中立"
            self.doc_sentiment['fg']='black'
        else:
            sent = "消极"
            self.doc_sentiment['fg']='red'
        self.doc_sentiment.config()
        self.doc_sentiment_var.set(sent)

    def analysis_func(self,string):
        self.get_language()
        self.get_keyword()
        self.get_sentiment()

if __name__ == "__main__":
    app = Application()
    app.mainloop()



        # self.canvas = tk.Canvas(frame1, bg='white', height=300, width=300)
        # image = Image.open('11.jpg')
        # filename = ImageTk.PhotoImage(image)
        # self.canvas.create_image(10, 45, anchor='w',image=filename)
        # self.canvas.create_text(400, 45, text = "欢迎使用微慕客小说平台",font=('楷体',18), fill = 'red')
        # self.canvas.grid(column=0,row=0)