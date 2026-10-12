from enum import Enum
from string import ascii_lowercase


class Method(Enum):
    ROW = 1  # 同行
    COLUMN = 2  # 同列
    CROSS = 3  # 对角线


class playfair:
    def __init__(self, key: str):
        """
        初始化 Playfair 密码的实例

        key(str): 初始化用的密钥
        """
        self.key = key
        self.matrix = self.build_matrix(key)

    def build_matrix(self, key: str) -> list[list[str]]:
        """
        构建密码阵

        key(str): 用于构建密码阵的密钥
        return(list[list[str]]): 返回构建好的密码阵
        """
        matrix: list[list[str]] = []  # 初始化空矩阵
        line: list[str] = []  # 行
        existed: set[str] = set()  # 存在的字符集，因为 playfair 里面没有重复的字符
        for c in key:
            if c not in existed:
                line.append(c if c not in ["i", "j"] else "i")  # i 和 j 是同一个东西
                existed.add(c if c not in ["i", "j"] else "i")
            if len(line) == 5:
                matrix.append(line)
                line = []
        for c in ascii_lowercase:  # 加完了密钥的，按照字母表顺序加其他的
            c = c if c not in ["i", "j"] else "i"
            if c not in existed:
                line.append(c)
                existed.add(c)
                if len(line) == 5:  # 满 5 换行
                    matrix.append(line)
                    line = []
        if line:  # 如果最后一行不满 5 个，也要加上去
            matrix.append(line)
        return matrix

    def pre_process(self, plain: str) -> list[str]:
        plain = plain.lower().replace("j", "i")
        chars = [c for c in plain if c.isalpha()]
        result: list[str] = []
        i = 0
        while i < len(chars):
            a = chars[i]
            if i + 1 < len(chars):
                b = chars[i + 1]
                if a == b:  # 前后相同，补 x
                    result.append(a + "x")
                    i += 1
                else:
                    result.append(a + b)
                    i += 2
            else:
                result.append(a + "x")
                i += 1
        return result

    def getpos(self, c: str) -> tuple[int, int]:
        """
        判断字符在密码阵中的位置，返回行列坐标

        c(str): 需要判断位置的字符
        return(tuple[int, int]): 返回行列坐标
        """
        return next(
            (i, j)
            for i, row in enumerate(self.matrix)
            for j, char in enumerate(row)
            if char == c
        )

    def determine_method(self, a: str, b: str) -> Method:
        """
        判断两个字符在密码阵中的关系，返回对应的方法

        a(str): 第一个字符
        b(str): 第二个字符
        return(Method): 返回对应的方法
        """
        pos_a = self.getpos(a)
        pos_b = self.getpos(b)
        if pos_a[0] == pos_b[0]:  # 同行
            return Method.ROW
        elif pos_a[1] == pos_b[1]:  # 同列
            return Method.COLUMN
        else:  # 对角线
            return Method.CROSS

    def encrypt(self, plain: str) -> str:
        """
        加密明文，返回密文

        plain(str): 需要加密的明文
        return(str): 返回加密后的密文
        """
        grouped_plain = self.pre_process(plain)
        new_plain = "".join(grouped_plain)
        result = ""
        for i in range(0, len(new_plain), 2):
            a = new_plain[i]
            b = new_plain[i + 1]
            method = self.determine_method(a, b)  # 确定加密的方法
            pos_a = self.getpos(a)
            pos_b = self.getpos(b)
            if method == Method.ROW:  # 同行，循环右移一个单位
                result += self.matrix[pos_a[0]][(pos_a[1] + 1) % 5]
                result += self.matrix[pos_b[0]][(pos_b[1] + 1) % 5]
            elif method == Method.COLUMN:  # 同列，循环下移一个单位
                result += self.matrix[(pos_a[0] + 1) % 5][pos_a[1]]
                result += self.matrix[(pos_b[0] + 1) % 5][pos_b[1]]
            else:  # 对角线，交换列坐标
                result += self.matrix[pos_a[0]][pos_b[1]]
                result += self.matrix[pos_b[0]][pos_a[1]]
        return result

    def decrypt(self, ciphertext: str) -> str:
        """
        解密经过同一个 Playfair 表加密的密文

        ciphertext(str): 需要解密的密文
        return(str): 返回解密后的明文
        """
        ciphertext = ciphertext.lower().replace("j", "i")
        result = ""
        for i in range(0, len(ciphertext), 2):
            a = ciphertext[i]
            b = ciphertext[i + 1]
            method = self.determine_method(a, b)  # 确定解密的方法
            pos_a = self.getpos(a)
            pos_b = self.getpos(b)
            if method == Method.ROW:  # 同行，循环左移一个单位
                result += self.matrix[pos_a[0]][(pos_a[1] - 1) % 5]
                result += self.matrix[pos_b[0]][(pos_b[1] - 1) % 5]
            elif method == Method.COLUMN:  # 同列，循环上移一个单位
                result += self.matrix[(pos_a[0] - 1) % 5][pos_a[1]]
                result += self.matrix[(pos_b[0] - 1) % 5][pos_b[1]]
            else:  # 对角线，交换列坐标
                result += self.matrix[pos_a[0]][pos_b[1]]
                result += self.matrix[pos_b[0]][pos_a[1]]
        return result
    
    def print_matrix(self):
        """
        打印密码阵
        """
        for row in self.matrix:
            print(" ".join(row))


