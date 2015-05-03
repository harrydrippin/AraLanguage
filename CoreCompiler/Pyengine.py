__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
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
        else:
            result.append(data)
    return result

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, AraCompiler.py를 사용하세요.")
    sys.exit(1)
