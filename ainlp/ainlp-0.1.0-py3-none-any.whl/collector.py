import pymysql.cursors
import json


class Collector(object):
    def __init__(self, host, user, password, db):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.papers = {}
        self.map_paper_id_to_name = {}
        self.load_papers()

    def get_answers(self, paper_ids):
        if not isinstance(paper_ids, (list, tuple)):
            paper_ids = [paper_ids]
        stmt = '''
        select question_id, answer from merged_answer where is_spam = 0 and paper_id in ({paper_id_str})
        order by question_id asc
        '''.format(paper_id_str=','.join(map(str, paper_ids)))
        answers = []
        with self.conn.cursor() as cursor:
            cursor.execute(stmt)
            result = cursor.fetchall()
            for item in result:
                ans = json.loads(item['answer'])
                answers.append(self.prune_answer(ans))
        return answers

    def prune_answer(self, answer):
        """修剪原始answer：只保留paper props指定那些subtype，并将无用的字段剔除掉"""
        paper_name = self.map_paper_id_to_name[answer['paper_id']]
        props = self.papers[paper_name]['props']
        if props:
            opinions = []
            for op in answer['data']['opinions']:
                if op['aspectType'] in props['aspects2label']:
                    if op['aspectSubtype'] in props['aspects2label'][op['aspectType']]:
                        opinions.append(op)
        else:
            opinions = answer['data']['opinions']
        # 剔除掉无用字段
        for op in opinions:
            if 'suggestion' in op:
                op.pop('suggestion')
            if 'polarityCheck' in op:
                op['polarity'] = op['polarityCheck']
                op.pop('polarityCheck')
        return {'text': answer['data']['text'], 'opinions': opinions}

    def get_answers_by_name(self, paper_names):
        if not isinstance(paper_names, (list, tuple)):
            paper_names = [paper_names]
        paper_ids = [self.papers[name]['id'] for name in paper_names]
        return self.get_answers(paper_ids)

    def load_papers(self):
        stmt = '''
        select id, title, props from paper
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(stmt)
            result = cursor.fetchall()
            for item in result:
                self.papers[item['title']] = {'id': item['id']}
                self.map_paper_id_to_name[item['id']] = item['title']
                if item['props']:
                    self.papers[item['title']]['props'] = json.loads(item['props'])
                else:
                    self.papers[item['title']]['props'] = None
