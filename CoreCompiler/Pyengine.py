from datetime import datetime

__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    result.append("# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의하여 작성되어진 Python 파일입니다.\n")
    result.append("# This file has been made by Ara, constructed by Korean language, Hangeul.\n")
    result.append("# 만들어진 시각 : " + datetime.today().strftime("%Y년 %m월 %d일 %H시 %M분 %S초\n\n"))
    for i in range(0, len(araCode)):
        data = araCode[i]

        # 들여쓰기에 대한 처리
        indent = data.count("\t")

        # 한글로 된 사칙 연산 정의
        data = data.replace("더하기", "+").replace("빼기", "-").replace("나누기", "/").replace("곱하기", "*").replace("나머지", "%")

        # 명령문 검출 방식 정의
        r_push = data.find("넣기")
        r_print = data.find("출력하기")
        r_repeatNum = data.find("번 반복하기")
        r_repeatForever = data.find("무한 반복하기")
        r_stopRepeat = data.find("반복 그만하기")
        r_if = data.find("만약")

        # 검출된 명령문을 if-elif-else로 찾아서 런타임 절약
        if r_push != -1:
            a = data.replace("에 ", " = ").replace("을 넣기", "").replace("를 넣기", "")
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
            a = data.replace("무한 반복하기", "while true")
            result.append(a)
        elif r_stopRepeat != -1:
            a = data.replace("반복 그만하기", "break")
            result.append(a)
        elif r_if != -1:
            a = if_processor(data, indent)
            result.append(a)
        else:
            result.append(data)
    return result

def if_processor(data, indent):
    data = data.split()

    # 변수
    data[1] = data[1][:-1]

    # 값 (와, 과, 보다)
    if data[2][-1:].find("와") >= 0:
        data[2] = data[2][:-1]
    elif data[2][-1:].find("과") >= 0:
        data[2] = data[2][:-1]
    elif data[2][-2:].find("보다") >= 0:
        data[2] = data[2][:-2]
    else:
        pass

    # (조건) (이, 으, 르)면
    data[3] = data[3].replace(":", "").replace("이면", "").replace("으면", "").replace("르면", "").replace("면", "")
    data[3] = data[3].replace("이상", ">=").replace("이하", "<=").replace("초과", ">").replace("크", ">").replace("미만", "<").replace("작", "<").replace("같", "==").replace("다", "!=")

    result = ("\t" * indent) + "if " + data[1] + " " + data[3] + " " + data[2] + ":\n"
    return result

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, AraCompiler.py를 사용하세요.")
    sys.exit(1)
