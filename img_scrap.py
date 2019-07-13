import os
import re
import sys
import urllib.request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QMessageBox, \
    QHBoxLayout, QPushButton, QDialog, QLineEdit, QMenu, QAction, QLabel, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class ImgScrap(QMainWindow):
    def __init__(self, parent=None):
        super(ImgScrap, self).__init__(parent)
       
        # search keyword        
        self.img_path = ''
      
        # input keyword
        self.keyword_input = QLineEdit()
        self.keyword_input.setFixedHeight(30)
        self.keyword_input.setPlaceholderText('Input keyword here...')
        self.path_input = QLineEdit()
        self.path_input.setFixedHeight(30)
        self.path_input.setPlaceholderText('Type where to save images here...')
      
        # menubar
        about_action = QAction('About writer', self)
        about_action.triggered.connect(self.about_writer)
        version_action = QAction('Version info', self)
        version_action.triggered.connect(self.show_version)
        menubar_bar = self.menuBar()
        about = menubar_bar.addMenu('About')
        about.addAction(about_action)
        about.addAction(version_action)
       
        # widgets
        btn_ScrapImg = QPushButton('ScrapImg')
        btn_ScrapImg.setFixedHeight(30)
        btn_ScrapImg.clicked.connect(lambda: self.scrap_choice())
        btn_ScrapImg.setFixedWidth(60)
        btn_SavePath = QPushButton('SavePath')
        btn_SavePath.setFixedHeight(30)
        btn_SavePath.clicked.connect(lambda: self.choose_path())
        btn_SavePath.setFixedWidth(60)
        # setting_layout
        brower_ChoiceLabel = QLabel('Browser')
        brower_ChoiceLabel.setFixedHeight(30)
        self.brower_Choice = QComboBox()
        self.brower_Choice.setFixedHeight(30)
        self.brower_Choice.addItems(['Baidu', 'Google'])
        img_NumLabel = QLabel('   Num')
        img_NumLabel.setFixedHeight(30)
        self.img_Num = QLineEdit()
        self.img_Num.setFixedHeight(30)
        self.img_Num.setPlaceholderText('0')
        null_Label = QLabel()
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(btn_SavePath)
        scrap_layout = QHBoxLayout()
        scrap_layout.addWidget(self.keyword_input)
        scrap_layout.addWidget(btn_ScrapImg)
        setting_layout = QHBoxLayout()
        setting_layout.addWidget(brower_ChoiceLabel, 2, Qt.AlignRight)
        setting_layout.addWidget(self.brower_Choice, 3, Qt.AlignLeft)
        setting_layout.addWidget(img_NumLabel, 1, Qt.AlignRight)
        setting_layout.addWidget(self.img_Num, 3, Qt.AlignLeft)
        setting_layout.addWidget(null_Label, 16)

        # program window design
        self.setFixedSize(720, 270)
        self.setWindowTitle("ImgScrap")
        self.setWindowIcon(QIcon('logo.png'))
        layout = QVBoxLayout()
        label_1 = QLabel('ImgScrap')
        label_1.setAlignment(Qt.AlignCenter)
        label_1.setFont(QFont("Microsoft YaHei", 18))
        label_2 = QLabel('   # Click SavePath or edit path to set where to save imgaes scraped\n   # Input search keywords and then images will be scraped soon')
        label_2.setAlignment(Qt.AlignLeft)
        label_2.setFont(QFont("Microsoft YaHei", 12))
        label_3 = QLabel('Simple Guide')
        label_3.setAlignment(Qt.AlignCenter)
        label_3.setFont(QFont("Microsoft YaHei", 15))
        layout.addWidget(label_1)
        layout.addWidget(label_3)
        layout.addWidget(label_2)
        layout.addLayout(setting_layout)
        layout.addLayout(path_layout)
        layout.addLayout(scrap_layout)
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(layout)
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    # choose img save path
    def choose_path(self):
        file_dialog = QFileDialog()
        self.img_path = file_dialog.getExistingDirectory(self, "File Explorer", os.getcwd())
        self.path_input.setText(self.img_path)

    # about_writer
    def about_writer(self): 
        QMessageBox.about(self, "Hello", "Hi I'm IcedOtaku\nSearch my name in github.com to find more")

    # show_version
    def show_version(self): 
        QMessageBox.about(self, "Version", "Version 0.0.1")

    # scrap choice
    def scrap_choice(self):
        if os.path.exists(self.path_input.text()) == False:
            QMessageBox.about(self, "Alert", "Please input correct save path")
            return
        if self.keyword_input.text() == '':
            QMessageBox.about(self, "Alert", "Please input search keyword")
            return
        if self.brower_Choice.currentText() == 'Baidu':
            self.baidu_scrap_process()
        else:
            self.google_scrap_process()
    
    # google scrap img process
    def google_scrap_process(self):
        print("gooooo")
        QMessageBox.about(self, "Attention","Let the brower remain top in windows")
        google_url_part1 = 'https://www.google.com/search?q='
        google_url_part2 = '&source=lnms&tbm=isch'
        location_driver = 'chromedriver.exe'
        url = google_url_part1 + self.keyword_input.text() + google_url_part2
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(executable_path=location_driver, chrome_options=chrome_options)
        driver.maximize_window()
        driver.get(url)
        # 记录下载过的图片地址，避免重复下载
        img_url_dic = {}
        count = 0
        target_num = int(self.img_Num.text())
        pos = 0
        while True:
            pos += 500
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            html_page = driver.page_source
            soup = bs(html_page, "html.parser")
            img_list = soup.findAll('img', {'class': 'rg_ic rg_i'})
            for img_url in img_list:
                print(count, end=' ')
                if img_url['src'] not in img_url_dic:
                    if self.img_path == '':
                        target = '{}/{}.jpg'.format(self.path_input.text(), count)
                    else:
                        target = '{}/{}.jpg'.format(self.img_path, count)
                    img_url_dic[img_url['src']] = ''
                    urllib.request.urlretrieve(img_url['src'], target)
                    count = count + 1
                    if count == target_num:
                        break
            if count == target_num:
                driver.close()
                QMessageBox.about(self, "Congratulations","Images have been scraped down")
                break
                
    # baidu scrap img process        
    def baidu_scrap_process(self):
        QMessageBox.about(self, "Attention", "Let the brower remain top in windows")
        baidu_url_part1 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
        baidu_url_part2 = '&oq=bagua&rsp=0'
        location_driver = 'chromedriver.exe'
        url = baidu_url_part1 + self.keyword_input.text() + baidu_url_part2
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(executable_path=location_driver, chrome_options=chrome_options)
        driver.maximize_window()
        driver.get(url)
        # 记录下载过的图片地址，避免重复下载
        img_url_dict = {}
        count = 0
        target_num = int(self.img_Num.text())
        pos = 0
        while True:
            pos += 500
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            html_page = driver.page_source
            soup = bs(html_page, "html.parser")
            img_list = soup.findAll('img', {'src': re.compile(r'https:.*\.(jpg|png)')})
            for img_url in img_list:
                if img_url['src'] not in img_url_dict:
                    if self.img_path=='':
                        target = '{}/{}.jpg'.format(self.path_input.text(), count)
                    else:
                        target = '{}/{}.jpg'.format(self.img_path, count)
                    img_url_dict[img_url['src']] = ''
                    urllib.request.urlretrieve(img_url['src'], target)
                    count = count + 1
                    if count == target_num:
                        break
            if count == target_num:
                driver.close()
                QMessageBox.about(self, "Congratulations", "Images have been scraped down")
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    run = ImgScrap()
    run.show()
    sys.exit(app.exec_())
