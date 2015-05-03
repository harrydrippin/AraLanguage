import optparse
import sys

__author__ = 'Seunghwan Hong'

p = optparse.OptionParser()
usage = "%prog -i [아라 파일] -o [출력될 파일 경로] (-c, -p, -b)"

p.set_usage(usage)

# 본 파일과 변환된 파일의 경로를 지정
p.add_option("-i", "--infile", action="store", help="작성하신 아라 파일의 경로", dest="infile", metavar="[아라 파일 경로]")
p.add_option("-o", "--outfile", action="store", help="변환된 파일의 경로 ('.'만 입력하면 이 파일과 같은 경로에 변환됩니다)", dest="outfile", metavar="[출력될 파일 경로]")

# 변환할 언어를 지정
p.add_option("-l", "--lang", action="store", type="choice", dest="lang", choices=["c", "py", "python", "all"], help="변환할 언어를 선택합니다. 언어는 C와 Python, 혹은 모두로 변환할 수 있습니다.")

# 옵션 파싱 및 변수 설정
opts, args = p.parse_args()
infile = opts.infile
outfile = opts.outfile
lang = opts.lang

# 아라 파일 오픈 (.ara)
try:
    if(".ara" not in infile) :
        raise Exception
    f = open(infile)
except Exception as e:
    print("아라 파일을 해당 경로에서 찾을 수 없습니다. 확장자가 .ara인 파일까지의 경로를 작성해야 합니다.")
    sys.exit(2)

f.close()