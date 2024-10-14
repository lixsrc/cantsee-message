# -*- coding: utf-8 -*-

def encode_message(carrier_text, hidden_message):
    """
    在载体文本中隐藏信息。

    参数：
    carrier_text (str): 载体文本。
    hidden_message (str): 需要隐藏的信息。

    返回：
    str: 包含隐藏信息的文本。
    """
    # 零宽字符映射
    zero_width_chars = {
        '0': '\u200B',  # 零宽空格
        '1': '\u200C',  # 零宽非连接符
    }

    # 将隐藏信息转换为二进制字符串（使用UTF-16编码，以支持汉字）
    binary_message = ''.join(format(ord(char), '016b') for char in hidden_message)

    # 将二进制位映射为零宽字符
    encoded_zero_width = ''.join(zero_width_chars[bit] for bit in binary_message)

    # 将零宽字符嵌入到载体文本中（这里选择每个字符后面插入一个零宽字符）
    encoded_text = ''
    index = 0
    for char in carrier_text:
        encoded_text += char
        if index < len(encoded_zero_width):
            encoded_text += encoded_zero_width[index]
            index += 1

    # 如果零宽字符未插入完，继续追加
    if index < len(encoded_zero_width):
        encoded_text += encoded_zero_width[index:]

    return encoded_text


def decode_message(encoded_text):
    """
    从包含隐藏信息的文本中提取出隐藏的信息。

    参数：
    encoded_text (str): 包含隐藏信息的文本。

    返回：
    str: 提取出的隐藏信息。
    """
    # 零宽字符反向映射
    reverse_zero_width_chars = {
        '\u200B': '0',  # 零宽空格
        '\u200C': '1',  # 零宽非连接符
    }

    # 提取零宽字符
    extracted_zero_width = ''.join(char for char in encoded_text if char in reverse_zero_width_chars)

    # 将零宽字符映射回二进制字符串
    binary_message = ''.join(reverse_zero_width_chars[char] for char in extracted_zero_width)

    # 将二进制字符串转换回字符（使用UTF-16编码，每16位一个字符）
    hidden_message = ''
    for i in range(0, len(binary_message), 16):
        byte = binary_message[i:i+16]
        if len(byte) == 16:
            hidden_message += chr(int(byte, 2))

    return hidden_message


if __name__ == "__main__":
    # 明文，可以直观看到的
    carrier = "我对你的爱，加了蜜"
    # 暗文，需要隐藏的内容
    secret = """
亲爱的，最近我爸爸妈妈都不在家，他们出去旅游了。
我自己在家害怕，如果你愿意的话，能不能晚上8点带着蓝精灵来我家。
如果这条信息你无法发现，那可能是我们的缘分还没有到，稍安勿躁。
但是这个隐藏内容如果被你发现了，那我相信天意，上天安排的最大。
加油！
    """

    #处理后的明文，此时这里面已经包含暗文了
    encoded_text = encode_message(carrier, secret)
    print(f"包含隐藏信息的文本：{encoded_text}")

    # 将包含暗文的信息进行解码
    decoded_message = decode_message(encoded_text)
    print(f"\n提取出的隐藏信息：{decoded_message}")
