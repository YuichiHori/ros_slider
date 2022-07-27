"""Slider(Oriental Motor) control module"""

import socket
import time

class SliderDriver():

    def __init__(self, IP = '192.168.100.101', port = 10001):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((IP, port))

    def zero_return(self):

        """高速原点復帰運転"""

        start_command = create_query('0106007D0010')
        self.s.sendall(start_command)
        time.sleep(1)
        end_command = create_query('0106007D0000')
        self.s.sendall(end_command)
        return

    def direct_operation(self, location=11000, speed=80000, acc=1000000):
        """
        ダイレクトデータ運転

        Parameters
        ----------
        location : int
        絶対位置(step)

        speed : int
        速度

        acc : int
        始点・終点加速度
        """
        speed_hex= format(speed, '08x')
        location_hex = format(location, '08x')
        acc_hex = format(acc, '08x')
        command = create_query('01 10 0058 0010 20 00000000 00000001' + location_hex + speed_hex + acc_hex + acc_hex+ '000003E8 00000001')
        self.s.sendall(command)
        return

    def close(self):
        self.s.close()

def crc16(command):
    """
    crc-16のエラーチェック生成

    Parameters
    ----------
    command : bytes
    コマンド

    Returns
    -------
    crc : bytes
    エラーチェック
    """
    # 最初のCRCレジスタ値をFFFFhに設定
    crc_register = 0xFFFF
    for data_byte in command:
        crc_register ^= data_byte
        for _ in range(8):
            overflow = crc_register & 1 == 1
            crc_register >>= 1
            if overflow:
                crc_register ^= 0xA001
    # 計算結果をbytes型へ変換
    crc = crc_register.to_bytes(2, 'little')
    return crc

def create_query(hex_command):
    """
    エラーチェックを含めたコマンドの生成

    Parameters
    ----------
    hex_command : char
    16進数のコマンドの文字列

    Returns
    -------
    query : bytes
    エラーチェックを含んだコマンド
    """
    bytes_command = bytes.fromhex(hex_command)
    error_check = crc16(bytes_command)
    query = bytes_command + error_check
    print(query)
    return query
