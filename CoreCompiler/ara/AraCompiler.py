import sys, os, argparse

__author__ = 'Seunghwan Hong'


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
        from ara import Pyengine as engine
        py_code = engine.convert(araCode)
        f.close()
    except Exception as e:
        print("[-] 예기치 못한 오류가 발생했습니다. 다시 시도하시거나, 에러 내용을 문의해주세요.")
        print("[-] 에러 명세 : " + e)
        sys.exit(4)

    outfile_path = outfile + "/" + os.path.basename(infile).replace(".ara", "") + ".py"
    print(outfile_path)

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
        os.system("python3 " + os.path.basename(infile).strip(".ara") + ".py")
    else:
        os.system("python " + os.path.basename(infile).strip(".ara") + ".py")
    sys.exit(1)

main()