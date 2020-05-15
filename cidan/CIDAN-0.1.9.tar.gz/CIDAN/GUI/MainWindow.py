import os

os.environ['QT_API'] = 'pyside2'
from PySide2.QtWidgets import QTabWidget
from CIDAN.GUI.Tabs.Tab import AnalysisTab
from CIDAN.GUI.Tabs.FileOpenTab import FileOpenTab
from CIDAN.GUI.Tabs.ROIExtractionTab import *
from CIDAN.GUI.Tabs.PreprocessingTab import *
import qdarkstyle
from CIDAN.GUI.ImageView.ImageViewModule import ImageViewModule
from CIDAN.GUI.Data_Interaction.DataHandler import DataHandler
from CIDAN.GUI.Console.ConsoleWidget import ConsoleWidget
import sys
import logging


class MainWindow(QMainWindow):
    """Initializes the basic window with Main widget being the focused widget"""

    def __init__(self, dev=False):
        super().__init__()
        self.title = 'CIDAN'
        self.width = 900
        self.height = 800
        self.setWindowTitle(self.title)
        self.setMinimumSize(self.width, self.height)
        self.main_menu = self.menuBar()
        self.table_widget = MainWidget(self, dev=dev)
        self.setCentralWidget(self.table_widget)
        # self.setStyleSheet(qdarkstyle.load_stylesheet())
        style = """
            QTabWidget {font-size: 25px; padding:1px; margin:5px;}
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                          stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                /*border: 2px solid #C4C4C3;*/
                /*border-bottom-color: #C2C7CB; !* same as the pane color *!*/
                
                min-width: 8ex;
                padding:1px;
                border:1px;
            }
            
            QComboBox::item:checked {
              font-weight: bold;
              height: 12px;
            }
            """
        self.setStyleSheet(qdarkstyle.load_stylesheet() + style)

        # extractAction.triggered.connect()

        self.show()


class MainWidget(QWidget):
    """Main Widget, contains everything

    Attributes
    ----------
    main_window : MainWindow
        A reference to the main window of the application
    main_menu : ???
        the top bar menu
    layout : QLayout
        The main layout for the widget
    data_handler : DataHandler
        The instance that controls all interactions with dataset
    thread_list : List[Thread]
        A list of all the possible running threads, used to ensure only 1 thread is
        running at a time
    preprocess_image_view : ImageViewModule
        The image view for the preprocess tab
    roi_image_view : ImageViewModule
        The image view for the roi extraction tab
    tab_widget : QTabWidget
        Controls the main tabs of the application
    console : ConsoleWidget
        Widget for the console
    tabs : List[Tabs]
        A list of the currently active tabs not used until after init_w_data is run
    """

    def __init__(self, parent, dev=False):
        """
        Initialize the main widget to load files
        Parameters
        ----------
        parent
        """
        super().__init__(parent)
        self.main_window = parent
        self.main_menu = self.main_window.main_menu
        self.layout = QVBoxLayout(self)
        self.data_handler = None
        self.thread_list = []
        self.preprocess_image_view = ImageViewModule(self, roi=False)
        self.roi_image_view = ImageViewModule(self, histogram=False, roi=False)
        self.dev = dev
        self.tab_widget = QTabWidget()
        self.fileOpenTab = FileOpenTab(self)
        self.tab_widget.addTab(self.fileOpenTab, "Open Dataset")

        # This part add placeholder tabs until data is loaded
        self.tabs = ["Preprocessing", "ROI Extraction", "Analysis"]
        for num, tab in enumerate(self.tabs):
            self.tab_widget.addTab(QWidget(), tab)
            self.tab_widget.setTabEnabled(num + 1, False)
        self.layout.addWidget(self.tab_widget)

        self.console = ConsoleWidget()
        self.console.setMaximumHeight(150)
        self.console.setMinimumHeight(150)
        self.layout.addWidget(self.console)
        self.setLayout(self.layout)

        # Initialize top bar menu
        fileMenu = self.main_menu.addMenu('&File')
        openFileAction = QAction("Open File", self)
        openFileAction.setStatusTip('Open a single file')
        openFileAction.triggered.connect(lambda: self.selectOpenFileTab(0))
        fileMenu.addAction(openFileAction)
        openFolderAction = QAction("Open Folder", self)
        openFolderAction.setStatusTip('Open a folder')
        openFolderAction.triggered.connect(lambda: self.selectOpenFileTab(1))
        fileMenu.addAction(openFolderAction)
        openPrevAction = QAction("Open Previous Session", self)
        openPrevAction.setStatusTip('Open a previous session')
        openPrevAction.triggered.connect(lambda: self.selectOpenFileTab(2))
        fileMenu.addAction(openPrevAction)

        # Below here in this function is just code for testing
        # TODO check if it can load data twice
        if False and dev:
            # auto loads a small dataset
            self.data_handler = DataHandler(

                "/Users/sschickler/Code Devel/LSSC-python/input_images/",
                "/Users/sschickler/Code Devel/LSSC-python/input_images/test31",
                trials=["small_dataset.tif"],
                save_dir_already_created=False)
            self.init_w_data()
        if False and dev:
            # auto loads a large dataset
            self.data_handler = DataHandler(
                "/Users/sschickler/Code Devel/LSSC-python/input_images/dataset_1",
                "/Users/sschickler/Code Devel/LSSC-python/input_images/test3",
                save_dir_already_created=False)
            self.init_w_data()

    def init_w_data(self):
        """
        Initialize main widget with data

        It activates the other tabs and helps load the data into image views
        Returns
        -------

        """
        for num, _ in enumerate(self.tabs):
            self.tab_widget.removeTab(1)
        # TODO actually delete the tabs not just remove them
        # TODO add to export tab to export all time traces or just currently caclulated ones
        self.tabs = [PreprocessingTab(self), ROIExtractionTab(self), AnalysisTab(self)]

        # Add tabs
        for tab in self.tabs:
            self.tab_widget.addTab(tab, tab.name)
        self.tab_widget.setCurrentIndex(1)
        self.tab_widget.currentChanged.connect(
            lambda x: self.tabs[1].set_background("",
                                                  self.tabs[
                                                      1].background_chooser.current_state(),
                                                  update_image=True))

        if not hasattr(self, "export_menu"):
            self.export_menu = self.main_menu.addMenu("&Export")
            export_action = QAction("Export Time Traces/ROIs", self)
            export_action.setStatusTip('Export Time Traces/ROIs')
            export_action.triggered.connect(lambda: self.exportStuff())
            self.export_menu.addAction(export_action)

    def selectOpenFileTab(self, index):
        self.tab_widget.setCurrentIndex(0)
        self.fileOpenTab.tab_selector.setCurrentIndex(index)

    def exportStuff(self):
        msg = QMessageBox()
        msg.setWindowTitle("Export data")
        msg.setText("Data Exported to save directory")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()


if __name__ == "__main__":
    # client = Client(processes=False, threads_per_worker=8,
    #                 n_workers=1, memory_limit='16GB')
    # print(client)
    LOG_FILENAME = 'log.out'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    logger = logging.getLogger("CIDAN")
    logger.debug("Program started")
    app = QApplication([])
    app.setApplicationName("CIDAN")
    widget = MainWindow(dev=True)

    sys.exit(app.exec_())
