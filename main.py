from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl('https://www.google.com'))

        self.setCentralWidget(self.web_view)

        tool_bar = QToolBar()
        tool_bar.setIconSize(QSize(30, 30))
        tool_bar.setMovable(False)
        self.addToolBar(tool_bar)

        back_action = QAction(QIcon('Stuff/back.png'), 'Back', self)
        back_action.setStatusTip('Go to Previous Page')
        back_action.triggered.connect(self.web_view.back)

        next_action = QAction(QIcon('Stuff/next.png'), 'Next', self)
        next_action.setStatusTip('Go next page')
        next_action.triggered.connect(self.web_view.forward)

        tool_bar.addActions([back_action, next_action])

        tool_bar.addSeparator()

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate_to_url)
        tool_bar.addWidget(self.urlBar)

        self.httpsIcon = QLabel()
        tool_bar.addWidget(self.httpsIcon)

        tool_bar.addSeparator()

        stop_action = QAction(QIcon('Stuff/stop.png'), 'Stop', self)
        stop_action.setStatusTip('Stop loading this page')
        stop_action.triggered.connect(self.web_view.stop)

        reload_action = QAction(QIcon('Stuff/reload.png'), 'Reload', self)
        reload_action.setStatusTip('Reload this page')
        reload_action.triggered.connect(self.web_view.reload)

        tool_bar.addActions([reload_action, stop_action])
        tool_bar.addSeparator()

        home_action = QAction(QIcon('Stuff/home.png'), 'Home', self)
        home_action.setStatusTip('Go to home')
        home_action.triggered.connect(
            lambda: self.web_view.setUrl(QUrl('https://www.google.com')))

        tool_bar.addAction(home_action)
        tool_bar.addSeparator()

        open_action = QAction(QIcon('Stuff/open.png'), 'Open', self)
        open_action.setStatusTip('Open a file')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        tool_bar.addAction(open_action)
        tool_bar.addSeparator()

        about_action = QAction(QIcon('Stuff/about.png'), 'About', self)
        about_action.setStatusTip('About us')
        about_action.triggered.connect(self.about)

        tool_bar.addAction(about_action)

        self.web_view.urlChanged.connect(self.update_url_bar)

        self.setWindowTitle('J Browser')
        self.setWindowIcon(QIcon('Stuff/icon2.png'))

    def update_url_bar(self, q):
        if q.scheme() == 'https':
            self.httpsIcon.setPixmap(QPixmap('Stuff/lock.png'))

        elif q.scheme() == 'http':
            self.httpsIcon.setPixmap(QPixmap('Stuff/warning.png'))

        elif q.scheme() == 'file':
            self.httpsIcon.setPixmap(QPixmap('Stuff/file.png'))

        self.urlBar.setText(q.toString())
        self.urlBar.setCursorPosition(0)

    def navigate_to_url(self):
        q = QUrl(self.urlBar.text())

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
        QMessageBox.about(self,
                          caption="About J Browser",
                          text="""<p style = 'font-family: sans-serif; font-size: 15px;'>The <b>J Browser</b> is a web 
                          browser_win developed by <b>Manbir Singh Judge</b> \n in <b>Python</b> programming language 
                          using <b>PyQt5</b> package. You can do anything \n with this browser_win that you are able to 
                          do with famous web browsers like <b>Google</b>, <b>FireFox</b>, \n <b>Microsoft Edge</b> 
                          etc. except that you can not login into you google account due to Google's \n security 
                          reasons.</p> <p style = 'font-family: sans-serif; font-size: 15px;'>This web browser_win is 
                          very simple but not as simple as you except because you can go back and \n forward in 
                          history of your pages, you can go to home page which is <b>https://www.google.com</b>, 
                          \n you can also open local HTML documents and this browser_win can also tell you that web page 
                          you have \n opened is secure or not or is a local HTML file.</p> <p style = 'font-family: 
                          sans-serif; font-size: 15px;'><b>Some disadvantages:</b> <ol> <li>You can not login into 
                          google account.</li> <li>You can not open multiple tabs at ones.</li> <li>This is slower 
                          than other web browser_win.</li> </ol></p>""")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    browser_win = MainWindow()
    browser_win.show()

    sys.exit(app.exec_())
