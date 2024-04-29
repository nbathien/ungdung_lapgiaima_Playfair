from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox

def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Error")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setText(message)
    msg_box.exec()

# Hàm mã hóa, lập mã Playfair
def playfair_encrypt(plain_text, key):
    def toLowerCase(text):
        return text.lower()
        
    def removeSpaces(text):
        newText = ""
        for i in text:
            if i == " ":
                continue
            else:
                newText = newText + i
        return newText

    def Diagraph(text):
        Diagraph = []
        group = 0
        for i in range(2, len(text), 2):
            Diagraph.append(text[group:i])
            group = i
        Diagraph.append(text[group:])
        return Diagraph

    def FillerLetter(text):
        k = len(text)
        if k % 2 == 0:
            for i in range(0, k, 2):
                if text[i] == text[i+1]:
                    new_word = text[0:i+1] + str('x') + text[i+1:]
                    new_word = FillerLetter(new_word)
                    break
                else:
                    new_word = text
        else:
            for i in range(0, k-1, 2):
                if text[i] == text[i+1]:
                    new_word = text[0:i+1] + str('x') + text[i+1:]
                    new_word = FillerLetter(new_word)
                    break
                else:
                    new_word = text
        return new_word

    list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def generateKeyTable(word, list1):
        key_letters = []
        for i in word:
            if i not in key_letters:
                key_letters.append(i)

        compElements = []
        for i in key_letters:
            if i not in compElements:
                compElements.append(i)
        for i in list1:
            if i not in compElements:
                compElements.append(i)

        matrix = []
        while compElements != []:
            matrix.append(compElements[:5])
            compElements = compElements[5:]

        return matrix

    def search(mat, element):
        for i in range(5):
            for j in range(5):
                if(mat[i][j] == element):
                    return i, j

    def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
        char1 = ''
        if e1c == 4:
            char1 = matr[e1r][0]
        else:
            char1 = matr[e1r][e1c+1]

        char2 = ''
        if e2c == 4:
            char2 = matr[e2r][0]
        else:
            char2 = matr[e2r][e2c+1]

        return char1, char2

    def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
        char1 = ''
        if e1r == 4:
            char1 = matr[0][e1c]
        else:
            char1 = matr[e1r+1][e1c]

        char2 = ''
        if e2r == 4:
            char2 = matr[0][e2c]
        else:
            char2 = matr[e2r+1][e2c]

        return char1, char2

    def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
        char1 = ''
        char1 = matr[e1r][e2c]

        char2 = ''
        char2 = matr[e2r][e1c]

        return char1, char2

    def encryptByPlayfairCipher(Matrix, plainList):
        CipherText = []
        for i in range(0, len(plainList)):
            c1 = 0
            c2 = 0
            ele1_x, ele1_y = search(Matrix, plainList[i][0])
            ele2_x, ele2_y = search(Matrix, plainList[i][1])

            if ele1_x == ele2_x:
                c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            elif ele1_y == ele2_y:
                c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            else:
                c1, c2 = encrypt_RectangleRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

            cipher = c1 + c2
            CipherText.append(cipher)
        return "".join(CipherText)

    text_Plain = removeSpaces(toLowerCase(plain_text))
    PlainTextList = Diagraph(FillerLetter(text_Plain))
    if len(PlainTextList[-1]) != 2:
        PlainTextList[-1] = PlainTextList[-1]+'z'

    key = key.lower()  # Convert key to lowercase
    Matrix = generateKeyTable(key, list1)

    CipherList = encryptByPlayfairCipher(Matrix, PlainTextList)

    CipherText = ""
    for i in CipherList:
        CipherText += i
    return CipherText

# Hàm giải mã Playfair
def playfair_decrypt(cipher_text, key):
    def toLowerCase(plain):
        return plain.lower()

    def removeSpaces(plain):
        return ''.join(plain.split())

    def generateKeyTable(key):
        keyT = [['' for i in range(5)] for j in range(5)]
        dicty = {chr(i + 97): 0 for i in range(26)}

        for i in range(len(key)):
            if key[i] != 'j':
                dicty[key[i]] = 2
        dicty['j'] = 1

        i, j, k = 0, 0, 0
        while k < len(key):
            if dicty[key[k]] == 2:
                dicty[key[k]] -= 1
                keyT[i][j] = key[k]
                j += 1
                if j == 5:
                    i += 1
                    j = 0
            k += 1

        for k in dicty.keys():
            if dicty[k] == 0:
                keyT[i][j] = k
                j += 1
                if j == 5:
                    i += 1
                    j = 0

        return keyT

    def search(keyT, a, b):
        arr = [0, 0, 0, 0]

        if a == 'j':
            a = 'i'
        elif b == 'j':
            b = 'i'

        for i in range(5):
            for j in range(5):
                if keyT[i][j] == a:
                    arr[0], arr[1] = i, j
                elif keyT[i][j] == b:
                    arr[2], arr[3] = i, j

        return arr

    def mod5(a):
        if a < 0:
            a += 5
        return a % 5

    def decrypt(str, keyT):
        ps = len(str)
        i = 0
        while i < ps:
            a = search(keyT, str[i], str[i+1])
            if a[0] == a[2]:
                str = str[:i] + keyT[a[0]][mod5(a[1]-1)] + keyT[a[0]][mod5(a[3]-1)] + str[i+2:]
            elif a[1] == a[3]:
                str = str[:i] + keyT[mod5(a[0]-1)][a[1]] + keyT[mod5(a[2]-1)][a[1]] + str[i+2:]
            else:
                str = str[:i] + keyT[a[0]][a[3]] + keyT[a[2]][a[1]] + str[i+2:]
            i += 2

        return str

    def decryptByPlayfairCipher(str, key):
        ks = len(key)
        key = removeSpaces(toLowerCase(key))
        str = removeSpaces(toLowerCase(str))
        keyT = generateKeyTable(key)
        return decrypt(str, keyT)

    decrypted_text = decryptByPlayfairCipher(cipher_text, key)
    return decrypted_text

