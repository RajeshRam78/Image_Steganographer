# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


import time

Imge_src = ""
Data_src = ""

""">>>>>>>>>>>>>>>>> BMP source data <<<<<<<<<<<<<<<<<<<<<<<<<"""
bmp_strct_data_offset_s = 10
bmp_strct_data_offset_e = 14
bmp_strct_file_size_s = 2
bmp_strct_file_size_e = 6
bmp_strct_infoheader_s = 14
bmp_strct_infoheader_e = 18
bmp_little_endian = True
bmp_size = 0
bmp_header_size = 0
bmp_data_offset = 0
bmp_data = []
bmp_path = ""
"""..........................................................."""

""">>>>>>>>>>>>>>>>> Hide data <<<<<<<<<<<<<<<<<<<<<<<<<"""
hide_data_path = ""
hide_data_data = ""
hide_data_size = 0
hide_data_format = ""
"""..........................................................."""

""">>>>>>>>>>>>>>>>> Hide data <<<<<<<<<<<<<<<<<<<<<<<<<"""
unhide_data = []
unhide_format = ""
"""..........................................................."""


class Ui_Image_Steganographer(object):
    def setupUi(self, Image_Steganographer):
        Image_Steganographer.setObjectName("Image_Steganographer")
        Image_Steganographer.resize(678, 366)
        self.centralwidget = QtWidgets.QWidget(Image_Steganographer)
        self.centralwidget.setObjectName("centralwidget")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(-250, 290, 185, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")

        self.btn_browse_img = QtWidgets.QPushButton(self.centralwidget)
        self.btn_browse_img.setGeometry(QtCore.QRect(40, 80, 75, 31))
        self.btn_browse_img.setObjectName("btn_browse_img")
        self.btn_browse_img.clicked.connect(self.getimage_path)

        self.image_src = QtWidgets.QTextBrowser(self.centralwidget)
        self.image_src.setGeometry(QtCore.QRect(140, 80, 491, 31))
        self.image_src.setObjectName("image_src")

        self.btn_browse_data = QtWidgets.QPushButton(self.centralwidget)
        self.btn_browse_data.setGeometry(QtCore.QRect(40, 150, 75, 31))
        self.btn_browse_data.setObjectName("btn_browse_data")
        self.btn_browse_data.clicked.connect(self.getdata_path)

        self.data_src = QtWidgets.QTextBrowser(self.centralwidget)
        self.data_src.setGeometry(QtCore.QRect(140, 150, 491, 31))
        self.data_src.setObjectName("data_src")


        self.btn_hide_data = QtWidgets.QPushButton(self.centralwidget)
        self.btn_hide_data.setGeometry(QtCore.QRect(40, 220, 71, 31))
        self.btn_hide_data.setObjectName("btn_hide_data")
        self.btn_hide_data.clicked.connect(self.hide_data)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(150, 260, 271, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.btn_unhide_data = QtWidgets.QPushButton(self.centralwidget)
        self.btn_unhide_data.setGeometry(QtCore.QRect(40, 280, 71, 31))
        self.btn_unhide_data.setObjectName("btn_unhide_data")
        self.btn_unhide_data.clicked.connect(self.unhide_data)
		
        Image_Steganographer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Image_Steganographer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 678, 21))
        self.menubar.setObjectName("menubar")
        Image_Steganographer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Image_Steganographer)
        self.statusbar.setObjectName("statusbar")
        Image_Steganographer.setStatusBar(self.statusbar)

        self.retranslateUi(Image_Steganographer)
        QtCore.QMetaObject.connectSlotsByName(Image_Steganographer)

    def retranslateUi(self, Image_Steganographer):
        _translate = QtCore.QCoreApplication.translate
        Image_Steganographer.setWindowTitle(_translate("Image_Steganographer", "MainWindow"))
        self.commandLinkButton.setText(_translate("Image_Steganographer", "CommandLinkButton"))
        self.btn_browse_img.setText(_translate("Image_Steganographer", "Browse BMI"))
        self.btn_browse_data.setText(_translate("Image_Steganographer", "Browse data"))
        self.btn_hide_data.setText(_translate("Image_Steganographer", "Hide data"))
        self.btn_unhide_data.setText(_translate("Image_Steganographer", "unhide data"))

    def reverse_concatinate(self, data):
        val = 0
        data = data[::-1]
        for i in data:
            val = (val << 8) | i

        return val


    def getimage_path(self):
        global bmp_path
        bmp_path = QtWidgets.QFileDialog.getOpenFileName(filter = "*.bmp")
        bmp_path = str(bmp_path)
        bmp_path = bmp_path[2 : (bmp_path.index(".bmp") + 4)]
        self.image_src.setText(bmp_path)

    def getdata_path(self):
        global hide_data_path, hide_data_format
        hide_data_path = QtWidgets.QFileDialog.getOpenFileName()
        hide_data_path = str(hide_data_path)
        hide_data_path = hide_data_path[2: (hide_data_path.index("',"))]
        hide_data_format = hide_data_path[hide_data_path.index('.')+1:]
        print(hide_data_format)
        self.data_src.setText(hide_data_path)

    def validate_bmp(self, bmp_path):
        global bmp_data, bmp_size,bmp_data_offset, bmp_header_size
        fptr = open(bmp_path, 'rb')
        bmp_data = fptr.read()
        bmp_size = len(bmp_data)
        bmp_sign = bmp_data[:2].decode('utf-8')
        fptr.close()
        bmp_data_offset = self.reverse_concatinate(bmp_data[bmp_strct_data_offset_s: bmp_strct_data_offset_e])
        bmp_header_size = 14 + self.reverse_concatinate(bmp_data[bmp_strct_infoheader_s:bmp_strct_infoheader_e])
        if(str(bmp_sign) == "BM" and (bmp_size == self.reverse_concatinate(bmp_data[bmp_strct_file_size_s: bmp_strct_file_size_e]))
        and (bmp_data_offset == bmp_header_size)):
            print("BMP valid")
            return True
        else:
            return False

    def validate_data_fit(self, hide_data_path):
        global hide_data_size, hide_data_data
        fptr = open(hide_data_path, 'rb')
        hide_data_data = fptr.read()
        hide_data_size = len(hide_data_data)
        size_possible = (bmp_size - bmp_header_size)

        if ((hide_data_size + 11) * 8) >= size_possible:
            return False
        else:
            return True


    def LSB_encode(self, dest, source):
        global  bmp_data_offset, hide_data_format
        offset_iter = bmp_data_offset
        dest = list(dest)
        source = list(source)
        hide_data_len_lst = []
        for i in range(0,6):
            hide_data_len_lst.append(((hide_data_size >> (8*i)) & 0xFF))

        prepend_data = [0x78]
        for i in hide_data_len_lst:
            prepend_data.append(i)

        prepend_data.append(len(hide_data_format))
        for i in hide_data_format:
            prepend_data.append(ord(i))
        for i in range(0, len(prepend_data)):
            source.insert(i, prepend_data[i])
        index = 0
        for byte in source:
            for i in range(0,8):
                if byte & 0x01:
                    dest[offset_iter + i] = (dest[offset_iter + i] | 0x01)
                else:
                    dest[offset_iter + i] = (dest[offset_iter + i] & 0xFE)
                byte >>= 1

            offset_iter += 8
            index += 1
            progress_prcnt = (index / len(source)) * 100
            self.progressBar.setValue(int(progress_prcnt))
            QtGui.QGuiApplication.processEvents()

        else:
            dest = bytearray(dest)
            fptr = open("encoded.bmp", 'wb')
            fptr.write(dest)
            fptr.close()

    def LSB_decode_byte(self, data):
        ret_val = 0
        for i in range(0, 8):
            if data[i] & 0x01:
                ret_val |= 0x80
            else:
                ret_val &= 0x7F
            if i != 7:
                ret_val >>= 1
        return ret_val


    def decode_bytes(self, data):
        """ sign*8 + data_size_bytes*8"""
        initial_decode_len = 56
        bytes = []

        for i in range(0, (initial_decode_len), 8):
            bytes.append(self.LSB_decode_byte(data[i:]))
        else:
            if bytes[0] == 0x78:
                initial_decode_len = (self.reverse_concatinate(bytes[1:7]) + 10) * 8
                bytes = []
               # data = data[11:]
                for i in range(0, (initial_decode_len), 8):
                    bytes.append(self.LSB_decode_byte(data[i:]))

                    progress_prcnt = (i/initial_decode_len)*100
                    self.progressBar.setValue(int(progress_prcnt))
                    QtGui.QGuiApplication.processEvents()
                else:
                    progress_prcnt = 100
                    self.progressBar.setValue(int(progress_prcnt))
                    QtGui.QGuiApplication.processEvents()
                    return bytes, True
            else:
                return 0, False



    def hide_data(self):
        global bmp_path, hide_data_path
        if bmp_path == "" or hide_data_path == "":
            dlg = QtWidgets.QMessageBox()
            dlg.setWindowTitle("Info!!")
            dlg.setIcon(dlg.Information)
            dlg.setText("please select the source files")
            dlg.exec_()
        else:
            """ Validate image """
            if self.validate_bmp(bmp_path):
                if self.validate_data_fit(hide_data_path):
                    self.LSB_encode(bmp_data, hide_data_data)
                else:
                    dlg = QtWidgets.QMessageBox()
                    dlg.setWindowTitle("Info!!")
                    dlg.setIcon(dlg.Information)
                    dlg.setText("More data to hide, please select lower file size")
                    dlg.exec_()

            else:
                dlg = QtWidgets.QMessageBox()
                dlg.setWindowTitle("Info!!")
                dlg.setIcon(dlg.Information)
                dlg.setText("Invalid/corrupted BMP image")
                dlg.exec_()

    def validate_encode(self, bmp_path):
        global unhide_data, unhide_format
        fptr = open(bmp_path, 'rb')
        bmp_data = fptr.read()
        lst_data = list(bmp_data)
        unhide_data, status = self.decode_bytes(lst_data[bmp_data_offset:])
        if status:
            unhide_format = "".join(chr(x) for x in unhide_data[8: (8 + unhide_data[7])])
            return True
        else:
            return False




    def unhide_data(self):
        global bmp_path, unhide_data, unhide_format
        if bmp_path == "":
            dlg = QtWidgets.QMessageBox()
            dlg.setWindowTitle("Info!!")
            dlg.setIcon(dlg.Information)
            dlg.setText("please select the source files")
            dlg.exec_()
        else:
            if self.validate_bmp(bmp_path) and self.validate_encode(bmp_path):
                fptr = open("decoded." + unhide_format , 'wb')
                unhide_data = bytearray(unhide_data[(8 + unhide_data[7]):])
                fptr.write(unhide_data)
                fptr.close()
            else:
                dlg = QtWidgets.QMessageBox()
                dlg.setWindowTitle("Info!!")
                dlg.setIcon(dlg.Information)
                dlg.setText("Not an encoded image")
                dlg.exec_()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Image_Steganographer = QtWidgets.QMainWindow()
    ui = Ui_Image_Steganographer()
    ui.setupUi(Image_Steganographer)
    Image_Steganographer.show()
    sys.exit(app.exec_())



for i in range(0, 10):
    if i & 0x01:
        print(i,"-Odd")
    else:
        print(i,"-Even")