def validate_key(key: str) -> bool:
    """
    验证密钥是否合法，反正全字母不含其他的字符、数字或非 ASCII 字符那都是合法

    key(str): 需要验证的密钥
    return(bool): 返回是否合法
    """
    return key.isalpha() and key.isascii()


def print_menu():
    """
    依旧显示菜单用的
    """
    menu = """=============== Playfair Cipher ===============
[1] 加密
[2] 解密
[3] 打印密码阵
[4] 重设密钥
[0] 退出
============================================"""
    print(menu)


def calculate_frequency(text: str) -> dict[str, int]:
    """
    计算文本中每个字母的频率，返回频率字典

    text(str): 需要计算频率的文本
    return(dict[str, int]): 返回频率字典
    """
    frequency: dict[str, int] = {}
    for c in text:
        if c.isalpha():
            frequency[c] = frequency.get(c, 0) + 1
    return frequency


if __name__ == "__main__":
    print("学号: 3124004333")
    while True:
        key = input("[+] 请输入 playfair 的密钥 (gdutcollegestudent): ")
        if not key:
            key = "gdutcollegestudent"
        if validate_key(key):
            break
        else:
            print("[!] 密钥不合法，请重新输入。")
    cipher = playfair(key)
    while True:
        print_menu()
        match input("[*] 请选择操作: "):
            case "1":
                plain = input("[*] 请输入明文: ")
                ciphertext = cipher.encrypt(plain)
                print(f"[+] 加密后的密文为: {ciphertext}")
                print(f"[+] 明文频率: {calculate_frequency(plain)}")
                print(f"[+] 密文频率: {calculate_frequency(ciphertext)}")
            case "2":
                ciphertext = input("[*] 请输入密文: ")
                plain = cipher.decrypt(ciphertext)
                print(f"[+] 解密后的明文为: {plain}")
                print(f"[+] 明文频率: {calculate_frequency(plain)}")
                print(f"[+] 密文频率: {calculate_frequency(ciphertext)}")
            case "3":
                print("[+] 当前的密码阵为:")
                cipher.print_matrix()
            case "4":
                while True:
                    key = input("[+] 请输入 playfair 的密钥 (gdutcollegestudent): ")
                    if validate_key(key):
                        break
                    else:
                        print("[!] 密钥不合法，请重新输入。")
                cipher = playfair(key)
            case "0":
                print("[*] 退出程序。")
                break
            case _:
                print("[!] 无效的选择，请重新输入。")
