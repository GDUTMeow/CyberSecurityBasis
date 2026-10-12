import os
from string import ascii_lowercase, ascii_uppercase


class caesar:
    def __init__(self, shift: int = 13):
        """
        初始化一个凯撒密码的实例，并指定对应的偏移量
        
        shift(int): 偏移量，默认按照 ROT13 走
        """
        self.shift = shift
        self.lowercase = ascii_lowercase
        self.uppercase = ascii_uppercase
        
    def encrypt(self, text: str, shift: int | None = None) -> str:
        """
        进行凯撒密码加密，并返回对应的加密后的结果
        
        text(str): 需要进行加密的内容
        shift(int): 偏移量，不指定就走实例初始化的时候指定的
        """
        if shift is None:
            shift = self.shift
        result: list[str] = []
        for c in text:
            if c in self.lowercase:
                # 小写字母，进行循环偏移
                result.append(self.lowercase[(self.lowercase.index(c) + shift) % 26])
            elif c in self.uppercase:
                # 大写字母，同上
                result.append(self.uppercase[(self.uppercase.index(c) + shift) % 26])
            else:
                # 非目标范围内字符
                result.append(c)
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, shift: int | None = None) -> str:
        """
        解密函数，返回解密后的结果
        
        ciphertext(str): 需要进行解密的密文
        shift(int): 偏移量
        """
        if shift is None:
            shift = self.shift
        result: list[str] = []
        for c in ciphertext:
            if c in self.lowercase:
                # 小写字母，进行循环偏移
                result.append(self.lowercase[(self.lowercase.index(c) - shift) % 26])
            elif c in self.uppercase:
                # 大写字母，同上
                result.append(self.uppercase[(self.uppercase.index(c) - shift) % 26])
            else:
                # 非目标范围内字符
                result.append(c)
        return ''.join(result)
    
def brute_force(ciphertext: str) -> list[tuple[int, str]]:
    """
    暴力破解函数，会跑一遍所有的偏移量，然后返回对应偏移量的结果
    
    ciphertext(str): 需要进行破解的密文
    """
    result: list[tuple[int, str]] = []
    for shift in range(26):
        c = caesar(shift)
        result.append((shift, c.decrypt(ciphertext)))
    return result

def print_menu(shift: int):
    """
    显示菜单
    
    shift(int): 当前的偏移量
    """
    menu = f"""=============== Caesar Cipher ===============
当前偏移量为: {shift}

[1] 加密
[2] 解密
[3] 爆破
[4] 调整偏移量
[0] 退出
============================================"""
    print(menu)

def set_shift() -> int:
    """
    用于设置偏移量，因为校验多处要用，所以直接写成了函数
    
    return(int): 返回合法的偏移量
    """
    while True:
        try:
            shift = input("[+] 为了初始化一个凯撒密码实例，请输入偏移量 (13): ")
            if not shift:
                shift = 13
            shift = int(shift)
        except ValueError:
            print("[!] 输入的偏移量不合法，请重新输入")
            continue
        if shift < 0:
            print("[!] 输入的偏移量不合法，请重新输入")
            continue
        break
    return shift

if __name__ == "__main__":
    print("学号: 3124004333")
    cipher = caesar(shift=set_shift())
    while True:
        print_menu(cipher.shift)
        choice = input("[*] 请选择操作: ")
        match choice:
            case "1":
                text = input("[*] 请输入需要加密的内容: ")
                print(f"[+] 加密后的结果为: {cipher.encrypt(text)}")
            case "2":
                text = input("[*] 请输入需要解密的内容: ")
                print(f"[+] 解密后的结果为: {cipher.decrypt(text)}")
            case "3":
                text = input("[*] 请输入需要破解的密文: ")
                result = brute_force(text)
                print("[+] 爆破结果如下:")
                for shift, decrypted in result:
                    print(f"> 偏移量: {shift}, 解密结果: {decrypted}")
            case "4":
                cipher = caesar(shift=set_shift())
            case "0":
                print("[-] 退出程序")
                os._exit(0)
            case _:
                print("[!] 输入的选项不合法，请重新输入")
