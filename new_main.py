import json
import logging
import sys
from typing import List
from uuid import uuid4

from PySide6.QtCore import QUrl, Signal as QSignal, QSize, QObject, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QMainWindow, QApplication, QToolBar, QVBoxLayout, QWidget, QTabWidget, QTabBar,
                               QPushButton, QLineEdit, QProgressBar)

from ui import Ui_MainWindow

log_formatter = logging.Formatter(fmt='%(asctime)s: %(name)s - [%(levelname)s] %(message)s')

log_handler = logging.FileHandler(f'{__name__}.log')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


class BrowserTabBar(QTabBar):
    new_tab_requested = QSignal()

    def __init__(self):
        super().__init__()

        self.setMovable(True)
        self.setTabsClosable(True)

        self.plus_btn = QPushButton("+")

        self.plus_btn.setParent(self)
        self.plus_btn.setFixedSize(12, 20)
        self.plus_btn.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_T))
        self.plus_btn.clicked.connect(self.new_tab_requested.emit)

        self.move_plus_btn()

    def sizeHint(self):
        size_hint = QTabBar.sizeHint(self)

        width = size_hint.width()
        height = size_hint.height()

        new_size = QSize(width, height)

        return new_size

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.move_plus_btn()

    def tabLayoutChange(self):
        super().tabLayoutChange()
        self.move_plus_btn()

    def move_plus_btn(self):
        # find the width of all the tabs
        total_tab_width = sum([self.tabRect(i).width() for i in range(self.count())])

        # set the plus button location in a visible area
        t = self.geometry().top()
        w = self.width()
        h = self.height()

        if total_tab_width > w:  # show just to the left of the scroll buttons
            self.plus_btn.move(w - 40, t)
        else:
            self.plus_btn.move(total_tab_width - 10, t + ((h // 2) - (self.plus_btn.height() // 2)))


class BrowserTab(QObject):
    title_changed = QSignal(str)  # new_title
    bookmark_requested = QSignal(str, str, str)  # title, url, icon url

    def __init__(self, parent_tabs: QTabWidget):
        super().__init__()

        self.parent_tabs = parent_tabs
        self.uid = uuid4()
        self.title = f'Tab {self.uid}'

        self.tab_widget = QWidget()
        self.tab_widget.setObjectName(f'tab_{self.uid}')

        self.tab_layout = QVBoxLayout()

        self.setup_web_view()
        self.setup_toolbar()
        self.setup_progress_bar()

        self.tab_layout.addWidget(self.tool_bar)
        self.tab_layout.addWidget(self.tab_web_view)
        self.tab_layout.addWidget(self.progress_bar)

        self.tab_widget.setLayout(self.tab_layout)

        self.tab_index = self.parent_tabs.addTab(self.tab_widget, f'Tab {self.uid}')

    def setup_toolbar(self):
        self.tool_bar = QToolBar(self.tab_widget)

        self.tool_bar.setObjectName(f"toolbar_page_{self.uid}")
        self.tool_bar.setEnabled(True)

        self.setup_toolbar_actions()

    def setup_progress_bar(self):
        self.progress_bar = QProgressBar(self.tab_widget)

        self.progress_bar.setObjectName(f'tab_{self.uid}_progress_bar')
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(14)
        self.progress_bar.setVisible(False)

        self.tab_layout.addWidget(self.progress_bar)

    def setup_web_view(self):
        def on_title_changed(new_title: str):
            self.title = new_title

            self.parent_tabs.setTabText(self.tab_index, self.title)
            self.title_changed.emit(str(self.title))

        self.tab_web_view = QWebEngineView()
        self.tab_web_view.setUrl(QUrl('https://www.google.com'))

        self.tab_web_view.urlChanged.connect(self.on_url_updated)
        self.tab_web_view.titleChanged.connect(on_title_changed)
        self.tab_web_view.loadStarted.connect(lambda: self.progress_bar.setVisible(True))
        self.tab_web_view.loadProgress.connect(lambda progress: self.progress_bar.setValue(progress))
        self.tab_web_view.loadFinished.connect(lambda: self.progress_bar.setVisible(False))

    def setup_toolbar_actions(self):
        def update_url():
            new_url = QUrl(self.toolbar_url_edit.text())

            if new_url.scheme() == '':
                new_url.setScheme('https')

            self.tab_web_view.setUrl(new_url)

        def on_bookmark_clicked():
            self.bookmark_requested.emit(
                self.title,
                self.tab_web_view.url().toString(),
                self.tab_web_view.iconUrl().toString()
            )

        self.toolbar_action_back = QAction(parent=self.tool_bar, text='Back', icon=QIcon('resources/arrow-back.png'))
        self.toolbar_action_back.triggered.connect(lambda: self.tab_web_view.back())

        self.toolbar_action_next = QAction(parent=self.tool_bar, text='Next', icon=QIcon('resources/arrow-next.png'))
        self.toolbar_action_next.triggered.connect(lambda: self.tab_web_view.forward())

        self.toolbar_action_reload = QAction(parent=self.tool_bar, text='Reload', icon=QIcon('resources/reload.png'))
        self.toolbar_action_reload.triggered.connect(lambda: self.tab_web_view.reload())

        self.toolbar_action_home = QAction(parent=self.tool_bar, text='Home', icon=QIcon('resources/home.png'))
        self.toolbar_action_home.triggered.connect(lambda: self.tab_web_view.setUrl(QUrl('https://www.google.com')))

        self.toolbar_action_bookmark = QAction(parent=self.tool_bar, text='Bookmark',
                                               icon=QIcon('resources/bookmark.svg'))
        self.toolbar_action_bookmark.triggered.connect(on_bookmark_clicked)

        self.toolbar_url_edit = QLineEdit()
        self.toolbar_url_edit.returnPressed.connect(update_url)

        self.tool_bar.addAction(self.toolbar_action_back)
        self.tool_bar.addAction(self.toolbar_action_next)
        self.tool_bar.addAction(self.toolbar_action_reload)
        self.tool_bar.addAction(self.toolbar_action_home)
        self.tool_bar.addAction(self.toolbar_action_bookmark)
        self.tool_bar.addWidget(self.toolbar_url_edit)

    def on_url_updated(self, new_url: QUrl):
        self.toolbar_url_edit.setText(new_url.toString())
        self.toolbar_url_edit.setCursorPosition(0)


class Bookmark:
    def __init__(self, uuid: str, title: str, url: str, icon_url: str, location: str):
        self.uuid = uuid
        self.title = title
        self.url = url
        self.icon_url = icon_url
        self.location = location

    def __str__(self):
        return f'Bookmark - {self.uuid}\n\tTitle: {self.title}\n\tURL: {self.url}\n\tIcon URL: {self.icon_url}\n' \
               f'\tLocation: {self.location}'

    def __dict__(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'url': self.url,
            'icon-url': self.icon_url,
            'location': self.location,
        }


class Bookmarks(QObject):
    bookmarks_loaded = QSignal(List[Bookmark])

    def __init__(self, bookmarks_path: str):
        super().__init__()

        self.bookmarks_path = bookmarks_path

        self.bookmarks: List[Bookmark] = []

        self.load_bookmarks()

    def load_bookmarks(self):
        with open(self.bookmarks_path, 'r') as bookmarks_f:
            for bookmark in json.load(bookmarks_f):
                self.bookmarks.append(Bookmark(
                    uuid=bookmark['uuid'],
                    title=bookmark['title'],
                    url=bookmark['url'],
                    icon_url=bookmark['icon-url'],
                    location=bookmark['location']
                ))

    def add_bookmark(self, text: str, url: str, icon_url: str, location: str = '/'):
        self.bookmarks.append(Bookmark(
            uuid=str(uuid4()),
            title=text,
            url=url,
            icon_url=icon_url,
            location=location
        ))

        with open(self.bookmarks_path, 'w') as bookmarks_f:
            _: List[dict] = []

            for __ in self.bookmarks:
                _.append(__.__dict__())

            json.dump(_, bookmarks_f)

        self.load_bookmarks()

    def remove_bookmark(self, bookmark_id):
        pass


class MainWindow(QMainWindow):
    BOOKMARKS_PATH = 'resources/bookmarks.json'

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.tabs: List[BrowserTab] = []

        self.bookmarks = Bookmarks(self.BOOKMARKS_PATH)

        self.setup_tabs()
        self.setup_shortcuts()

    def setup_tabs(self):
        def on_current_tab_changed(current_tab_i: int):
            current_tab = self.tabs[current_tab_i]

            self.setWindowTitle(f'{current_tab.title} | Browser J')

            current_tab.title_changed.connect(lambda new_title: self.setWindowTitle(f'{new_title} | Browser J'))
            current_tab.bookmark_requested.connect(lambda t, url, i_url: self.bookmarks.add_bookmark(t, url, i_url))

        self.ui.browser_tabs.removeTab(0)
        self.ui.browser_tabs.currentChanged.connect(on_current_tab_changed)

        self.tab_bar = BrowserTabBar()

        self.tab_bar.new_tab_requested.connect(lambda: self.add_tab())
        self.tab_bar.tabCloseRequested.connect(lambda tab_i: self.ui.browser_tabs.removeTab(tab_i))

        self.ui.browser_tabs.setTabBar(self.tab_bar)
        self.add_tab()

    def add_tab(self):
        new_tab = BrowserTab(parent_tabs=self.ui.browser_tabs)

        self.tabs.append(new_tab)
        self.ui.browser_tabs.setCurrentIndex(new_tab.tab_index)

    def setup_shortcuts(self):
        def on_reload_requested():
            self.tabs[self.ui.browser_tabs.currentIndex()].tab_web_view.reload()

        QShortcut(QKeySequence(Qt.CTRL | Qt.Key_R), self).activated.connect(on_reload_requested)
        QShortcut(QKeySequence(Qt.Key_F5), self).activated.connect(on_reload_requested)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec())
