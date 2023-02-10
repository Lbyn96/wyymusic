import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
import main1
import requests

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # 初始化界面
    def initUI(self):
        #展示搜索框，搜索按钮和搜索结果
        self.searchEdit = QLineEdit()
        self.searchBtn = QPushButton("搜索")
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(3)
        self.resultTable.setHorizontalHeaderLabels(['歌名', '在线播放', '下载'])
        self.resultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resultTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.resultTable.setAlternatingRowColors(True)
        self.resultTable.verticalHeader().setVisible(False)

        #设置布局
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.searchEdit, 1, 0)
        grid.addWidget(self.searchBtn, 1, 1)
        grid.addWidget(self.resultTable, 2, 0, 1, 2)
        self.setLayout(grid)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('搜索音乐')
        self.show()

        #绑定搜索按钮事件
        self.searchBtn.clicked.connect(self.search)

        #绑定搜索框回车事件
        self.searchEdit.returnPressed.connect(self.search)

        #绑定在线播放按钮事件
        self.resultTable.cellClicked.connect(self.play)

        #绑定下载按钮事件
        self.resultTable.cellClicked.connect(self.download)

    #搜索按钮事件
    def search(self):
        #获取搜索框内容
        keyword = self.searchEdit.text()
        #调用搜索方法
        result = main1.search(keyword)
        # print(result)

        #清空搜索结果
        self.resultTable.clearContents()
        #设置行数
        self.resultTable.setRowCount(len(result))
        #显示搜索结果
        for i in range(len(result)):
            self.resultTable.setItem(i, 0, QTableWidgetItem(result[i]['name']))
            if 'http' not in result[i]['url']:
                self.resultTable.setItem(i, 1, QTableWidgetItem('无资源'))
                self.resultTable.setItem(i, 2, QTableWidgetItem('无资源'))
            else:
                self.resultTable.setItem(i, 1, QTableWidgetItem('在线播放'))
                self.resultTable.setItem(i, 2, QTableWidgetItem('下载'))
            #将对应的歌曲链接保存到临时存储中
            self.resultTable.item(i, 1).setData(Qt.UserRole, result[i]['url'])
            self.resultTable.item(i, 2).setData(Qt.UserRole, result[i]['url'])
            

    #在线播放按钮事件
    def play(self, row, col):
        if col == 1:
            #获取歌曲链接
            url = self.resultTable.item(row, col).data(Qt.UserRole)
            #python 直接打开链接
            import webbrowser
            webbrowser.open(url)

    #下载按钮事件
    def download(self, row, col):
        if col == 2:
            #获取歌曲链接
            url = self.resultTable.item(row, col).data(Qt.UserRole)
            # 去除“"”
            url = url.replace('"', '')
            headers = {
    # 用户身份信息
    'cookie': '用户cookie',
    # 浏览器信息
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
}
            song_response = requests.get(url=url,headers=headers)
            music_data = song_response.content
            #下载到桌面，判断桌面是否有music文件夹，没有则创建
            import os
            desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
            music_path = os.path.join(desktop, 'music')
            if not os.path.exists(music_path):
                os.mkdir(music_path)
            #写入文件
            song_name = self.resultTable.item(row, 0).text()
            with open(music_path + '/' + song_name + '.mp3', 'wb') as f:
                f.write(music_data)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainView = MainView()
    mainView.show()
    sys.exit(app.exec_())
