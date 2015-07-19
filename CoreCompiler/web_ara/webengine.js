// Web-customized-engine for Ara Web Compiler
// @author: hongseunghwan
// June 14, 2015

function convert(araCode):
    var result = [];
    is_turtle = False;
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
        r_import = data.find("불러오기")
        r_for = data.find("넣어가며 반복하기")
        r_elif = data.find("아니고 만약")
        r_else = data.find("아니면")
        r_def = data.find("함수")
        r_defstop = data.find("함수 끝내기")
        r_jump = data == "\n"

        # Turtle Graphics 설정
        rt_decl = data.find("거북이 등장") # 홍승환 거북이 등장
        rt_forward = data.find("앞으로") # 홍승환 거북이 3만큼 앞으로
        rt_backward = data.find("뒤로") # 홍승환 거북이 3만큼 뒤로
        rt_left = data.find("좌회전") # 홍승환 거북이 좌회전
        rt_right = data.find("우회전") # 홍승환 거북이 우회전
        rt_turn = data.find("뒤돌아") # 홍승환 거북이 뒤돌아

        # TODO: 범위에서 반복을 컴파일하지 않음 : 추가 필요
        # TODO: input에서 타입 지정을 한글로 그대로 출력 : 처리 필요

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
        elif rt_turn != -1:
            a = data.split()
            a = ("\t" * indent) + a[0] + ".right(180)\n"
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
                    value.push(piece[:-1])
                elif piece[-2:] == "으로":
                    value.push(piece[:-2])
                elif piece[-1:] == "로":
                    value.push(piece[:-1])
                elif piece[-3:] == "으로써":
                    value.push(piece[:-3])
                elif piece[-2:] == "로써":
                    value.push(piece[:-2])
                elif piece[-3:] == "으로서":
                    value.push(piece[:-3])
                elif piece[-2:] == "로서":
                    value.push(piece[:-2])

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
                value[2] = value[2].replace("정수", "int").replace("소수", "float").replace("문자열", "str").replace("긴정수", "long")
                a = f_input.format(dest=value[0], value=value[1], type=value[2])
            else:
                pass  # 명령어 에러

        # 후처리 : 문자열 재 치환 : result로 내보내기
        a = a.replace("글자(", "str(")
        a = a.replace("__string__", string)
        a = a.replace("범위(", "range(")
        result.push(a)

    # 후처리 : 터틀 그래픽 사용 후 화면 정지
    if is_turtle:
        result.push("turtle.mainloop()")
        result.push("")

    return result

# if 문 처리 함수
def if_processor(data, indent):  # 만약 변수이(가) 값(이)면 / 만약 변수이(가) 값이(가) 아니면 / 만약 변수이(가) 상태 이상/이하/초과/미만(이)면

    data = data.replace("아니고 만약", "elif").replace("만약", "if").replace("아니면", "else")
    data = data.replace(":", "")

    if data.find("else") != -1:
        return ("\t" * indent) + "else:\n"

    data = data.split()
    data[1] = data[1].replace(data[1][-1:], "")
    print(data)
    if_type = -1

    if len(data) == 3:
        if data[2][-2:] == "이면":
            data[2] = data[2].replace(data[2][-2:], "")
        else:
            data[2] = data[2].replace(data[2][-1:], "")
        if_type = 1  # 3자리 : 만약 변수가 값이면
    else:
        if data[3] == "아니면":
            data[2] = data[2].replace(data[2][:-1], "")
            if_type = 2  # 4자리 : 만약 변수가 값이 아니면
        else:
            if data[3][-2:] == "이면":
                print("triggered")
                data[3] = data[3].replace(data[3][-2:], "")
            else:
                data[3] = data[3].replace(data[3][-1:], "")
            if_type = 3  # 4자리 : 만약 변수가 상태 조건이면

    if if_type == 1:
        result = data[0] + " " + data[1] + " == " + data[2]
    elif if_type == 2:
        result = data[0] + " " + data[1] + " != " + data[2]
    elif if_type == 3:
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

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, ara 명령어를 사용하세요.")
    sys.exit(1)
