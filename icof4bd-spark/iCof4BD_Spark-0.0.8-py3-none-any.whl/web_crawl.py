import math
import re
import requests
from lxml import etree


class WebCrawl:

    def __init__(self):
        self.environment_info = {}
        self.stages_info_skipped = []
        self.stages_skipped = set()
        self.stages_unskipped = set()
        self.stages_info_unskipped = []

    @staticmethod
    def handler_request(url):
        """
        :param url:
        :return:
        """
        html = requests.get(url)
        if html.status_code == 200:
            return etree.HTML(html.content.decode('utf8'))
        else:
            print("Can not access! Please check the URL address: " + url)
            return -1

    def get_jobs_page(self, host, jobs):
        """
        page http://host:port/history/application_*************_****/1/jobs
        :param host:
        :param jobs:
        :return:
        """
        tree = self.handler_request(host + jobs)
        for line in tree.xpath(
                '/html/body/div[@class="container-fluid"]/div[4]/table[@id="completedJob-table"]/tbody/tr'):
            job = line.xpath('./td[2]/a/@href')[0]
            self.get_job_page(host + job)
        self.resolve_dependencies()

    def resolve_dependencies(self):
        for stage in self.stages_info_skipped:
            for equal_stage in self.stages_info_unskipped:
                if stage['stage_rdds'] <= equal_stage['stage_rdds']:
                    if stage['stage_rdds'] >= equal_stage['stage_rdds']:
                        stage['equal_stage'] = equal_stage['stage_id']
                        break
                else:
                    stage['equal_stage'] = []

    def get_job_page(self, url):
        """
        For each job http://host:port/history/application_*************_****/1/jobs/job/?id=7
        :param url:
        :return:
        """
        tree = self.handler_request(url)
        lists = []
        for line in tree.xpath('//*[@id="dag-viz-metadata"]/div'):
            dicts = {'Job_id': re.findall(r'\d+', tree.xpath('/html/body/div[2]/div[1]/div/h3')[0].text.strip())[0],
                     'stage_id': int(line.attrib['stage-id']),
                     'stage_skipped': line.attrib['skipped']}
            list_parents_rdds = []
            for stage in line.xpath('./div'):
                if stage.attrib['class'] == 'dot-file':
                    set_rdd = set()
                    if re.search(r'\d+->\d+', stage.text):
                        for rdd in re.findall(r'\d+->\d+', stage.text):
                            set_rdd.update(tuple(rdd.split('->')))
                    dicts['stage_rdds'] = set_rdd
                elif stage.attrib['class'] == 'incoming-edge':
                    list_parents_rdds.append(stage.text.split(',')[0])
                else:
                    pass
            dicts['parent_rdds'] = set(tuple(list_parents_rdds))
            dicts['parent_stages'] = set()
            lists.append(dicts)
        reversed_list = list(reversed(lists))
        for i, stage in enumerate(reversed_list):
            if stage['parent_rdds']:
                for stage_parent in range(i + 1, len(reversed_list)):
                    if stage['parent_rdds'] & reversed_list[stage_parent]['stage_rdds']:
                        stage['parent_stages'].add(reversed_list[stage_parent]['stage_id'])

        stage_index = 0
        for line in tree.xpath(
                '//table[@id="completedStage-table"]/tbody/tr'):
            dicts_data = {
                'Task_Raw': line.xpath(
                    'normalize-space(./td[@class="progress-cell"]/div[@class="progress"]/span/text())').split(
                    '/')[0],
                'Input': self.transfer(line.xpath('./td[6]/text()')),
                'Output': self.transfer(line.xpath('./td[7]/text()')),
                'Shuffle_Read': self.transfer(line.xpath('./td[8]/text()')),
                'Shuffle_Write': self.transfer(line.xpath('./td[9]/text()'))}
            while reversed_list[stage_index]['stage_skipped'] == 'true':
                stage_index = stage_index + 1

            reversed_list[stage_index].update(dicts_data)
            stage_index = stage_index + 1

        for stage in reversed_list:
            if stage['stage_skipped'] == 'true':
                self.stages_info_skipped.append(stage)
                self.stages_skipped.add(stage['stage_id'])
            elif stage['stage_skipped'] == 'false':
                self.stages_info_unskipped.append(stage)
                self.stages_unskipped.add(stage['stage_id'])
            else:
                print("no skipped id")

    def get_start_page(self, url, application):
        """
        page http://host:port/history/application_*************_****/1/stages
        :param url:
        :param application: application
        """
        url_app = url.strip().split('/')
        url_app[4] = application
        host = url.strip().split('/hi')[0]
        tree = self.handler_request('/'.join(url_app))

        environment = tree.xpath(
            "/html/body/div[@class='navbar navbar-static-top']/div[@class='navbar-inner']/ul[@class='nav']/li[4]/a/@href")[
            0]
        self.get_environment_page(host + environment, application.split('_')[2])

        jobs = tree.xpath(
            "/html/body/div[@class='navbar navbar-static-top']/div[@class='navbar-inner']/ul[@class='nav']/li[1]/a/@href")[
            0]
        self.get_jobs_page(host, jobs)

    def get_environment_page(self, url, app_id):
        """
        page http://host:name/history/application_*************_****/1/environment/
        :param url: http://host:name/history/application_*************_****/1/environment/
        :param app_id: Application id
        """
        tree = self.handler_request(url)
        Application_Name = tree.xpath(
            "/html/body/div[@class='navbar navbar-static-top']/div[@class='navbar-inner']/p[@class='navbar-text pull-right']/strong/@title")

        self.environment_info = {'Application_Name': app_id + '_' + Application_Name[0]}
        for line in tree.xpath(
                "/html/body/div[@class='container-fluid']/span/table[@class='table table-bordered table-condensed table-striped sortable'][2]/tbody/tr"):
            if line.xpath('./td[1]/text()')[0] == 'spark.executor.memory':
                self.environment_info['spark.executor.memory'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.executor.cores':
                self.environment_info['spark.executor.cores'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.driver.memory':
                self.environment_info['spark.driver.memory'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.default.parallelism':
                self.environment_info['spark.default.parallelism'] = line.xpath('./td[2]/text()')[0]
            if line.xpath('./td[1]/text()')[0] == 'spark.memory.offHeap.size':
                self.environment_info['spark.memory.offHeap.size'] = line.xpath('./td[2]/text()')[0]
            '''
                Todo
            '''

    def get_executor_num(self, url):
        """
        page http://host:name/history/application_*************_****/1/executors/
        :param url: http://host:name/history/application_*************_****/1/executors/
        Todo
        """

        tree = self.handler_request(url)
        tree.path(
            "/html/body/div[@class='container-fluid']/div[2]/div[@id='active-executors']/div[@class='container-fluid'][2]/div[@class='container-fluid']/div[@id='active-executors-table_wrapper']/div[@class='row'][2]/div[@class='col-sm-12']/table[@id='active-executors-table']/tbody/tr[@class='odd'][1]/td[2]")

    def start(self, host, application):
        """
        :param host: host:port
        :param application: application
        """
        self.get_start_page(host, application)

    def transfer(self, data):
        if len(data):
            if data[0].split(' ')[1] == 'GB' or data[0].split(' ')[1] == 'g':
                return str(math.ceil(float(data[0].split(' ')[0]) * 1024))
            if data[0].split(' ')[1] == 'MB' or data[0].split(' ')[1] == 'm':
                return str(math.ceil(float(data[0].split(' ')[0])))
            if data[0].split(' ')[1] == 'KB':
                if float(data[0].split(' ')[0]) < 1024:
                    return '1'
                else:
                    return str(math.ceil(float(data[0].split(' ')[0]) / 1024))
        else:
            return '0'

    def prettify_xml(self, element, indent, newline, level=0):
        if len(element):
            if element.text is None or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        temp = list(element)
        for sub_element in temp:
            if temp.index(sub_element) < (len(temp) - 1):
                sub_element.tail = newline + indent * (level + 1)
            else:
                sub_element.tail = newline + indent * level
            self.prettify_xml(sub_element, indent, newline, level=level + 1)

# if __name__ == '__main__':
#     # wc = WebCrawl()
#     # wc.get_start_page('http://10.239.166.104:18088', '/1/jobs', 'application_1587718859083_0232')
#     template_tree = etree.ElementTree(file='template.xml')
#     template_tree_root = template_tree.getroot()
#     print(list(template_tree_root.iter(tag='DebugLevel')))
#     for i in template_tree_root[6]:
#         print(i.tag, i.text)
