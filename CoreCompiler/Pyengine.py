__author__ = 'Seunghwan Hong'

def convert(araCode):
    result = []
    for i in range(0, len(araCode)):
        data = araCode[i]

        r_push = data.find("넣기")
        r_print = data.find("출력하기")

        if r_push != -1:
            a = data.replace("에 ", " = ").replace("을 넣기", "").replace("를 넣기", "")
            result.append(a)
        elif r_print != -1:
            a = data.replace("을 출력하기", '').replace("를 출력하기", '').replace("\n", '')
            b = "print(" + a + ")\n"
            result.append(b)
        else:
            result.append(data)
    return result

if __name__ == "__main__":
    import sys
    print("이 파일은 모듈로써, 독립실행될 수 없습니다. 변환이 목적이시라면, AraCompiler.py를 사용하세요.")
    sys.exit(1)
