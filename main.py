import sys

from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow, QToolBar, QLineEdit, QLabel, QFileDialog, QMessageBox, QApplication


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # setting up window
        self.setWindowTitle('J Browser')
        self.setWindowIcon(QIcon('resources/icon2.png'))

        # setting up web view
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(r"D:\Manbir\School\10th\Punjabi\ਪ੍ਰਾਰਥਨਾ Solutions.pdf"))

        self.setCentralWidget(self.web_view)

        # setting up toolbar
        tool_bar = QToolBar()
        tool_bar.setIconSize(QSize(30, 30))
        tool_bar.setMovable(False)
        self.addToolBar(tool_bar)

        # setting up toolbar actions and widgets
        back_action = QAction(QIcon('resources/arrow-back.png'), 'Back', self)
        back_action.setStatusTip('Go to Previous Page')
        back_action.triggered.connect(self.web_view.back)

        next_action = QAction(QIcon('resources/arrow-next.png'), 'Next', self)
        next_action.setStatusTip('Go next page')
        next_action.triggered.connect(self.web_view.forward)

        tool_bar.addActions([back_action, next_action])
        tool_bar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.httpsIcon = QLabel()

        tool_bar.addWidget(self.url_bar)
        tool_bar.addWidget(self.httpsIcon)

        tool_bar.addSeparator()

        stop_action = QAction(QIcon('resources/cancel.png'), 'Stop', self)
        stop_action.setStatusTip('Stop loading this page')
        stop_action.triggered.connect(self.web_view.stop)

        reload_action = QAction(QIcon('resources/reload.png'), 'Reload', self)
        reload_action.setStatusTip('Reload this page')
        reload_action.triggered.connect(self.web_view.reload)

        tool_bar.addActions([reload_action, stop_action])
        tool_bar.addSeparator()

        home_action = QAction(QIcon('resources/home.png'), 'Home', self)
        home_action.setStatusTip('Go to home')
        home_action.triggered.connect(
            lambda: self.web_view.setUrl(QUrl('https://www.google.com')))

        tool_bar.addAction(home_action)
        tool_bar.addSeparator()

        open_action = QAction(QIcon('resources/folder.png'), 'Open', self)
        open_action.setStatusTip('Open a file')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        tool_bar.addAction(open_action)
        tool_bar.addSeparator()

        about_action = QAction(QIcon('resources/info.png'), 'About', self)
        about_action.setStatusTip('About us')
        about_action.triggered.connect(self.about)

        tool_bar.addAction(about_action)

        # setting up web engine view actions
        self.web_view.urlChanged.connect(self.update_url_bar)
        self.web_view.loadProgress.connect(lambda progress: print(f'Loaded: {progress}%'))
        self.web_view.titleChanged.connect(lambda new_title: self.setWindowTitle(f'{new_title} | J Browser'))
        # self.web_view.iconUrlChanged.connect(lambda new_icon_url: self.setWindowIcon(QIcon(new_icon_url)))

    def update_url_bar(self, q):
        # if q.scheme() == 'https':
        #     self.httpsIcon.setPixmap(QPixmap('resources/secure.png'))
        #
        # elif q.scheme() == 'http':
        #     self.httpsIcon.setPixmap(QPixmap('resources/unsecure.png'))
        #
        # elif q.scheme() == 'file':
        #     self.httpsIcon.setPixmap(QPixmap('resources/file.png'))

        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())

        if q.scheme() == '':
            q.setScheme('https')

        self.web_view.setUrl(q)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory='',
            filter='HTML Files (*.html);; All Files (*.*)'
        )

        if path:
            self.web_view.setUrl(QUrl.fromLocalFile(localfile=path))
        else:
            pass

    def about(self):
        msg_box = QMessageBox(parent=self)

        msg_box.setWindowTitle('About J Browser')
        with open('resources/about.txt.html', 'r') as f:
            msg_box.setText(f.read())

        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    browser_win = MainWindow()
    browser_win.show()

    sys.exit(app.exec())
