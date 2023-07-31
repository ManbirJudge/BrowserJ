# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Browser J DesignycTcKP.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import (QStatusBar,
                               QTabWidget, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(873, 539)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.action_back = QAction(MainWindow)
        self.action_back.setObjectName(u"action_back")
        self.action_next = QAction(MainWindow)
        self.action_next.setObjectName(u"action_next")
        self.action_reload = QAction(MainWindow)
        self.action_reload.setObjectName(u"action_reload")
        self.action_home = QAction(MainWindow)
        self.action_home.setObjectName(u"action_home")
        self.action_bookmark = QAction(MainWindow)
        self.action_bookmark.setObjectName(u"action_bookmark")
        self.action_more = QAction(MainWindow)
        self.action_more.setObjectName(u"action_more")
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.browser_tabs = QTabWidget(self.central_widget)
        self.browser_tabs.setObjectName(u"browser_tabs")
        self.browser_tabs.setTabShape(QTabWidget.Rounded)
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.setMovable(True)

        self.verticalLayout.addWidget(self.browser_tabs)

        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.browser_tabs.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Browser J", None))
        self.action_back.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        # if QT_CONFIG(tooltip)
        self.action_back.setToolTip(
            QCoreApplication.translate("MainWindow", u"Go back to the back to the previous page.", None))
        # endif // QT_CONFIG(tooltip)
        self.action_next.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        # if QT_CONFIG(tooltip)
        self.action_next.setToolTip(QCoreApplication.translate("MainWindow", u"Go to the next page.", None))
        # endif // QT_CONFIG(tooltip)
        self.action_reload.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        # if QT_CONFIG(tooltip)
        self.action_reload.setToolTip(QCoreApplication.translate("MainWindow", u"Relaod the current page.", None))
        # endif // QT_CONFIG(tooltip)
        self.action_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        # if QT_CONFIG(tooltip)
        self.action_home.setToolTip(QCoreApplication.translate("MainWindow", u"Go back to the home page.", None))
        # endif // QT_CONFIG(tooltip)
        self.action_bookmark.setText(QCoreApplication.translate("MainWindow", u"Bookmark", None))
        # if QT_CONFIG(tooltip)
        self.action_bookmark.setToolTip(QCoreApplication.translate("MainWindow", u"Bookmark the current page.", None))
        # endif // QT_CONFIG(tooltip)
        self.action_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        # if QT_CONFIG(tooltip)
        self.action_more.setToolTip(QCoreApplication.translate("MainWindow", u"More optinos", None))
# endif // QT_CONFIG(tooltip)
# retranslateUi
