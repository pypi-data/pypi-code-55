import re
import os
import sys
import fileinput
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import openpyxl
import xlrd


# from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
# # Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure

class log_analysis:

    def __init__(self):
        self.list_stage_par = []
        self.list_stage = []
        self.list_stage_exe = []
        self.list_stage_par = []
        self.list_stage_exe_time = []
        self.list_task = []
        self.list_totalExcutionMS = []
        self.list_totalCPUMS = []
        self.list_totalGCTime = []
        self.list_totalDiskRdMS = []
        self.list_totalDiskWrtMS = []
        self.list_HDFSrdMS = []
        self.list_HDFSwrtMS = []
        self.list_totalNICMS = []
        self.list_fetchMS = []
        self.list_copyMS = []
        self.list_rddRdMS = []
        self.list_rddWrtMS = []
        self.list_shuffleResultMS = []
        self.list_totalRDDMS = []
        self.list_misc = []
        self.list_shuffSort = []
        self.list_shuffSer = []
        self.list_shuffDeser = []
        self.list_shuffCompress = []
        self.list_shuffUncompress = []
        self.list_shuffRead = []
        self.list_shuffWrite = []
        self.list_spillWrtMS = []
        self.list_spillRdMS = []
        self.list_spillWrtByte_MEM = []
        self.list_spillWrtBytes_DISK = []

    def stage_static(self, filename):
        try:
            with open(filename, 'r', encoding='cp850') as f:
                for line in f:
                    if re.search(r'parsing app(.*)$', line):
                        self.list_stage_par.append(re.findall(r'has (\d+) partitions', line)[0])
                    if re.search(r'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<(.*)$', line):
                        Stage_execution_time = re.findall(r'\d+', line)
                        self.list_stage_exe.append(Stage_execution_time[1])
                        self.list_stage_exe_time.append(int(Stage_execution_time[0]))
                    if re.search(r'SendMsgToApp/TaskDone2(.*)$', line):
                        self.list_task.append(re.findall(r'MS task (\d+) of', line)[0])
                        self.list_stage.append(re.findall(r'of stage (\d+) of', line)[0])
                    if re.search(r'totalExcutionMS(.*)', line):
                        self.list_totalExcutionMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'totalCPUMS(.*)', line):
                        self.list_totalCPUMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'totalGCTime(.*)', line):
                        self.list_totalGCTime.append(re.findall(r'\d+', line)[0])
                    if re.search(r'totalDiskRdMS(.*)', line):
                        self.list_totalDiskRdMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'totalDiskWrtMS(.*)', line):
                        self.list_totalDiskWrtMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'HDFSrdMS(.*)', line):
                        self.list_HDFSrdMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'HDFSwrtMS(.*)', line):
                        self.list_HDFSwrtMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'totalNICMS(.*)', line):
                        self.list_totalNICMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'fetchMS(.*)', line):
                        self.list_fetchMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'copyMS(.*)', line):
                        self.list_copyMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'rddRdMS(.*)', line):
                        self.list_rddRdMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'rddWrtMS(.*)', line):
                        self.list_rddWrtMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffleResultMS(.*)', line):
                        self.list_shuffleResultMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'totalRDDMS(.*)', line):
                        self.list_totalRDDMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'misc(.*)', line):
                        self.list_misc.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffSort(.*)', line):
                        self.list_shuffSort.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffSer(.*)', line):
                        self.list_shuffSer.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffDeser(.*)', line):
                        self.list_shuffDeser.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffCompress(.*)', line):
                        self.list_shuffCompress.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffUncompress(.*)', line):
                        self.list_shuffUncompress.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffRead(.*)', line):
                        self.list_shuffRead.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'shuffWrite(.*)', line):
                        self.list_shuffWrite.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'spillWrtMS(.*)', line):
                        self.list_spillWrtMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'spillRdMS(.*)', line):
                        self.list_spillRdMS.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'spillWrtBytes_MEM(.*)', line):
                        self.list_spillWrtByte_MEM.append(re.findall(r'\d+\.\d+', line)[0])
                    if re.search(r'spillWrtBytes_DISK(.*)', line):
                        self.list_spillWrtBytes_DISK.append(re.findall(r'\d+\.\d+', line)[0])
            f.close()
        except UnicodeDecodeError:
            print("encoding error!")

    def save_to_excel(self, file):
        writer = pd.ExcelWriter(file.split('.')[0] + '.xlsx')
        pd.DataFrame({'Stages': self.list_stage,
                      'Tasks': self.list_task,
                      'totalExcutionMS': self.list_totalExcutionMS,
                      'totalCPUMS': self.list_totalCPUMS,
                      'totalGCTime': self.list_totalGCTime,
                      'totalDiskRdMS': self.list_totalDiskRdMS,
                      'totalDiskWrtMS': self.list_totalDiskWrtMS,
                      'HDFSrdMS': self.list_HDFSrdMS,
                      'HDFSwrtMS': self.list_HDFSwrtMS,
                      'totalNICMS': self.list_totalNICMS,
                      'fetchMS': self.list_fetchMS,
                      'copyMS': self.list_copyMS,
                      'rddRdMS': self.list_rddRdMS,
                      'rddWrtMS': self.list_rddWrtMS,
                      'shuffleResultMS': self.list_shuffleResultMS,
                      'totalRDDMS': self.list_totalRDDMS,
                      'misc': self.list_misc,
                      'shuffSort': self.list_shuffSort,
                      'shuffSer': self.list_shuffSer,
                      'shuffDeser': self.list_shuffDeser,
                      'shuffCompress': self.list_shuffCompress,
                      'shuffUncompress': self.list_shuffUncompress,
                      'shuffRead': self.list_shuffRead,
                      'shuffWrite': self.list_shuffWrite,
                      'spillWrtMS': self.list_spillWrtMS,
                      'spillRdMS': self.list_spillRdMS,
                      'spillWrtBytes_MEM': self.list_spillWrtByte_MEM,
                      'spillWrtBytes_DISK': self.list_spillWrtBytes_DISK}).to_excel(writer, index=None,
                                                                                    sheet_name='statics')
        i = len(self.list_stage_exe_time) - 1
        while i > 0:
            self.list_stage_exe_time[i] = self.list_stage_exe_time[i] - self.list_stage_exe_time[i - 1]
            i = i - 1
        pd.DataFrame({'Stage': self.list_stage_exe,
                      'Tasks': self.list_stage_par,
                      'time(ms)': self.list_stage_exe_time}).to_excel(writer, index=None,
                                                                      sheet_name='stage_exe_time')
        writer.save()

    def graph_draw(self, file):
        plt.figure(figsize=(15, 6))
        # plt.figure(1)
        # plt.subplot(551)
        # plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1, hspace=1)
        plt.title('Execution time (ms)')
        plt.xlabel('Stages')
        plt.ylabel('Time (ms)')

        # plt.xticks(self.list_stage_exe,size='small',rotation=33)
        plt.bar(self.list_stage_exe, self.list_stage_exe_time, color='c', width=0.5, alpha=0.8)
        # plt.subplot(111)
        # plt.plot(self.list_task, self.list_totalExcutionMS)
        # self.autolabel()
        plt.xticks(size='small', rotation=33)
        for a, b in zip(self.list_stage_exe, self.list_stage_exe_time):
            plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
        plt.savefig(file.split('.')[0] + '.png', dpi=400)
        plt.close()
        # plt.grid()
        # plt.show()

    # def autolabel(self, rects):
    #     for rect in rects:
    #         height = rect.get_height()
    #         plt.text(rect.get_x() + rect.get_width() / 2. - 0.3, 1.01 * height, '%s' % int(height))
    # def gui_view(self):
    #     root=Tk()
    #     root.title('Graph statics')
    #     fig = Figure(figsize=(50, 40), dpi=500)
    #     fig.add_subplot(331).bar(self.list_stage_exe, self.list_stage_exe_time)
    #     canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    #     canvas.draw()
    #
    #     toolbar = NavigationToolbar2Tk(canvas, root)
    #     toolbar.update()
    #
    #     def on_key_press(event):
    #         print("you pressed {}".format(event.key))
    #         key_press_handler(event, canvas, toolbar)
    #
    #     canvas.mpl_connect("key_press_event", on_key_press)
    #
    #     button = Button(master=root, text="Quit", command=root.quit)
    #
    #     # Packing order is important. Widgets are processed sequentially and if there
    #     # is no space left, because the window is too small, they are not displayed.
    #     # The canvas is rather flexible in its size, so we pack it last which makes
    #     # sure the UI controls are displayed as long as possible.
    #     button.pack(side=BOTTOM)
    #     canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    #     mainloop()