# Tạo ma trận Playfair từ khóa
def create_playfair_matrix(key):
    key = key.lower()
    alphabet = "abcdefghiklmnopqrstuvwxyz"  # Loại bỏ 'j'

    # Xây dựng ma trận 5x5 từ khóa
    matrix = []
    for char in key + alphabet:
        if char not in matrix and char != 'j':
            matrix.append(char)
    matrix = [matrix[i:i+5] for i in range(0, 25, 5)]

    # Chuyển đổi ma trận thành chữ in hoa
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j].upper()

    return matrix

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(878, 627)
        MainWindow.setStyleSheet("border-color: rgb(255, 255, 127);")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(260, 70, 361, 221))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 36, 55, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.ban_tin = QtWidgets.QLineEdit(parent=self.groupBox)
        self.ban_tin.setGeometry(QtCore.QRect(110, 30, 231, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.ban_tin.setFont(font)
        self.ban_tin.setStyleSheet("")
        self.ban_tin.setText("")
        self.ban_tin.setObjectName("ban_tin")
        self.key = QtWidgets.QLineEdit(parent=self.groupBox)
        self.key.setGeometry(QtCore.QRect(110, 100, 231, 31))
        self.key.setObjectName("key")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 0, 521, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 310, 821, 271))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.ma_tran = QtWidgets.QTableWidget(parent=self.groupBox_2)
        self.ma_tran.setGeometry(QtCore.QRect(10, 50, 521, 191))
        self.ma_tran.setObjectName("ma_tran")
        self.ma_tran.setColumnCount(5)
        self.ma_tran.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ma_tran.setHorizontalHeaderItem(4, item)
        self.ket_qua = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.ket_qua.setGeometry(QtCore.QRect(550, 50, 261, 31))
        self.ket_qua.setObjectName("ket_qua")
        self.lap_ma = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.lap_ma.setGeometry(QtCore.QRect(570, 110, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lap_ma.setFont(font)
        self.lap_ma.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.lap_ma.setObjectName("lap_ma")
        self.giai_ma = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.giai_ma.setGeometry(QtCore.QRect(690, 110, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.giai_ma.setFont(font)
        self.giai_ma.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.giai_ma.setObjectName("giai_ma")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Kết nối sự kiện nhấn nút "Lập mã" và "Giải mã" với hàm xử lý tương ứng
        self.lap_ma.clicked.connect(self.lap_ma_clicked)
        self.giai_ma.clicked.connect(self.giai_ma_clicked)
        
        self.key.textChanged.connect(self.update_matrix)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Bản tin"))
        self.label_3.setText(_translate("MainWindow", "Khóa"))
        self.label.setText(_translate("MainWindow", "LẬP MÃ VÀ GIẢI MÃ PLAYFAIR"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Ma trận"))
        item = self.ma_tran.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.ma_tran.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.ma_tran.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.ma_tran.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.ma_tran.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        item = self.ma_tran.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.ma_tran.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.ma_tran.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.ma_tran.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.ma_tran.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        self.lap_ma.setText(_translate("MainWindow", "Lập mã"))
        self.giai_ma.setText(_translate("MainWindow", "Giải mã "))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))

    def update_matrix(self):
        key = self.key.text()
        matrix = create_playfair_matrix(key)
    # Thiết lập dữ liệu cho QTableWidget
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.ma_tran.setItem(i, j, QtWidgets.QTableWidgetItem(matrix[i][j]))
    
    # Hàm xử lý khi nhấn nút "Lập mã"
    def lap_ma_clicked(self):
        plaintext = self.ban_tin.text()
        key = self.key.text()
        if not plaintext or not key:
            show_error_message("Vui lòng nhập cả bản rõ và khóa.")
            return
        try:
            result = playfair_encrypt(plaintext, key)
            result = result.upper()
            self.ket_qua.setText(result)
        except Exception as e:
            show_error_message("Có lỗi xảy ra: " + str(e))

    # Hàm xử lý khi nhấn nút "Giải mã"
    def giai_ma_clicked(self):
        ciphertext = self.ban_tin.text()
        key = self.key.text()
        if not ciphertext or not key:
            show_error_message("Vui lòng nhập cả bản mã và khóa.")
            return
        try:
            result = playfair_decrypt(ciphertext, key)
            result = result.upper()
            self.ket_qua.setText(result)
        except Exception as e:
            show_error_message("Có lỗi xảy ra: " + str(e))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
