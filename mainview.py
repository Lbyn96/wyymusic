#写一个界面
#有搜索框和搜索按钮，显示结果界面
#搜索框输入关键字，点击搜索按钮，显示搜索结果

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
    'cookie': '_ntes_nnid=467b23a61f007c739744af38f4babce0,1666157996344; _ntes_nuid=467b23a61f007c739744af38f4babce0; NMTID=00OJtldceXGuWoytUV5n2J3Z-grS-gAAAGD7sFpFw; WEVNSM=1.0.0; WNMCID=eylrum.1666157996686.01.0; WM_NI=UMdxgGRceZ0MfBjxGcIpENVWe6AGYNNRD4SqApRsD+Hz9WFJ8d04/ZFIZn5T2Yy5lmqHxg4aaA6HIdwFXRV65Fc8EFvk1VXScZUFZDWJI2ciq7XuVrmLsbFILEz/ADnmUXU=; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8ef65fa898b696ee7df5e78fa7c55f828b8a86c154f5a7c0d6c169b4b1a5a3b12af0fea7c3b92a9793ac99e64d92bdabbbb347a69ea699c6698bb08bafd55da7ea8fa8dc468e8e8cd5d27b83b09e94c7218ca6f7b8c542fcbc00d5ae528697968fb860f287b7d6ef67b398b888b76ba39ffaa9cc70b59a98b3d53ef79aadd9c84eb6b5ffb7db59a1869ba7d950959687d3e263b3e99896d57aaf94bd83c543909bb6d0c450aeb39bb9d837e2a3; WM_TID=T2eydeqiV4ZBVRFVBRbFCrmssRc48wFi; __snaker__id=6hJyTGx5uG8qbBWy; gdxidpyhxdE=Xf038Wc4AmoiO1ldvZB782uaa\chQLX0CyNdZ21qD2QZ9utZvr6ZpoRdWc/yMWw2UOUtESMh\vxoOsIeAH/A91QhlyLIJAoUkmVs8tAygQE90c\Wq95jvoM/thvySfHSpSY1bDESK0uIqjcf+/i9/NQox0pmvvJ7565\fVJMsRS3xrOP:1666159109817; YD00000558929251:WM_NI=96foAgKV7HRFYmzkeoaNJL5XWAjHn3QfAoMcBsF5kAxdz2eumRQgOl1btBbYeS5E79QkHOuzvOVMUp3VgILQTTEUJw39XzgB2ZrqZ7RP1GTWWUmNbX5DO6lHOvNXRVzAdEg=; YD00000558929251:WM_NIKE=9ca17ae2e6ffcda170e2e6eed5cc39f8bebf91f842f6868eb3c14e838b8fadc14db3b7f8d5c759a8b686a7d12af0fea7c3b92afbeaaa90c46d898af9a9d14e9bb3b68ce865a39286adb854959fa6a9ed3993ba8f90d06982ad8ad6ea4bbcbcb6d3e87faf8e9f88ce68f3bebca3e153a78dfba6b63393b588b0f872b6919aaed87cf18aa9aacf5b988c8bb6c97df1e7989be64af286be92d93d9290ffa8d75d958ba3afe154f79c81d7ef448daa82b9d15eba9faca6e637e2a3; YD00000558929251:WM_TID=IEA0fD7iRgRFFEEEUUPBH/j98XXN3YVA; MUSIC_U=f8bb9a871a271a022590a0ea65d0b182605b71f1e46b0aaed17fba7b4fde6fe858323a99dde6a55565ab267a4f8a3b1061a09b8d102e82636bbcbe0f7bd40b1580cc10d95dec96a7abcbf7551dcd336e867e1a3428a0de18c55792a47c98c1db090f3ad7c86ad1db; __csrf=abb207e1dc2eab343523ef2537afa18e; ntes_kaola_ad=1; _iuqxldmzr_=32; JSESSIONID-WYYY=6W5+i5XHQIGhUSTlkwBAKjNYsxVhDoduXpCe+\pMHg0E2EfvjsyevM5OAYxMj719cdbs+k7s9fqlpfuw+2SZeE+jEIo0hU3k\mBEqAIDd0ys7vrCsxbySrExHDT+WAUoFsbSbZYgAOw/VE0csSC7bG6dZbakgwZWRa2zpHqi9s4UYlsV:1666161749872',
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