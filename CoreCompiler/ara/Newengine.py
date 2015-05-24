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
        data = araCode[i]
        string = ""

        # 전처리 : 문자열 치환
        if data.find("\"") + data.rfind("\"") != -2:
            string = data[data.find("\""):data.rfind("\"") + 1]
            data = data.replace(string, "__string__")

        # 전처리 : 들여쓰기 처리
        data = data.replace("    ", "\t")
        indent = data.count("\t")
        ind_prefix = "\t" * indent

        # 단순 명령어 선별
        r_repeatNum = data.find("번 반복하기")
        r_repeatForever = data.find("무한 반복하기")
        r_stopRepeat = data.find("반복 그만하기")
        r_if = data.find("만약")
        r_elif = data.find("그렇지 않고 만약")
        r_else = data.find("아니면")
        r_def = data.find("함수")
        r_defstop = data.find("함수 끝내기")
        r_jump = data == "\n"

        # TODO: 범위에서 반복을 컴파일하지 않음 : 추가 필요
        # TODO: input에서 타입 지정을 한글로 그대로 출력 : 처리 필요
        # TODO: 치명적인 오류 : elif를 error로 처리함 : re.split()으로 다시 구성 필요

        # 단순 명령어, 개행, 주석 걸러내서 치환
        if r_repeatNum != -1:
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
        elif r_defstop != -1:
            a = data.replace("함수 끝내기", "return")
        elif r_def != -1:
            a = data.replace("함수", "def")
        elif r_jump:
            a = "\n"
        else:
            # 공백을 기준으로 나누어 리스트로 변환
            data = data.split()

            i = 0
            pat = re.compile("에서?|을|를|으?로서?써?")
            # 1차 분석 : 조사 기준 정리
            while i < len(data):
                if data[i][-1:] == "기": # 명령어면
                    pass
                elif len(pat.findall(data[i][-2:])) == 0:  # 만일 마지막 부분이 조사를 포함하고 있지 않으면
                    data[i + 1] = data[i] + " " + data[i + 1]
                    data.pop(i)
                i += 1

            # 2차 분석 : 명령어 종류 기반 자릿수 정리
            oper_pat = re.compile("넣|보|출|더|빼|곱|나|입")  # 넣기 보여주기 출력하기 더하기 빼기 곱하기 나누기 입력하기
            oper = oper_pat.search(str(data[-1:])).group()
            if oper == "입":
                i = 3
            elif oper == "넣" or oper == "더" or oper == "빼" or oper == "곱" or oper == "나":
                i = 2
            else:
                i = 1

            if len(data) != i + 1:
                while len(data) != i + 1:
                    data[i] = str(data[i - 1]) + " " + str(data[i])
                    data.pop(i - 1)
                    if len(data) == i + 1:
                        break

            dest = "_NON_"
            value = []

            print(data)
            # 3차 분석 : 인자 분석과 의미 분별 : v1=목적, v2=도구, v3=입력타입
            for piece in data:
                if piece[-2:] == "에서":
                    dest = piece[:-2]
                elif piece[-1:] == "에":
                    dest = piece[:-1]
                elif piece[-1:] == "을" or piece[-1:] == "를":
                    value.append(piece[:-1])
                elif piece[-2:] == "으로":
                    value.append(piece[:-2])
                elif piece[-1:] == "로":
                    value.append(piece[:-1])
                elif piece[-3:] == "으로써":
                    value.append(piece[:-3])
                elif piece[-2:] == "로써":
                    value.append(piece[:-2])
                elif piece[-3:] == "으로서":
                    value.append(piece[:-3])
                elif piece[-2:] == "로서":
                    value.append(piece[:-2])

            # 포맷 정리
            f_push = ind_prefix + "{dest} = {value}\n"
            f_show = ind_prefix + "print({value})\n"
            f_plus = ind_prefix + "{dest} += {value}\n"
            f_minus = ind_prefix + "{dest} -= {value}\n"
            f_mul = ind_prefix + "{dest} *= {value}\n"
            f_div = ind_prefix + "{dest} /= {value}\n"
            f_input = ind_prefix + "{dest} = {type}(input({value}))\n"

            # 포맷
            if oper == "넣":
                a = f_push.format(dest=dest, value=value[0])
            elif oper == "보" or oper == "출":
                a = f_show.format(value=value[0])
            elif oper == "더":
                a = f_plus.format(dest=dest, value=value[0])
            elif oper == "빼":
                a = f_minus.format(dest=dest, value=value[0])
            elif oper == "곱":
                a = f_mul.format(dest=dest, value=value[0])
            elif oper == "나":
                a = f_div.format(dest=dest, value=value[0])
            elif oper == "입":
                print(value)
                a = f_input.format(dest=value[0], value=value[1], type=value[2])
            else:
                pass  # 명령어 에러

        # 후처리 : 문자열 재 치환 : result로 내보내기
        a = a.replace("글자(", "str(")
        a = a.replace("__string__", string)
        result.append(a)

    return result

# if 문 처리 함수
def if_processor(data, indent):
    data = data.split()

    # elif 구분용 카운터
    i = 0

    if data[0].find("그렇지") != -1:
        i = 2

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
        return "error\n"

# 반복문 카운터 처리
def loopcnt(indent):
    loop_alphabet = "ijklmnop"
    if indent <= 7:
        return loop_alphabet[indent]
    else:
        return "__loopcnt" + str(indent)

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, ara 명령어를 사용하세요.")
    sys.exit(1)
