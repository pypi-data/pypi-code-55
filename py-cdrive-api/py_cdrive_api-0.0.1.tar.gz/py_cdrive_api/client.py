import os, requests

class CDriveClient:
    def __init__(self, domain=None, username=None, password=None, access_token=None):
        if domain != None:
            self.api_url = 'https://api.' + domain + '/'
        else:
            self.api_url = 'http://cdrive/'
        if access_token != None:
            self.access_token = access_token
            self.home = 'users/' + self.user_details['username']
        elif (username != None and password != None):
            self.access_token = self.get_access_token(username, password)
            self.home = 'users/' + username
    def get_token(self, username, password):
        response = requests.post(url= self.api_url + 'api-access-token/', data={'username': username, 'password': password})
        return response.json()['accessToken']
    def user_details(self):
        auth_header = 'Bearer ' + self.access_token
        response = requests.get(url= self.api_url + 'user-details/', headers={'Authorization': auth_header})
        return response.json()
    def upload(self, local_path, cdrive_path):
        if os.path.isdir(local_path):
            data = {
                'path': cdrive_path,
                'name': os.path.basename(local_path)
            }
            requests.post(self.api_url + 'create/', data=data, headers={'Authorization': 'Bearer ' + self.access_token})
            for obj_name in os.listdir(local_path):
                self.upload(os.path.join(local_path, obj_name), cdrive_path + '/' + data['name'])
        elif os.path.isfile(local_path):
            f = open(local_path, 'rb')
            file_name = os.path.basename(local_path)
            file_arg = {'file': (file_name, f), 'path': (None, cdrive_path)}
            requests.post(self.api_url + 'upload/', files=file_arg, headers={'Authorization': 'Bearer ' + self.access_token})
            f.close()
    def download(self, cdrive_path, local_path):
        response = requests.get(self.api_url + 'download/?path=' + cdrive_path, headers={'Authorization':'Bearer ' + self.access_token})
        download_url = response.json()['download_url']
        if local_path != None:
            url_wo_sig = download_url[:download_url.find('?')]
            name = url_wo_sig[url_wo_sig.rfind('/') + 1 :]
            file_path = os.path.join(local_path, name)
            response = requests.get(download_url)
            with open(file_path, 'wb') as f:
                f.write(response.content)
        else:
            return download_url
    def share(self, cdrive_path, permission, target_name='', target_type='user'):
        data = {
            'path': cdrive_path,
            'permission': permission,
            'targetType': target_type,
            'name': target_name
        }
        response = requests.post(self.api_url + 'share/', data=data, headers={'Authorization': 'Bearer ' + self.access_token})
    def install_app(self, app_url):
        response = requests.post(self.api_url + 'install-application/', data={'app_docker_link': app_url}, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 201:
            app_name = response.json()['appName']
            while(True):
                res = requests.get(self.api_url + 'app-status/?app_name=' + app_name, headers={'Authorization': 'Bearer ' + self.access_token})
                if res.status_code == 200 and res.json()['appStatus'] == 'Available':
                    break
            return app_name
    def app_token(self, app_name):
        response = requests.post(self.api_url + 'app-token/', data={'app_name': app_name}, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code == 200:
            return response.json()['app_token']
