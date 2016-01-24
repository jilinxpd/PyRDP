# -*- coding:utf8 -*-
import re
from control import public
import sys
import os
from PyQt4 import QtCore, QtGui, uic
import rdpInstance
from types import MethodType


qtCreatorFile = "ui/rdcD.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class RDPDialog(QtGui.QDialog, Ui_QDialog):

    def __init__(self, ip, userName, blacklist = None):
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        self.resize(391, 151)
        self.optionWidget.hide()

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('img/rdc.ico'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.colorDepthMap = [15, 16, 24, 32]

        self.driveNameMap = {'0': '未知',
                             '1':'无根目录',
                             '2':'可移动磁盘',
                             '3':'本地磁盘',
                             '4':'网络驱动器',
                             '5':'CD 驱动器',
                             '6':'虚拟内存盘'}
        if blacklist is None:
            #self.blacklist = {"drives": ["C:", "D:"], "devices": ["*"]}
            self.blacklist = {"drives": [], "devices": []}
        else:
            self.blacklist = blacklist

        self.initEquipConent()

        self.initMetics()
        self.horizontalSlider.setRange(0, len(self.metricsMap)-1)

        self.rdpFilePath = None

        self.initTmpFolder()

        self.addListener()

        self.rdpInstance = rdpInstance.RDPInstance()
        self.setDefaultRDP()
        self.cmpLineEdit.setText(ip)
        self.accountTxtLable.setText(userName)

    def setDefaultRDP(self):
        self.connBarCheckBox.setCheckState(QtCore.Qt.Checked)
        self.printCheckBox.setCheckState(QtCore.Qt.Checked)
        self.cliCheckBox.setCheckState(QtCore.Qt.Checked)
        self.reconnCheckBox.setCheckState(QtCore.Qt.Checked)
        self.authComboBox.setCurrentIndex(2)
        self.cmpLineEdit.setText("")
        self.accountTxtLable.setText("")
        self.cmpLineEdit_2.setText("")
        self.accountTxtLable_2.setText("")
        self.audioCaptureComBox.setCurrentIndex(0)
        self.audioPlayComBox.setCurrentIndex(0)
        self.keyComBox.setCurrentIndex(2)
        self.smartCardCheckBox.setCheckState(QtCore.Qt.Checked)
        self.portCheckBox.setCheckState(QtCore.Qt.Checked)
        self.colorComboBox.setCurrentIndex(3)
        self.connTypeComboBox.setCurrentIndex(5)
        self.horizontalSlider.setValue(len(self.metricsMap)-1)

    def addListener(self):
        def toOptionDWidget():
            self.cmpLineEdit_2.setText(self.cmpLineEdit.text())
            self.accountTxtLable_2.setText(self.accountTxtLable.text())
            self.resize(411, 346)
            self.defaultWidget.hide()
            self.optionWidget.show()
        self.optionToolBtn.clicked.connect(toOptionDWidget)

        def toDefaultDWidget():
            self.cmpLineEdit.setText(self.cmpLineEdit_2.text())
            self.accountTxtLable.setText(self.accountTxtLable_2.text())
            self.resize(391, 151)
            self.optionWidget.hide()
            self.defaultWidget.show()
        self.optionToolBtn_2.clicked.connect(toDefaultDWidget)

        def defaultConnectFunc():
            if not self.connectRDP():
                self.statusLabel.setText(u'请输入合法的IP地址')
        self.connBtn.clicked.connect(defaultConnectFunc)

        def optionConnectFunc():
            if not self.connectRDP():
                self.statusLabel_2.setText(u'请输入合法的IP地址')
        self.connBtn_2.clicked.connect(optionConnectFunc)

        self.openBtn.clicked.connect(self.openFile)

        self.saveBtn.clicked.connect(self.saveFile)

        self.saveasBtn.clicked.connect(self.saveAsFile)

        def connBarCheckBox_stateChanged(state):
            self.rdpInstance.set_displayconnectionbar(state == QtCore.Qt.Checked)
        self.connBarCheckBox.stateChanged.connect(connBarCheckBox_stateChanged)

        def printCheckBox_stateChanged(state):
            self.rdpInstance.set_redirectprinters(state == QtCore.Qt.Checked)
        self.printCheckBox.stateChanged.connect(printCheckBox_stateChanged)

        def cliCheckBox_stateChanged(state):
            self.rdpInstance.set_redirectclipboard(state == QtCore.Qt.Checked)
        self.cliCheckBox.stateChanged.connect(cliCheckBox_stateChanged)

        def reconnCheckBox_stateChanged(state):
            self.rdpInstance.set_autoreconnection(state == QtCore.Qt.Checked)
        self.reconnCheckBox.stateChanged.connect(reconnCheckBox_stateChanged)

        def authComboBox_stateChanged(index):
            self.rdpInstance.set_authentication_level(index)
        self.authComboBox.currentIndexChanged.connect(authComboBox_stateChanged)

        def cmpLineEdit_2_stateChanged(data):
            self.rdpInstance.set_full_address(data)
        self.cmpLineEdit_2.textChanged.connect(cmpLineEdit_2_stateChanged)

        def audioCaptureComBox_stateChanged(index):
            self.rdpInstance.set_audiocapturemode(index)
        self.audioCaptureComBox.currentIndexChanged.connect(audioCaptureComBox_stateChanged)

        def audioPlayComBox_stateChanged(index):
            self.rdpInstance.set_audiomode(index)
        self.audioPlayComBox.currentIndexChanged.connect(audioPlayComBox_stateChanged)

        def keyComBox_stateChanged(index):
            self.rdpInstance.set_keyboardhook(index)
        self.keyComBox.currentIndexChanged.connect(keyComBox_stateChanged)

        def smartCardCheckBox_stateChanged(state):
            self.rdpInstance.set_redirectsmartcards(state == QtCore.Qt.Checked)
        self.smartCardCheckBox.stateChanged.connect(smartCardCheckBox_stateChanged)

        def portCheckBox_stateChanged(state):
            self.rdpInstance.set_redirectcomports(state == QtCore.Qt.Checked)
        self.portCheckBox.stateChanged.connect(portCheckBox_stateChanged)

        def colorComboBox_stateChanged(index):
            self.rdpInstance.set_session_bpp(self.colorDepthMap[index])
        self.colorComboBox.currentIndexChanged.connect(colorComboBox_stateChanged)

        def connTypeComboBox_stateChanged(index):
            if index == 0:
                self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Unchecked)
            elif index == 1:
                self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
            elif index == 2:
                self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
            elif index == 3 or index == 4:
                self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Checked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
            else:
                self.backCheckBox.setCheckState(QtCore.Qt.Checked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Checked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Checked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Checked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Checked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
            self.rdpInstance.set_connection_type(index)
        self.connTypeComboBox.currentIndexChanged.connect(connTypeComboBox_stateChanged)

        def backCheckBox_stateChanged(state):
            self.rdpInstance.set_wallpaper(state == QtCore.Qt.Checked)
        self.backCheckBox.stateChanged.connect(backCheckBox_stateChanged)

        def fontCheckBox_stateChanged(state):
            self.rdpInstance.set_font_smoothing(state == QtCore.Qt.Checked)
        self.fontCheckBox.stateChanged.connect(fontCheckBox_stateChanged)

        def backCssCheckBox_stateChanged(state):
            self.rdpInstance.set_desktop_composition(state == QtCore.Qt.Checked)
        self.backCssCheckBox.stateChanged.connect(backCssCheckBox_stateChanged)

        def dragCheckBox_stateChanged(state):
            self.rdpInstance.set_full_window_drag(state == QtCore.Qt.Checked)
        self.dragCheckBox.stateChanged.connect(dragCheckBox_stateChanged)

        def menuCheckBox_stateChanged(state):
            self.rdpInstance.set_menu_anims(state == QtCore.Qt.Checked)
        self.menuCheckBox.stateChanged.connect(menuCheckBox_stateChanged)

        def viewCheckBox_stateChanged(state):
            self.rdpInstance.set_themes(state == QtCore.Qt.Checked)
        self.viewCheckBox.stateChanged.connect(viewCheckBox_stateChanged)

        def bitMapCheckBox_stateChanged(state):
            self.rdpInstance.set_bitmapcachepersistenable(state == QtCore.Qt.Checked)
        self.bitMapCheckBox.stateChanged.connect(bitMapCheckBox_stateChanged)

        def horizontalSlider_stateChanged(index):
            width = self.metricsMap[index][0]
            height = self.metricsMap[index][1]
            if(index == len(self.metricsMap) - 1):
                self.deskSizeLabel.setText(u'全屏')
            else:
                self.deskSizeLabel.setText(u'%s x %s 像素' % (width, height))
            self.rdpInstance.set_desktopwidth(width)
            self.rdpInstance.set_desktopheight(height)
        self.horizontalSlider.valueChanged.connect(horizontalSlider_stateChanged)


    def initTmpFolder(self):
        self.tmpFileFolder = os.path.join(os.getcwd(), 'tmp')
        if not os.path.isdir(self.tmpFileFolder):
            os.mkdir(self.tmpFileFolder)

    def initEquipConent(self):
        def itemDrive_setCheckState(this, col, state):
            this._setCheckState(col, state)
            name = unicode(this.text(0))
            #results = re.match("^.*\((.+:)\)$", name)
            self.rdpInstance.set_drivestoredirect(state == QtCore.Qt.Checked, name)

        def dynamicDrive_setCheckState(this, col, state):
            this._setCheckState(col, state)
            self.rdpInstance.set_drivestoredirect(state == QtCore.Qt.Checked, u"DynamicDrives")

        def dynamicDevice_setCheckState(this, col, state):
            this._setCheckState(col, state)
            self.rdpInstance.set_devicestoredirect(state == QtCore.Qt.Checked, u"DynamicDevices")

        def equipParentChangeWithChild(sitem):
            length = sitem.childCount()
            checkedSize = 0
            for i in range(0, length):
                if(sitem.child(i).checkState(0) == QtCore.Qt.Checked):
                    checkedSize += 1
            if(checkedSize == length):
                sitem._setCheckState(0, QtCore.Qt.Checked)
            elif(checkedSize == 0):
                sitem._setCheckState(0, QtCore.Qt.Unchecked)
            else:
                sitem._setCheckState(0, QtCore.Qt.PartiallyChecked)

        def equipClicked(item):
            if hasattr(item, "isDrive"):
                item.setCheckState(0, item.checkState(0))
            else:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, item.checkState(0))
            if(isinstance(item.parent(), QtGui.QTreeWidgetItem)):
                equipParentChangeWithChild(item.parent())

        def drives_setCheckState(this, col, state):
            this._setCheckState(col, state)
            for i in range(this.childCount()):
                this.child(i).setCheckState(0, state)


        if "*" not in self.blacklist["drives"]:
            self.drives = QtGui.QTreeWidgetItem(self.equipTreeWidget)
            self.drives.setText(0, u'驱动器')
            self.drives.setFlags(self.drives.flags() |
                                 QtCore.Qt.ItemIsUserCheckable)
            self.drives.setCheckState(0, QtCore.Qt.Unchecked)
            self.drives._setCheckState = self.drives.setCheckState
            self.drives.setCheckState = MethodType(drives_setCheckState, self.drives, QtGui.QTreeWidgetItem)

            data = os.popen('wmic logicaldisk get caption,drivetype,volumename').read()
            items = data.splitlines()
            for item in items[1:]:
                properties = item.split()
                if len(properties) < 1:
                    continue
                elif len(properties) < 3:
                    volName = self.driveNameMap[properties[1]].decode('UTF-8')
                else:
                    volName = properties[2].decode('GBK')
                if properties[0] in self.blacklist["drives"]:
                    continue
                itemStr = volName + ' (' + properties[0] + ')'
                itemDrive = QtGui.QTreeWidgetItem(self.drives)
                itemDrive.setText(0, itemStr)
                itemDrive.setFlags(itemDrive.flags() |
                                  QtCore.Qt.ItemIsUserCheckable)
                itemDrive.setCheckState(0, QtCore.Qt.Unchecked)
                itemDrive._setCheckState = itemDrive.setCheckState
                itemDrive.setCheckState = MethodType(itemDrive_setCheckState, itemDrive, QtGui.QTreeWidgetItem)
                itemDrive.isDrive = True
                self.drives.addChild(itemDrive)

            dynamicDrive = QtGui.QTreeWidgetItem(self.drives)
            dynamicDrive.setText(0, u'稍后插入的驱动器')
            dynamicDrive.setFlags(dynamicDrive.flags() |
                                  QtCore.Qt.ItemIsUserCheckable)
            dynamicDrive.setCheckState(0, QtCore.Qt.Unchecked)
            dynamicDrive._setCheckState = dynamicDrive.setCheckState
            dynamicDrive.setCheckState = MethodType(dynamicDrive_setCheckState, dynamicDrive, QtGui.QTreeWidgetItem)
            dynamicDrive.isDrive = True

        if "*" not in self.blacklist["devices"]:
            self.devices = QtGui.QTreeWidgetItem(self.equipTreeWidget)
            self.devices.setText(0, u'其他支持的即插即用(PnP)设备')
            self.devices.setFlags(self.devices.flags() |
                                  QtCore.Qt.ItemIsUserCheckable)
            self.devices.setCheckState(0, QtCore.Qt.Unchecked)
            self.devices._setCheckState = self.devices.setCheckState
            self.devices.setCheckState = MethodType(drives_setCheckState, self.devices, QtGui.QTreeWidgetItem)

            dynamicDevice = QtGui.QTreeWidgetItem(self.devices)
            dynamicDevice.setText(0, u'稍后插入的设备')
            dynamicDevice.setFlags(dynamicDevice.flags() |
                                   QtCore.Qt.ItemIsUserCheckable)
            dynamicDevice.setCheckState(0, QtCore.Qt.Unchecked)
            dynamicDevice._setCheckState = dynamicDevice.setCheckState
            dynamicDevice.setCheckState = MethodType(dynamicDevice_setCheckState, dynamicDevice, QtGui.QTreeWidgetItem)
            dynamicDevice.isDrive = True

        self.equipTreeWidget.itemClicked.connect(equipClicked)



    def connectRDP(self):
        if(public.isValidIP(self.rdpInstance.get_full_address())):
            self.saveFile(None)
            self.runCommand('mstsc %s' % self.rdpFilePath)
            return True
        else:
            return False


    def runCommand(self, cmdStr):
        stdouterr = os.popen4(str(cmdStr))[1].read()


    def openFile(self):
        openFilePath = unicode(QtGui.QFileDialog(self).getOpenFileName())
        if os.path.isfile(openFilePath):
            self.rdpFilePath = openFilePath
            self.updateView()

    def saveFile(self, fpath):
        if isinstance(fpath, unicode):
            self.rdpFilePath = fpath
        elif self.rdpFilePath is None or len(self.rdpFilePath) == 0:
            self.rdpFilePath = os.path.join(self.tmpFileFolder, 'rdp_%s.rdp' %
                self.cmpLineEdit_2.text())
        self.rdpInstance.write(self.rdpFilePath)

    def saveAsFile(self):
        saveAsFilePath = unicode(QtGui.QFileDialog(self).getSaveFileName())
        if len(saveAsFilePath) > 0:
            self.saveFile(saveAsFilePath)


    def updateView(self):
        tmp_rdpInstance = rdpInstance.RDPInstance()
        tmp_rdpInstance.read(self.rdpFilePath)
        stateMap = {True: QtCore.Qt.Checked, False: QtCore.Qt.Unchecked}

        self.setDefaultRDP()

        addr = tmp_rdpInstance.get_full_address()
        if addr is not None:
            self.cmpLineEdit_2.setText(addr)
            self.cmpLineEdit.setText(addr)

        disConnBar = tmp_rdpInstance.get_displayconnectionbar()
        if disConnBar is not None:
            self.connBarCheckBox.setCheckState(stateMap[disConnBar])

        printChkB = tmp_rdpInstance.get_redirectprinters()
        if printChkB is not None:
            self.printCheckBox.setCheckState(stateMap[printChkB])

        cliChkB = tmp_rdpInstance.get_redirectclipboard()
        if cliChkB is not None:
            self.cliCheckBox.setCheckState(stateMap[cliChkB])

        reconnChkB = tmp_rdpInstance.get_autoreconnection()
        if reconnChkB is not None:
            self.reconnCheckBox.setCheckState(stateMap[reconnChkB])

        authlevelComB = tmp_rdpInstance.get_authentication_level()
        if authlevelComB is not None:
            self.authComboBox.setCurrentIndex(int(authlevelComB))

        audioCaptureComB = tmp_rdpInstance.get_audiocapturemode()
        if audioCaptureComB is not None:
            self.audioCaptureComBox.setCurrentIndex(int(audioCaptureComB))

        audioPlayComB = tmp_rdpInstance.get_audiomode()
        if audioPlayComB is not None:
            self.audioPlayComBox.setCurrentIndex(int(audioPlayComB))

        keyComB = tmp_rdpInstance.get_keyboardhook()
        if keyComB is not None:
            self.keyComBox.setCurrentIndex(int(keyComB))

        smartCardChkB = tmp_rdpInstance.get_redirectsmartcards()
        if(smartCardChkB is not None):
            self.smartCardCheckBox.setCheckState(stateMap[smartCardChkB])

        portChkB = tmp_rdpInstance.get_redirectcomports()
        if(portChkB is not None):
            self.portCheckBox.setCheckState(stateMap[portChkB])

        drivesChkB = tmp_rdpInstance.get_drivestoredirect(u"*")
        if drivesChkB is not None:
            self.drives.setCheckState(0, QtCore.Qt.Checked)
        else:
            for i in xrange(self.drives.childCount()):
                driveItem = self.drives.child(i)
                name = unicode(driveItem.text(0))
                state = tmp_rdpInstance.get_drivestoredirect(name)
                if state is not None:
                    driveItem.setCheckState(0, QtCore.Qt.Checked)

        devicesChkB = tmp_rdpInstance.get_devicestoredirect(u"*")
        if devicesChkB is not None:
            self.devices.setCheckState(0, QtCore.Qt.Checked)
        else:
            for i in xrange(self.devices.childCount()):
                deviceItem = self.devices.child(i)
                name = unicode(deviceItem.text(0))
                state = tmp_rdpInstance.get_devicestoredirect(name)
                if state is not None:
                    deviceItem.setCheckState(0, QtCore.Qt.Checked)

        colorComB = tmp_rdpInstance.get_session_bpp()
        if(colorComB is not None):
            self.colorComboBox.setCurrentIndex(self.colorDepthMap.index(int(colorComB)))

        connTypeComB = tmp_rdpInstance.get_connection_type()
        if(connTypeComB is not None):
            self.connTypeComboBox.setCurrentIndex(int(connTypeComB))

        backChkB = tmp_rdpInstance.get_wallpaper()
        if(backChkB is not None):
            self.backCheckBox.setCheckState(stateMap[backChkB])

        fontChkB = tmp_rdpInstance.get_font_smoothing()
        if(fontChkB is not None):
            self.fontCheckBox.setCheckState(stateMap[fontChkB])

        layoutChkB = tmp_rdpInstance.get_desktop_composition()
        if(layoutChkB is not None):
                self.backCssCheckBox.setCheckState(stateMap[layoutChkB])

        dragChkB = tmp_rdpInstance.get_full_window_drag()
        if(dragChkB is not None):
            self.dragCheckBox.setCheckState(stateMap[dragChkB])

        menuChkB = tmp_rdpInstance.get_menu_anims()
        if(menuChkB is not None):
                self.menuCheckBox.setCheckState(stateMap[menuChkB])

        viewChkB = tmp_rdpInstance.get_themes()
        if(viewChkB is not None):
                self.viewCheckBox.setCheckState(stateMap[viewChkB])

        bitMapChkB = tmp_rdpInstance.get_bitmapcachepersistenable()
        if(bitMapChkB is not None):
                self.bitMapCheckBox.setCheckState(stateMap[bitMapChkB])

        width = tmp_rdpInstance.get_desktopwidth()
        height = tmp_rdpInstance.get_desktopheight()
        if width is not None and height is not None:
            if [int(width), int(height)] in self.metricsMap:
                self.horizontalSlider.setValue(self.metricsMap.index([int(width), int(height)]))

    def initMetics(self):
        def getMinIndexUp(val, numSet):
            low = 0
            high = len(numSet) - 1
            while low <= high:
                mid = (low + high) / 2
                midVal = numSet[mid]
                if(midVal < val):
                    low = mid + 1
                elif midVal > val:
                    high = mid - 1
                else:
                    return mid
            return low - 1
        width = [640, 800, 1024, 1280, 1366, 1440, 1600, 1680, 1920]
        height = [480, 600, 720, 768, 800, 900, 1024, 1050, 1080]

        geometry = QtGui.QApplication.desktop().screenGeometry()
        wi = geometry.width()
        hi = geometry.height()
        wIndex = getMinIndexUp(wi, width)
        hIndex = getMinIndexUp(hi, height)
        self.metricsMap = []
        for i in range(0, wIndex + 1):
            if(i <= hIndex):
                self.metricsMap.append([width[i], height[i]])
            else:
                self.metricsMap.append([width[i], height[hIndex]])
        if wIndex < hIndex:
            for i in(wIndex + 1, hIndex):
                self.metricsMap.append([width[wIndex], height[i]])

        if(width[wIndex] != wi or height[hIndex] != hi):
            self.metricsMap.append([wi, hi])

    def closeEvent(self, event):
        sys.exit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = RDPDialog(u"192.168.1.1", u"测试用户")
    dialog.show()
    sys.exit(app.exec_())
