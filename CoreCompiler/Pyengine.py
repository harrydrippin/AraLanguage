from datetime import datetime
import re
__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    result.append("# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의하여 작성되어진 Python 파일입니다.\n")
    result.append("# This file has been made by Ara, constructed by Korean language, Hangeul.\n")
    result.append("# 만들어진 시각 : " + datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S초\n\n"))
    for i in range(0, len(araCode)):
        data = araCode[i]

        # TODO : 반복문을 중첩했을 때 카운터 변수 i가 겹치는 치명적인 버그가 존재 - 대안 필요

        # 들여쓰기에 대한 처리
        indent = data.count("\t")
        data = data.replace("_", " ")

        # 명령문 검출 방식 정의
        r_push = data.find("넣기")
        r_operator = "".join(data.split()[-1:]).find("더하기") + "".join(data.split()[-1:]).find("빼기") +\
                    "".join(data.split()[-1:]).find("곱하기") + "".join(data.split()[-1:]).find("나누기")
        r_print = data.find("출력하기")
        r_repeatNum = data.find("번 반복하기")
        r_repeatForever = data.find("무한 반복하기")
        r_stopRepeat = data.find("반복 그만하기")
        r_if = data.find("만약")
        r_elif = data.find("그렇지 않고 만약")
        r_else = data.find("그렇지 않으면")

        # 검출된 명령문을 if-elif-else로 찾음
        if r_push != -1:
            a = data.replace("에게 ", " = ").replace("에 ", " = ").replace("을 넣기", "").replace("를 넣기", "")
            result.append(a)
        elif r_operator != -4:
            a = op_processor(data, indent)
            result.append(a)
        elif r_print != -1:
            a = data.replace("을 출력하기", '').replace("를 출력하기", '').replace("\n", '')
            b = ("\t" * indent) + "print(" + a.replace("\t", '') + ")\n"
            result.append(b)
        elif r_repeatNum != -1:
            a = data.replace("번 반복하기", "").replace("\t", "").replace("\n", "")
            b = ("\t" * indent) + "i = 0\n" + ("\t" * indent) + "while i < " + a + "\n" + ("\t" * indent) + "\ti = i + 1\n"
            result.append(b)
        elif r_repeatForever != -1:
            a = data.replace("무한 반복하기", "while 0 == 0")
            result.append(a)
        elif r_stopRepeat != -1:
            a = data.replace("반복 그만하기", "break")
            result.append(a)
        elif r_if != -1 or r_elif != -1:
            a = if_processor(data, indent)
            result.append(a)
        elif r_else != -1:
            a = data.replace("그렇지 않으면", "else")
            result.append(a)
        else:
            result.append(data)

        # 한글로 된 사칙 연산 정의
        result[-1:] = "".join(result[-1:]).replace("더하기", "+").replace("빼기", "-").replace("나누기", "/").replace("곱하기", "*").replace("나머지", "%")
    return result

# 연산문 처리 함수
def op_processor(data, indent):
    data = re.split("[에서|에게|에]|[을|를]", data)  # (변수)[에/에서] (값)[을/를] [더하기/빼기/곱하기/나누기]

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

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, AraCompiler.py를 사용하세요.")
    sys.exit(1)
