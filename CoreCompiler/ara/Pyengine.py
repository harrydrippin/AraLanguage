# -*- coding : utf-8 -*-
from datetime import datetime
import re
__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    result.append("# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의하여 작성되어진 Python 파일입니다.\n")
    result.append("# This file has been made by Ara, constructed by Korean language, Hangeul.\n")
    result.append("# 만들어진 시각 : " + datetime.today().strftime("%Y. %m. %d. %H:%M:%S\n\n"))
    for i in range(0, len(araCode)):
        data = araCode[i]

        # 들여쓰기에 대한 처리
        data = data.replace("    ", "\t")
        indent = data.count("\t")

        # 명령문 검출 방식 정의
        r_push = data.find("넣기")
        r_operator = "".join(data.split()[-1:]).find("더하기") + "".join(data.split()[-1:]).find("빼기") +\
                    "".join(data.split()[-1:]).find("곱하기") + "".join(data.split()[-1:]).find("나누기")
        r_print = data.find("보여주기")
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
            result.append(a)
        elif r_operator != -4:
            a = op_processor(data, indent)
            result.append(a)
        elif r_print != -1:
            a = data.replace("을 보여주기", '').replace("를 보여주기", '').replace("\n", '')
            b = ("\t" * indent) + "print(" + a.replace("\t", '') + ")\n"
            result.append(b)
        elif r_repeatNum != -1:
            a = data.replace("번 반복하기", "").replace("\t", "").replace("\n", "")
            b = ("\t" * indent) + loopcnt(indent) + " = 0\n" + ("\t" * indent) + "while " + loopcnt(indent) \
                + " < " + a + "\n" + ("\t" * indent) + "\t" + loopcnt(indent) + " = " + loopcnt(indent) + " + 1\n"
            result.append(b)
        elif r_repeatForever != -1:
            a = data.replace("무한 반복하기", "while True")
            result.append(a)
        elif r_stopRepeat != -1:
            a = data.replace("반복 그만하기", "break")
            result.append(a)
        elif r_if != -1 or r_elif != -1:
            a = if_processor(data, indent)
            result.append(a)
        elif r_else != -1:
            a = data.replace("아니면", "else")
            result.append(a)
        elif r_for != -1:
            a = data.replace("범위", "range")
            a = re.split("[을|를]|에", a)
            b = ("\t" * indent) + "for " + a[1].strip() + " in " + a[0].strip() + ":\n"
            result.append(b)
        elif r_defstop != -1:
            a = data.replace("함수 끝내기", "return")
            result.append(a)
        elif r_def != -1:
            a = data.replace("함수", "def")
            result.append(a)
        elif r_return != -1:
            a = data.replace("을 내보내기", "").replace("를 내보내기", "").strip()
            b = ("\t" * indent) + "return " + a
            result.append(b)
        else:
            result.append(data)

        # 명령문 변환 후 처리
        result[-1:] = "".join(result[-1:]).replace("더하기", "+").replace("빼기", "-").replace("나누기", "/").replace("곱하기", "*").replace("나머지", "%")\
            .replace("글자(", "str(")
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
def if_processor(data, indent): # TODO : re.split()을 사용하여 더 짧게 하고, 만약 결과가 '0이면'의 꼴 지원하게 수정
    data = data.split()

    # elif 구분용 카운터
    i = 0

    if data[0].find("그렇지") != -1:
        i = 2

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

def loopcnt(indent):  # TODO : Dictionary를 사용하여 최적화 필요 / 지금은 임시로!
    if indent == 0:
        return "i"
    elif indent == 1:
        return "j"
    elif indent == 2:
        return "k"
    elif indent == 3:
        return "l"
    elif indent == 4:
        return "m"
    elif indent == 5:
        return "n"
    elif indent == 6:
        return "o"
    elif indent == 7:
        return "p"
    else:
        return "__loopcnt" + str(indent)

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, AraCompiler.py를 사용하세요.")
    sys.exit(1)
