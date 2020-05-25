import os,sys, tempfile
from io import StringIO
#from thebe.core.output import outputController
from multiprocessing import Process
from subprocess import call, check_output

class FileManager:
    def __init__(self, target_name):
        self.temp_name = ''
        self.target_name = target_name

        target_ext = self.test_file(self.target_name)

        if target_ext == 'ipynb':
            self.ipynb_name = ipynb_name
            ipynb_content = self.load_ipynb(target_name)
            self.target_name = self.write_temp(ipynb_content)


def test_file(targetLocation):
    '''
    Return the relevant extension. 
    If input is incorrect, explain, and quit the application.
    '''
    if os.path.isfile(targetLocation):
        try:
            return test_extension(targetLocation)
        except ValueError:
            logging.info('Please use a valid file extension. (.ipynb or .py)')
            sys.exit()
    else:
        logging.info('Thebe only works with files, not directories. Please try again with a file. (.ipynb or .py)')
        sys.exit()

def test_extension(targetLocation):
    '''
    '''

    targetExtension=targetLocation.split('.')[1]
    if targetExtension=='ipynb':
        return 'ipynb'
    elif targetExtension=='py':
        return 'py'
    else:
        logging.info('Please use a valid file extension. (.ipynb or .py)')
        sys.exit()

def load_ipynb(targetLocation):
    '''
    Return the ipynb file as a dictionary.
    '''

    data = {}
    with open(targetLocation) as ipynb_data:
        data = json.load(ipynb_data)
    return data
    def open(self):
        '''
        '''
        print('This is the location of the temporary file:\t%s'%(self.temp_loc))

        def callVim():
            # Open the file with the text editor
    #        outputController.open()
            so = sys.stdout = StringIO()
            EDITOR = os.environ.get('EDITOR','vim')
            call([EDITOR, self.temp_loc])
    #        outputController.close()

        try:
            print('Starting vim process...')
            vim = Process(target = callVim)
            vim.start()

        except KeyboardInterrupt:
            print("Terminating vim server.")
            vim.terminate()
            vim.join()
            print("Terminated flask server.")

