# -*- coding: utf-8 -*-
import sys, os, argparse
from datetime import datetime
import re

__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    result.append("# -*- coding : utf-8 -*-\n")
    result.append("# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.\n")
    result.append("# NewPyengine build, beta 0.0.3\n")
    result.append("# 만들어진 시각 : " + datetime.today().strftime("%Y. %m. %d. %H:%M:%S\n\n"))
    is_turtle = False
    for i in range(0, len(araCode)):
        data = araCode[i]
        string = ""

        # 전처리 : 문자열 치환
        if data.find("\"") + data.rfind("\"") != -2:
            string = data[data.find("\""):data.rfind("\"") + 1]
            data = data.replace(string, "__string__")

        if data.strip("\t").strip("\n") == "":
            data = ""

        # 전처리 : 들여쓰기 처리
        data = data.replace("    ", "\t")
        indent = data.count("\t")

        # 단순 명령어 선별
        r_repeatNum = data.find("번 반복하기")
        r_repeatForever = data.find("무한 반복하기")
        r_stopRepeat = data.find("반복 그만하기")
        r_if = data.find("만약")
        r_import = data.find("불러오기")
        r_for = data.find("넣어가며 반복하기")
        r_elif = data.find("아니고 만약")
        r_else = data.find("아니면")
        r_def = data.find("함수")
        r_defstop = data.find("함수 끝내기")
        r_jump = data == "\n" or data == ""

        # Turtle Graphics 설정
        rt_decl = data.find("거북이 등장") # 홍승환 거북이 등장
        rt_forward = data.find("앞으로") # 홍승환 거북이 3만큼 앞으로
        rt_backward = data.find("뒤로") # 홍승환 거북이 3만큼 뒤로
        rt_left = data.find("좌회전") # 홍승환 거북이 좌회전
        rt_right = data.find("우회전") # 홍승환 거북이 우회전
        rt_leftturn = data.find("왼쪽으로") # 홍승환 왼쪽으로 90도 회전
        rt_rightturn = data.find("오른쪽으로") # 홍승환 오른쪽으로 90도 회전

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
        elif r_import != -1:
            a = data.split()
            if a[0] == "거북이":
                a[0] = "turtle"
            a = ("\t" * indent) + "import " + a[0]
        elif r_for != -1:
            a = data.replace("범위", "range")
            a = re.split("[을|를]|에", a)
            a = ("\t" * indent) + "for " + a[1].strip() + " in " + a[0].strip() + ":\n"
        elif r_defstop != -1:
            a = data.replace("함수 끝내기", "return")
        elif r_def != -1:
            a = data.replace("함수", "def")
        elif r_jump:
            a = "\n"
        elif rt_decl != -1:
            a = data.split()
            a = ("\t" * indent) + a[0] + " = turtle.Turtle()\n"
            is_turtle = True
        elif rt_forward != -1:
            a = data.split()
            a[2] = a[2].replace("만큼", "")
            a = ("\t" * indent) + a[0] + ".forward(" + a[2] + ")\n"
        elif rt_backward != -1:
            a = data.split()
            a[2] = a[2].replace("만큼", "")
            a = ("\t" * indent) + a[0] + ".backward(" + a[2] + ")\n"
        elif rt_left != -1:
            a = data.split()
            a = ("\t" * indent) + a[0] + ".left(90)\n"
        elif rt_right != -1:
            a = data.split()
            a = ("\t" * indent) + a[0] + ".right(90)\n"
        elif rt_leftturn != -1:
            a = data.split()
            a = ("\t" * indent) + a[0] + ".left(" + a[2].replace("도", "") + ")\n"
        elif rt_rightturn != -1:
            a = data.split()
            a = ("\t" * indent) + a[0] + ".right(" + a[2].replace("도", "") + ")\n"
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
            f_push = ("\t" * indent) + "{dest} = {value}\n"
            f_show = ("\t" * indent) + "print({value})\n"
            f_plus = ("\t" * indent) + "{dest} += {value}\n"
            f_minus = ("\t" * indent) + "{dest} -= {value}\n"
            f_mul = ("\t" * indent) + "{dest} *= {value}\n"
            f_div = ("\t" * indent) + "{dest} /= {value}\n"
            f_input = ("\t" * indent) + "{dest} = {type}(input({value}))\n"

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
                value[2] = value[2].replace("정수", "int").replace("소수", "float").replace("문자열", "str").replace("긴정수", "long")
                a = f_input.format(dest=value[0], value=value[1], type=value[2])
            else:
                pass  # 명령어 에러


        # 후처리 : 문자열 재 치환 : result로 내보내기
        a = a.replace("글자(", "str(")
        a = a.replace("__string__", string)
        a = a.replace("범위(", "range(")
        result.append(a)

    # 후처리 : 터틀 그래픽 사용 후 화면 정지
    if is_turtle:
        result.append("turtle.mainloop()")
        result.append("")

    return result

