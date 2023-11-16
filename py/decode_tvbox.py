import urllib.request
import datetime
import re
import base64
import json
import os


# Insert characters into the specified column on the specified line in the file
def insert2lc(filename: str, line: int, column: int, context: str):
    """
    Insert characters into the specified column on the specified line in the file
    """
    with open(filename, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    lines[line] = lines[line][:column] + context + lines[line][column:]

    with open(filename, 'w', encoding="utf-8") as file:
        file.writelines(lines)


# 检查json文件格式是否合法。本次错误缺少逗号分隔符，处理好了
def json_check(decode_file: str):
    loop = 1
    while loop:
        try:
            json.load(open(decode_file, "r", encoding="utf-8"))
        except Exception as e:
            # print(e.msg)  # 错误内容
            # print(e.doc)  # 文件所有内容
            # print(e.pos)  # 出错是第几个字符
            # print(e.lineno)  # 出错行号
            # print(e.colno)  # 出错列号
            print(e)  # 打印出错内容，提示用

            # 当前只能处理逗号分隔符的错误
            yes = re.match("Expecting '(.)' delimiter", e.msg)
            if yes:
                # print(yes.groups()[0])
                delimiter = yes.groups()[0]
            else:
                print("unknown error:", e)
                exit(1)

            insert2lc(decode_file, e.lineno - 1, e.colno - 1, delimiter)
        else:
            # 没错误了，结束检查
            loop = 0


# config here
# 是否测试模式，测试模式就是本地测试，不从网络下文件，而是使用本地文件，
test = False
# test = True
if test:
    img_filename = 'o.bmp'
else:
    img_filename = str(datetime.date.today()) + '_o.bmp'

decode_filename = "decode_tvbox.txt"
# url = 'https://gitee.com/haitang123/abc/raw/master/o.bmp'
url = 'https://raw.gitmirror.com/HiTang123/abc/main/o.bmp'

def main():
    # 1. 从url下载文件，存为img_filename
    if not test:
        urllib.request.urlretrieve(url, img_filename)

    # 2. 获取文件内容，提取**后面的base64加密内容，将其解密，存为txt
    # 2.1 获取文件内容，然后删除临时图片文件
    with open(img_filename, "rb") as f:
        con = f.read().decode("ascii", "ignore").rsplit("*")[-1]
    if not test:
        os.remove(img_filename)
    else:
        with open(r"encode_context.txt", "w") as tttt:
            tttt.write(con)
        print("encode_context write finish")

    with open(decode_filename, "wb") as f_de:
        # 2.3 将其解密，存为txt
        f_de.write(base64.b64decode(con))
    # 3. 检查json文件格式是否合法。本次错误缺少逗号分隔符，处理好了
    json_check(decode_filename)
    print("all OK!")
    """
    # 2.2 提取**后面的base64加密内容
    ret = re.findall(r"\*\*.*", str(con))
    if ret:
        # print(ret)
        # print(type(ret))
        # print(ret.group().decode())
        with open(decode_filename, "wb") as f_de:
            # 2.3 将其解密，存为txt
            f_de.write(base64.b64decode(ret[-1][2:]))

        # 3. 检查json文件格式是否合法。本次错误缺少逗号分隔符，处理好了
        json_check(decode_filename)
        print("all OK!")
    else:
        print("not found **, exit!")
        exit(-1)
    """


if __name__ == '__main__':
    main()
    # json_check(decode_filename)
