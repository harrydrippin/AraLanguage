# -*- coding : utf-8 -*-
from datetime import datetime
import re
__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    result.append("# -*- coding : utf-8 -*-\n")
    result.append("# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의하여 작성되어진 Python 파일입니다.\n")
    result.append("# NewPyengine build, beta 0.0.3\n")
    result.append("# 만들어진 시각 : " + datetime.today().strftime("%Y. %m. %d. %H:%M:%S\n\n"))
    for i in range(0, len(araCode)):
        pass
    # TODO: 조사 연구용 엔진 파일. 조사 스플릿, 의미 분석, 포맷, 추가의 알고리즘.

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
def if_processor(data, indent): # TODO : 만약 결과가 '0이면'의 꼴 지원하게 수정 [ 만약 변수가 값보다 상태(하)면, 만약 변수가 값이면, (+) 만약 변수가 값이 아니면? ]
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