# if 문 처리 함수
def if_processor(data, indent):  # 만약 변수이(가) 값(이)면 / 만약 변수이(가) 값이(가) 아니면 / 만약 변수이(가) 상태 이상/이하/초과/미만(이)면

    data = data.replace("아니고 만약", "elif").replace("만약", "if")
    data = data.replace(":", "")

    if data.strip("\t").strip("\n") == "아니면:":
        data = data.replace("아니면", "else")

    if data.find("else") != -1:
        return ("\t" * indent) + "else:\n"

    data = data.split()
    data[1] = data[1].replace(data[1][-1:], "")
    if_type = -1

    if len(data) == 3:
        if data[2][-2:] == "이면":
            data[2] = data[2].replace(data[2][-2:], "")
        else:
            data[2] = data[2].replace(data[2][-1:], "")
        if_type = 1  # 3자리 : 만약 변수가 값이면
    else:
        if data[3] == "아니면":
            data[2] = data[2].replace(data[2][-1:], "")
            if_type = 2  # 4자리 : 만약 변수가 값이 아니면
        else:
            if data[3][-2:] == "이면":
                data[3] = data[3].replace(data[3][-2:], "")
            elif data[3] == "크면" or data[3] == "작으면": # 4자리 : 만약 변수가 상태보다 크면/작으면
                data[2] = data[2][:-2]
                data[3] = data[3][:-1]
            else:
                data[3] = data[3].replace(data[3][-1:], "")
            if_type = 3  # 4자리 : 만약 변수가 상태 조건이면

    if if_type == 1:
        result = data[0] + " " + data[1] + " == " + data[2]
    elif if_type == 2:
        result = data[0] + " " + data[1] + " != " + data[2]
    elif if_type == 3:
        data[3] = data[3].replace("크", ">").replace("작", "<")
        result = data[0] + " " + data[1] + " " + data[3] + " " + data[2]
        result = result.replace("이상", ">=").replace("이하", "<=").replace("초과", ">").replace("미만", "<")
    else:
        pass  # 에러 출력

    result = ("\t" * indent) + result + ":\n"
    return result

# 반복문 카운터 처리
def loopcnt(indent):
    loop_alphabet = "ijklmnop"
    if indent <= 7:
        return loop_alphabet[indent]
    else:
        return "__loopcnt" + str(indent)

def main():
    p = argparse.ArgumentParser(description="예) ara sample.ara / ara -n sample.ara / ara sample.ara C:\myProjects")
    p.add_argument("arafile", help="작성하신 아라 파일의 경로", metavar="[아라 파일]")
    p.add_argument("-o", "--output", help="Python 파일 출력 경로, 필수 아님", default=".", type=str, metavar="<출력 경로>")
    p.add_argument("-n", "--dontrun", help="이 옵션이 부여되면, 변환만 수행하고 실행하지 않습니다.", action="store_false")

    # 옵션 파싱 및 변수 설정
    args = p.parse_args()
    infile = args.arafile
    outfile = args.output

    # 아라 파일 오픈 (.ara) 혹은 인코딩 에러 catch 후 수정
    try:
        if ".ara" not in infile:
            raise Exception
        f = open(infile, "rU", encoding="euc-kr")
        araCode = f.readlines()
    except UnicodeDecodeError as e:
        f.close()
        f = open(infile, "rU", encoding="utf-8")
        araCode = f.readlines()

    if "".join(araCode[-1:]).find("아라") == -1:
        print("[!] 정상적인 아라 파일이 아닙니다! 파일 하단에 \"아라\" 문자열을 넣으셨습니까?")
        sys.exit(9)
    else:
        araCode.pop()

    # 변환 완료 소스 리스트 준비
    py_code = []

    # 언어별로 변환 : 엔진 연계
    try:
        py_code = convert(araCode)
        f.close()
    except Exception as e:
        print("[-] 예기치 못한 오류가 발생했습니다. 다시 시도하시거나, 에러 내용을 문의해주세요.")
        print("[-] 에러 명세 : " + e)
        sys.exit(4)

    outfile_path = outfile + "/" + os.path.basename(infile).replace(".ara", "") + ".py"

    try:
        f = open(outfile_path, "w")
        for i in range(0, len(py_code) - 1):
            f.write(py_code[i])
        f.close()
    except Exception as e:
        print("[-] 예기치 못한 오류가 발생했습니다. 다시 시도하시거나, 에러 내용을 문의해주세요.")
        print("[-] 에러 명세 : " + str(e))
        sys.exit(5)
    print("[*] 실행 결과 : \n")
    if os.name != "nt":
        os.system("python3 " + outfile_path)
    else:
        os.system("python " + outfile_path)
    sys.exit(1)

main()