def print_files():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # print(base_dir)
    # print(os.getcwd())
    # print(os.path.abspath(os.path.dirname(__file__)))
    # file = open(base_dir+'/'+filename, 'r')
    # file = base_dir + '/' + filename
    file_list = []
    for files in os.walk(base_dir):
        for file in files[2]:
            if os.path.splitext(file)[1] == '.log':
                # For windows
                file_list.append(file)
                # For Linux 
                # file_list.append(base_dir + '/' + file)
    # print("Handling logs: ")
    # for handle_file in file_list:
    #     print(handle_file)
    if not file_list:
        print("No log files in this dir: " + base_dir)
    return file_list


def main(argv):
    # log.gui_view()
    if len(argv)>1:
        try:
            for i in range(1, len(argv)):
                log = log_analysis()
                print('Handling ' + argv[i])
                try:
                    log.stage_static(argv[i])
                    log.save_to_excel(argv[i])
                    log.graph_draw(argv[i])
                    print('Successful')
                except:
                    print('Failed')
        except:
            print('Failed')
    else:
        try:
            for file in print_files():
                log = log_analysis()
                print('Handling ' + file)
                try:
                    log.stage_static(file)
                    log.save_to_excel(file)
                    log.graph_draw(file)
                    print('Successful')
                except:
                    print('Failed')
        except:
            print('Failed')


if __name__ == "__main__":
    main(sys.argv)
