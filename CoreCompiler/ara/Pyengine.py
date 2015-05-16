# -*- coding : utf-8 -*-
from datetime import datetime
import re
__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    result.append("# -*- coding : utf-8 -*-\n")
    result.append("# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의하여 작성되어진 Python 파일입니다.\n")
    result.append("# Pyengine build.\n")
    result.append("# 만들어진 시각 : " + datetime.today().strftime("%Y. %m. %d. %H:%M:%S\n\n"))
    for i in range(0, len(araCode)):
        data = araCode[i]
        string = ""

        # 문자열에 대한 처리
        if data.find("\"") + data.rfind("\"") != -2:
            string = data[data.find("\""):data.rfind("\"") + 1]
            data = data.replace(string, "__string__")

        # 들여쓰기에 대한 처리
        data = data.replace("    ", "\t")
        indent = data.count("\t")

        # 명령문 검출 방식 정의
        r_push = data.find("넣기")
        r_operator = "".join(data.split()[-1:]).find("더하기") + "".join(data.split()[-1:]).find("빼기") +\
                    "".join(data.split()[-1:]).find("곱하기") + "".join(data.split()[-1:]).find("나누기")
        r_print = data.find("보여주기") + data.find("출력하기")
        r_input = data.find("입력받기") # TODO: input에서 무조건 문자열로 값을 받음 : 반환값 타입을 지정하게 수정해야 함
        r_repeatNum = data.find("번 반복하기")
        r_repeatForever = data.find("무한 반복하기")
        r_stopRepeat = data.find("반복 그만하기")
        r_if = data.find("만약")
        r_elif = data.find("그렇지 않고 만약")
        r_else = data.find("아니면")
        r_for = data.find("넣어가며 반복하기")
        r_def = data.find("함수")
        r_return = data.find("내보내기")
        r_defstop = data.find("함수 끝내기")

        # 검출된 명령문을 if-elif-else로 찾음
        if r_push != -1:
            a = data.replace("에게 ", " = ").replace("에 ", " = ").replace("을 넣기", "").replace("를 넣기", "")
        elif r_operator != -4:
            a = op_processor(data, indent)
        elif r_print != -2:
            a = data.replace("을 보여주기", '').replace("를 보여주기", '').replace("을 출력하기", "").replace("를 출력하기", "").replace("\n", " ")
            a = ("\t" * indent) + "print(" + a.replace("\t", '').strip() + ")\n"
        elif r_input != -1:
            data = data.replace("으로", "로")
            a = re.split("[을|를]|로", data)
            a = ("\t" * indent) + a[0].strip() + " = input(" + a[1].strip() + ")\n"
        elif r_repeatNum != -1:
            a = data.replace("번 반복하기", "").replace("\t", "").replace("\n", "")
            a = ("\t" * indent) + loopcnt(indent) + " = 0\n" + ("\t" * indent) + "while " + loopcnt(indent) \
                + " < " + a + "\n" + ("\t" * indent) + "\t" + loopcnt(indent) + " = " + loopcnt(indent) + " + 1\n"
        elif r_repeatForever != -1:
            a = data.replace("무한 반복하기", "while True")
        elif r_stopRepeat != -1:
            a = data.replace("반복 그만하기", "break")
        elif r_if != -1 or r_elif != -1:
            a = if_processor(data, indent)
        elif r_else != -1:
            a = data.replace("아니면", "else")
        elif r_for != -1:
            a = data.replace("범위", "range")
            a = re.split("[을|를]|에", a)
            a = ("\t" * indent) + "for " + a[1].strip() + " in " + a[0].strip() + ":\n"
        elif r_defstop != -1:
            a = data.replace("함수 끝내기", "return")
        elif r_def != -1:
            a = data.replace("함수", "def")
        elif r_return != -1:
            a = data.replace("을 내보내기", "").replace("를 내보내기", "").strip()
            a = ("\t" * indent) + "return " + a
        else:
            a = data

        # 명령문 변환 후 처리
        a = a.replace("글자(", "str(")
        a = a.replace("__string__", string)
        result.append(a)
    return result

# 연산문 처리 함수
def op_processor(data, indent):
    data = re.split("에서|에|을|를", data)  # (변수)[에/에서] (값)[을/를] [더하기/빼기/곱하기/나누기]

    data[0] = data[0].strip()
    data[1] = data[1].strip()
    data[2] = data[2].replace("더하기", "+=").replace("빼기", "-=").replace("곱하기", "*=").replace("나누기", "/=").strip()
    result = ("\t" * indent) + data[0] + " " + data[2] + " " + data[1] + "\n"
    return result

# if 문 처리 함수
def if_processor(data, indent):
    data = data.split()

    # elif 구분용 카운터
    i = 0

    if data[0].find("그렇지") != -1:
        i = 2
    print(len(data))
    if len(data) == 4:  # 만약 변수가 값보다 상태하면
        # 변수
        data[i + 1] = data[i + 1][:-1]

        # 값 (와, 과, 보다)
        if data[i + 2][-1:].find("와") >= 0:
            data[i + 2] = data[i + 2][:-1]
        elif data[i + 2][-1:].find("과") >= 0:
            data[i + 2] = data[i + 2][:-1]
        elif data[i + 2][-2:].find("보다") >= 0:
            data[i + 2] = data[i + 2][:-2]
        else:
            pass

        # (조건) (이, 으, 르)면
        data[i + 3] = data[i + 3].replace(":", "").replace("이면", "").replace("으면", "").replace("르면", "").replace("면", "")
        data[i + 3] = data[i + 3].replace("이상", ">=").replace("이하", "<=").replace("초과", ">").replace("크", ">").replace("미만", "<").replace("작", "<").replace("같", "==").replace("다", "!=")

        if i == 2:
            result = ("\t" * indent) + "elif " + data[i + 1] + " " + data[i + 3] + " " + data[i + 2] + ":\n"
        else:
            result = ("\t" * indent) + "if " + data[1] + " " + data[3] + " " + data[2] + ":\n"
        return result
    elif len(data) == 3 or len(data) == 5:  # 만약 변수가 값이면
        result = (data[i] + data[i + 1]).replace("이", " == ").replace("가", " == ").replace("만약", "").replace("그렇지않고", "")
        data[i + 2] = data[i + 2].replace("이면", "").replace("면", "")

        if i == 2:
            result = ("\t" * indent) + "elif " + result + data[i + 2] + "\n"
        else:
            result = ("\t" * indent) + "if " + result + data[i + 2] + "\n"
        return result
    else:
        return "error"

# 반복문 카운터 처리
def loopcnt(indent):
    loop_alphabet = "ijklmnop"
    if indent <= 7:
        return loop_alphabet[indent]
    else:
        return "__loopcnt" + str(indent)

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, AraCompiler.py를 사용하세요.")
    sys.exit(1)
