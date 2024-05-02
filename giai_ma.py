# Hàm giải mã Playfair
def playfair_decrypt(cipher_text, key):
    # Chuyển đổi văn bản thành chữ thường
    def toLowerCase(plain):
        return plain.lower()

    # Loại bỏ khoảng trắng trong văn bản
    def removeSpaces(plain):
        return ''.join(plain.split())

    # Tạo ma trận khóa từ key
    def generateKeyTable(key):
        # Khởi tạo ma trận khóa rỗng
        keyT = [['' for i in range(5)] for j in range(5)]
        # Khởi tạo từ điển để theo dõi việc sử dụng ký tự trong key
        dicty = {chr(i + 97): 0 for i in range(26)}

        # Đánh dấu các ký tự trong key (trừ 'j')
        for i in range(len(key)):
            if key[i] != 'j':
                dicty[key[i]] = 2
        dicty['j'] = 1

        # Điền các ký tự từ key vào ma trận khóa
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

        # Điền các ký tự còn lại vào ma trận khóa
        for k in dicty.keys():
            if dicty[k] == 0:
                keyT[i][j] = k
                j += 1
                if j == 5:
                    i += 1
                    j = 0

        return keyT

    # Tìm vị trí của các ký tự trong ma trận khóa
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

    # Hàm lấy phần dư khi chia cho 5
    def mod5(a):
        if a < 0:
            a += 5
        return a % 5

    # Hàm giải mã văn bản
    def decrypt(str, keyT):
        ps = len(str)
        i = 0
        while i < ps:
            a = search(keyT, str[i], str[i+1])
            if a[0] == a[2]:  # Cùng hàng
                str = str[:i] + keyT[a[0]][mod5(a[1]-1)] + keyT[a[0]][mod5(a[3]-1)] + str[i+2:]
            elif a[1] == a[3]:  # Cùng cột
                str = str[:i] + keyT[mod5(a[0]-1)][a[1]] + keyT[mod5(a[2]-1)][a[1]] + str[i+2:]
            else:  # Khác hàng và cột
                str = str[:i] + keyT[a[0]][a[3]] + keyT[a[2]][a[1]] + str[i+2:]
            i += 2

        return str

    # Hàm giải mã Playfair chính
    def decryptByPlayfairCipher(str, key):
        # Chuẩn hóa key và văn bản đầu vào
        key = removeSpaces(toLowerCase(key))
        str = removeSpaces(toLowerCase(str))
        # Tạo ma trận khóa
        keyT = generateKeyTable(key)
        # Giải mã văn bản
        return decrypt(str, keyT)

    # Giải mã văn bản đã mã hóa bằng mật mã Playfair
    decrypted_text = decryptByPlayfairCipher(cipher_text, key)
    return decrypted_text
    
