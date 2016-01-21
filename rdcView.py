# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
import rdpInstance
from types import MethodType


qtCreatorFile = "ui/rdcD.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyDialog(QtGui.QDialog, Ui_QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        # self.connBtn.clicked.connect(self.connectFunc)
        self.resize(391, 151)
        self.optionWidget.hide()

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('img/rdc.ico'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.driveNameMap = {'0': '未知',
                             '1':'无根目录',
                             '2':'可移动磁盘',
                             '3':'本地磁盘',
                             '4':'网络驱动器',
                             '5':'CD 驱动器',
                             '6':'虚拟内存盘'}
        self.initEquipConent()

        self.initMetics()
        self.horizontalSlider.setRange(0, len(self.metricsMap))

        self.rdpFilePath = None

        self.initTmpFolder()

        self.addListener()

        self.rdpInstance = rdpInstance.RDPInstance()

        # print self.colorComboBox.itemText(0).extracomment
        #self.setGeometry(300, 300, 250, 150)
        # self.connect(self.accountEdit, SIGNAL("returnPressed(void)"),
        #              self.runCommand


    def addListener(self):
        def toOptionDWidget():
            text=str(self.cmpLineEdit.text())
            if len(text):
                self.cmpLineEdit_2.setText(text)
            self.resize(411, 346)
            self.defaultWidget.hide()
            self.optionWidget.show()
        self.optionToolBtn.clicked.connect(toOptionDWidget)

        def toDefaultDWidget():
            text=str(self.cmpLineEdit_2.text())
            if len(text):
                self.cmpLineEdit.setText(text)
            self.resize(391, 151)
            self.optionWidget.hide()
            self.defaultWidget.show()
        self.optionToolBtn_2.clicked.connect(toDefaultDWidget)

        def defaultConnectFunc():
            self.connectRDP(self.cmpLineEdit.text())
        self.connBtn.clicked.connect(defaultConnectFunc)

        def optionConnectFunc():
            self.connectRDP(self.cmpLineEdit_2.text())
        self.connBtn_2.clicked.connect(optionConnectFunc)

        self.openBtn.clicked.connect(self.openFile)

        self.saveBtn.clicked.connect(self.saveFile)

        self.saveasBtn.clicked.connect(self.saveAsFile)

        def connBarCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_displayconnectionbar()
            else:
                self.rdpInstance.disable_displayconnectionbar()
        self.connBarCheckBox.stateChanged.connect(connBarCheckBox_stateChanged)

        def printCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_redirectprinters()
            else:
                self.rdpInstance.disable_redirectprinters()
        self.printCheckBox.stateChanged.connect(printCheckBox_stateChanged)

        def cliCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_redirectclipboard()
            else:
                self.rdpInstance.disable_redirectclipboard()
        self.cliCheckBox.stateChanged.connect(cliCheckBox_stateChanged)

        def reconnCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_autoreconnection()
            else:
                self.rdpInstance.disable_autoreconnection()
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
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_redirectsmartcards()
            else:
                self.rdpInstance.disable_redirectsmartcards()
        self.smartCardCheckBox.stateChanged.connect(smartCardCheckBox_stateChanged)

        def portCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_redirectcomports()
            else:
                self.rdpInstance.disable_redirectcomports()
        self.portCheckBox.stateChanged.connect(portCheckBox_stateChanged)

        def colorComboBox_stateChanged(index):
            self.rdpInstance.set_session_bpp(self.getColorComVal(index))
        self.colorComboBox.currentIndexChanged.connect(colorComboBox_stateChanged)

        def connTypeComboBox_stateChanged(index):
            self.rdpInstance.set_connection_type(index+1)
        self.connTypeComboBox.currentIndexChanged.connect(connTypeComboBox_stateChanged)

        def backCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.disable_wallpaper()
            else:
                self.rdpInstance.enable_wallpaper()
        self.backCheckBox.stateChanged.connect(backCheckBox_stateChanged)

        def fontCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_font_smoothing()
            else:
                self.rdpInstance.disable_font_smoothing()
        self.fontCheckBox.stateChanged.connect(fontCheckBox_stateChanged)

        def backCssCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_desktop_composition()
            else:
                self.rdpInstance.disable_desktop_composition()
        self.backCssCheckBox.stateChanged.connect(backCssCheckBox_stateChanged)

        def dragCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.disable_full_window_drag()
            else:
                self.rdpInstance.enable_full_window_drag()
        self.dragCheckBox.stateChanged.connect(dragCheckBox_stateChanged)

        def menuCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.disable_menu_anims()
            else:
                self.rdpInstance.enable_menu_anims()
        self.menuCheckBox.stateChanged.connect(menuCheckBox_stateChanged)

        def viewCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.disable_themes()
            else:
                self.rdpInstance.enable_themes()
        self.viewCheckBox.stateChanged.connect(viewCheckBox_stateChanged)

        def bitMapCheckBox_stateChanged(state):
            if state == QtCore.Qt.Checked:
                self.rdpInstance.enable_bitmapcachepersistenable()
            else:
                self.rdpInstance.disable_bitmapcachepersistenable()
        self.bitMapCheckBox.stateChanged.connect(bitMapCheckBox_stateChanged)

        def horizontalSlider_stateChanged(index):
            width = self.metricsMap[index][0]
            height = self.metricsMap[index][1]
            if(index == len(self.metricsMap)):
                self.deskSizeLabel.setText(u'   全屏')
            else:
                self.deskSizeLabel.setText(u'%s x %s 像素' % (width, height))
            self.rdpInstance.set_desktopwidth(width)
            self.rdpInstance.set_desktopheight(height)
        self.horizontalSlider.valueChanged.connect(horizontalSlider_stateChanged)

        def connTypeComboBox_stateChanged(index):
            #index = self.connTypeComboBox.currentIndex()
            if index == 0:
                self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
            elif index == 1:
                self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
                self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
            elif index == 2 or index == 3:
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
        self.connTypeComboBox.currentIndexChanged.connect(connTypeComboBox_stateChanged)



    def initTmpFolder(self):
        self.tmpFileFolder = os.getcwd() + '\\tmp'
        if(not os.path.isdir(self.tmpFileFolder)):
            os.mkdir(self.tmpFileFolder)

    def initEquipConent(self):
        def itemDrive_setCheckState(this, col, state):
            this._setCheckState(col, state)
            name = unicode(this.text(0))
            results = re.match("^.*\((.+:)\)$", name)
            letter = results.group(1)
            if(state == QtCore.Qt.Checked):
                self.rdpInstance.enable_drivestoredirect(letter, name)
            else:
                self.rdpInstance.disable_drivestoredirect(letter)

        self.drives = QtGui.QTreeWidgetItem(self.equipTreeWidget)
        self.drives.setText(0, u'驱动器')
        self.drives.setFlags(self.drives.flags() |
                             QtCore.Qt.ItemIsUserCheckable)
        self.drives.setCheckState(0, QtCore.Qt.Unchecked)
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
        self.drives.addChild(dynamicDrive)

        self.devices = QtGui.QTreeWidgetItem(self.equipTreeWidget)
        self.devices.setText(0, u'其他支持的即插即用(PnP)设备')
        self.devices.setFlags(self.devices.flags() |
                              QtCore.Qt.ItemIsUserCheckable)
        self.devices.setCheckState(0, QtCore.Qt.Unchecked)

        dynamicDevice = QtGui.QTreeWidgetItem(self.devices)
        dynamicDevice.setText(0, u'稍后插入的设备')
        dynamicDevice.setFlags(dynamicDevice.flags() |
                               QtCore.Qt.ItemIsUserCheckable)
        dynamicDevice.setCheckState(0, QtCore.Qt.Unchecked)
        self.equipTreeWidget.itemClicked.connect(self.equipClicked)

    def initDeskSize(self):

        self.horizontalSlider.setValue(size)
        self.deskSizeLabel.setText(u'   全屏')



    def equipClicked(self, item):
        def equipParentChangeWithChild(item):
            length = item.childCount()
            checkedSize = 0
            for i in range(0, length):
                if(item.child(i).checkState(0) == QtCore.Qt.Checked):
                    checkedSize += 1
            if(checkedSize == length):
                item.setCheckState(0, QtCore.Qt.Checked)
            elif(checkedSize == 0):
                item.setCheckState(0, QtCore.Qt.Unchecked)
            else:
                item.setCheckState(0, QtCore.Qt.PartiallyChecked)
        if hasattr(item, "isDrive"):
            name = unicode(item.text(0))
            results = re.match("^.*\((.+:)\)$", name)
            letter = results.group(1)
            if(item.checkState(0) == QtCore.Qt.Checked):
                self.rdpInstance.enable_drivestoredirect(letter, name)
            else:
                self.rdpInstance.disable_drivestoredirect(letter)
        if(isinstance(item.parent(), QtGui.QTreeWidgetItem)):
            equipParentChangeWithChild(item.parent())
        self.setQTreeWidgetItems(item, item.checkState(0))


    def connectRDP(self, ip):
        if(self.isValidIP(ip)):
            fpath = self.saveFile()
            self.runCommand('mstsc %s' % fpath)
        else:
            QtGui.QMessageBox.question(
                self, 'Message', u'请输入合法的IP地址', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)



    def runCommand(self, cmdStr):
        stdouterr = os.popen4(str(cmdStr))[1].read()
        # print '--'+stdouterr+'--'
        # if(len(stdouterr)==0):
        #     self.close()


    def openFile(self):
        fd = QtGui.QFileDialog(self).getOpenFileName()
        if os.path.isfile(fd):
            self.fromDefault = False
            self.rdpFilePath = fd
            self.updateView()

    def saveFile(self, fpath):
        if
        if len(fpath) == 0:
            self.rdpFilePath = self.tmpFileFolder + '\\rdp_' + \
                self.cmpLineEdit_2.text() + '.rdp'
        else:
            self.rdpFilePath = fpath
        self.rdpInstance.write(self.rdpFilePath)

    def saveAsFile(self):
        saveAsFilePath = str(QtGui.QFileDialog(self).getSaveFileName())
        if len(saveAsFilePath) != 0:
            self.saveFile(saveAsFilePath)

    def initView(self):
        pass


    def updateView(self):
        self.rdcCtl.initDefaultContent(self.rdpFilePath)
        add = self.rdcCtl.getValueByKeyStr('full address:s:')
        if add is not None:
            self.cmpLineEdit_2.setText(add)

        disConnBar = self.rdcCtl.getValueByKeyStr('displayconnectionbar:i:')
        if(disConnBar is not None):
            if(str(self.connBarCheckBox.checkState()) != disConnBar):
                self.connBarCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if disConnBar == '0' else QtCore.Qt.Checked)

        printChkB = self.rdcCtl.getValueByKeyStr('redirectprinters:i:')
        if(printChkB is not None):
            if(str(self.printCheckBox.checkState()) != printChkB):
                self.printCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if printChkB == '0' else QtCore.Qt.Checked)

        cliChkB = self.rdcCtl.getValueByKeyStr('redirectclipboard:i:')
        if(cliChkB is not None):
            if(str(self.cliCheckBox.checkState()) != cliChkB):
                self.cliCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if cliChkB == '0' else QtCore.Qt.Checked)

        reconnChkB = self.rdcCtl.getValueByKeyStr(
            'autoreconnection enabled:i:')
        if(reconnChkB is not None):
            if(str(self.reconnCheckBox.checkState()) != reconnChkB):
                self.reconnCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if reconnChkB == '0' else QtCore.Qt.Checked)

        authlevelComB = self.rdcCtl.getValueByKeyStr('authentication level:i:')
        if(authlevelComB is not None):
            curIndex = int(authlevelComB)
            if(self.authComboBox.currentIndex() != curIndex):
                self.authComboBox.setCurrentIndex(curIndex)

        audioCaptureComB = self.rdcCtl.getValueByKeyStr('audiocapturemode:i:')
        if(audioCaptureComB is not None):
            curIndex = int(audioCaptureComB)
            if(self.audioCaptureComBox.currentIndex() != curIndex):
                self.audioCaptureComBox.setCurrentIndex(curIndex)

        audioPlayComB = self.rdcCtl.getValueByKeyStr('audiomode:i:')
        if(audioPlayComB is not None):
            curIndex = int(audioPlayComB)
            if(self.audioPlayComBox.currentIndex() != curIndex):
                self.audioPlayComBox.setCurrentIndex(curIndex)

        keyComB = self.rdcCtl.getValueByKeyStr('keyboardhook:i:')
        if(keyComB is not None):
            curIndex = int(keyComB)
            if(self.keyComBox.currentIndex() != curIndex):
                self.keyComBox.setCurrentIndex(curIndex)

        smartCardChkB = self.rdcCtl.getValueByKeyStr('redirectsmartcards:i:')
        if(smartCardChkB is not None):
            if(str(self.smartCardCheckBox.checkState()) != smartCardChkB):
                self.smartCardCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if smartCardChkB == '0' else QtCore.Qt.Checked)

        portChkB = self.rdcCtl.getValueByKeyStr('redirectcomports:i:')
        if(portChkB is not None):
            if(str(self.portCheckBox.checkState()) != portChkB):
                self.portCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if portChkB == '0' else QtCore.Qt.Checked)

        drivesChkB = self.rdcCtl.getValueByKeyStr('drivestoredirect:s:')
        if(drivesChkB is not None):
            if(drivesChkB == '*'):
                if(self.drives.checkState(0) == QtCore.Qt.Unchecked):
                    self.drives.setCheckState(0, QtCore.Qt.Checked)
                    self.setQTreeWidgetItems(self.drives, QtCore.Qt.Checked)
        else:
            if(self.drives.checkState(0) == QtCore.Qt.Checked):
                self.drives.setCheckState(0, QtCore.Qt.Unchecked)
                self.setQTreeWidgetItems(self.drives, QtCore.Qt.Unchecked)

        devicesChkB = self.rdcCtl.getValueByKeyStr('devicestoredirect:s:')
        if(devicesChkB is not None):
            if(devicesChkB == '*'):
                if(self.devices.checkState(0) == QtCore.Qt.Unchecked):
                    self.devices.setCheckState(0, QtCore.Qt.Checked)
                    self.setQTreeWidgetItems(self.devices, QtCore.Qt.Checked)
        else:
            if(self.devices.checkState(0) == QtCore.Qt.Checked):
                self.devices.setCheckState(0, QtCore.Qt.Unchecked)
                self.setQTreeWidgetItems(self.devices, QtCore.Qt.Unchecked)

        colorComB = self.rdcCtl.getValueByKeyStr('session bpp:i:')
        if(colorComB is not None):
            curVal = int(colorComB)
            if(curVal != self.getColorComVal(self.colorComboBox.currentIndex())):
                self.colorComboBox.setCurrentIndex((curVal - 16) / 8 + 1)

        connTypeComB = self.rdcCtl.getValueByKeyStr('connection type:i:')
        if(connTypeComB is not None):
            curIndex = int(connTypeComB) - 1
            if(curIndex != self.connTypeComboBox.currentIndex()):
                self.connTypeComboBox.setCurrentIndex(curIndex)

        backChkB = self.rdcCtl.getValueByKeyStr('disable wallpaper:i:')
        if(backChkB is not None):
            if((self.backCheckBox.checkState() == QtCore.Qt.Checked and backChkB == '1')or (self.backCheckBox.checkState() == QtCore.Qt.Unchecked and backChkB == '0')):
                self.backCheckBox.setCheckState(
                    QtCore.Qt.Checked if backChkB == '0' else QtCore.Qt.Unchecked)

        fontChkB = self.rdcCtl.getValueByKeyStr('allow font smoothing:i:')
        if(fontChkB is not None):
            if((self.fontCheckBox.checkState() == QtCore.Qt.Checked and fontChkB == '0')or (self.fontCheckBox.checkState() == QtCore.Qt.Unchecked and fontChkB == '1')):
                self.fontCheckBox.setCheckState(
                    QtCore.Qt.Checked if fontChkB == '1' else QtCore.Qt.Unchecked)
        layoutChkB = self.rdcCtl.getValueByKeyStr(
            'allow desktop composition:i:')
        if(layoutChkB is not None):
            if((self.backCssCheckBox.checkState() == QtCore.Qt.Checked and layoutChkB == '0')or (self.backCssCheckBox.checkState() == QtCore.Qt.Unchecked and layoutChkB == '1')):
                self.backCssCheckBox.setCheckState(
                    QtCore.Qt.Checked if layoutChkB == '1' else QtCore.Qt.Unchecked)

        dragChkB = self.rdcCtl.getValueByKeyStr('disable full window drag:i:')
        if(dragChkB is not None):
            if((self.dragCheckBox.checkState() == QtCore.Qt.Checked and dragChkB == '1')or (self.dragCheckBox.checkState() == QtCore.Qt.Unchecked and dragChkB == '0')):
                self.dragCheckBox.setCheckState(
                    QtCore.Qt.Checked if dragChkB == '0' else QtCore.Qt.Unchecked)

        menuChkB = self.rdcCtl.getValueByKeyStr('disable menu anims:i:')
        if(menuChkB is not None):
            if((self.menuCheckBox.checkState() == QtCore.Qt.Checked and menuChkB == '1')or (self.menuCheckBox.checkState() == QtCore.Qt.Unchecked and menuChkB == '0')):
                self.menuCheckBox.setCheckState(
                    QtCore.Qt.Checked if menuChkB == '0' else QtCore.Qt.Unchecked)

        viewChkB = self.rdcCtl.getValueByKeyStr('disable themes:i:')
        if(viewChkB is not None):
            if((self.viewCheckBox.checkState() == QtCore.Qt.Checked and viewChkB == '1')or (self.viewCheckBox.checkState() == QtCore.Qt.Unchecked and viewChkB == '0')):
                self.viewCheckBox.setCheckState(
                    QtCore.Qt.Checked if viewChkB == '0' else QtCore.Qt.Unchecked)

        bitMapChkB = self.rdcCtl.getValueByKeyStr(
            'bitmapcachepersistenable:i:')
        if(bitMapChkB is not None):
            if((self.bitMapCheckBox.checkState() == QtCore.Qt.Checked and bitMapChkB == '0')or (self.bitMapCheckBox.checkState() == QtCore.Qt.Unchecked and bitMapChkB == '1')):
                self.bitMapCheckBox.setCheckState(
                    QtCore.Qt.Checked if bitMapChkB == '1' else QtCore.Qt.Unchecked)

        wid = self.rdcCtl.getValueByKeyStr(
            'desktopwidth:i:')
        hig = self.rdcCtl.getValueByKeyStr(
            'desktopheight:i:')
        if wid is not None and hig is not None:
            val = int(wid) + int(hig)
            if val in self.metricsInvertMap.keys():
                self.horizontalSlider.setValue(self.metricsInvertMap[val])

    def getColorComVal(self, index):  # 0:15 1:16 2:24 3:32
        if(index == 0):
            return 15
        else:
            return 15 + 1 + (index - 1) * 8

    def getMinIndexUp(self, val, numSet):
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

    def initMetics(self):
        width = []
        width.append(640)
        width.append(800)
        width.append(1024)
        width.append(1280)
        width.append(1366)
        width.append(1440)
        width.append(1600)
        width.append(1680)
        width.append(1920)
        height = []
        height.append(480)
        height.append(600)
        height.append(720)
        height.append(768)
        height.append(800)
        height.append(900)
        height.append(1024)
        height.append(1050)
        height.append(1080)

        geometry = QtGui.QApplication.desktop().screenGeometry()
        wi = geometry.width()
        hi = geometry.height()
        wIndex = self.getMinIndexUp(wi, width)
        hIndex = self.getMinIndexUp(hi, height)
        self.metricsMap = []
        self.metricsInvertMap = {}
        for i in range(0, wIndex + 1):
            if(i <= hIndex):
                self.metricsMap.append([width[i], height[i]])
                self.metricsInvertMap[width[i] + height[i]] = i
            else:
                self.metricsMap.append([width[i], height[hIndex]])
                self.metricsInvertMap[width[i] + height[hIndex]] = i
        if wIndex < hIndex:
            for i in(wIndex + 1, hIndex):
                self.metricsMap.append([width[wIndex], height[i]])
                self.metricsInvertMap[width[wIndex] + height[i]] = i

        if(width[wIndex] != wi or height[hIndex] != hi):
            self.metricsMap.append([wi, hi])
            self.metricsInvertMap[wi + hi] = len(self.metricsMap - 1)

    def setQTreeWidgetItems(self, item, state):
        itemSize = item.childCount()
        for i in range(0, itemSize):
            item.child(i).setCheckState(0, state)

    '''def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(
            self, 'Message', 'Are you sure to quit?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()'''

    def isValidIP(self, ipStr):
        if(len(ipStr) < 8):
            return False
        reip = re.compile(
            '^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
        return reip.match(ipStr)

    def closeEvent(self, event):
        sys.exit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
