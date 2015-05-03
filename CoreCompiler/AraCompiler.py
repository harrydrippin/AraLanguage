import optparse
import sys

__author__ = 'Seunghwan Hong'

p = optparse.OptionParser()
usage = "%prog -i [아라 파일] -o [출력될 파일 경로] (-c, -p, -b)"

p.set_usage(usage)

# 본 파일과 변환된 파일의 경로를 지정
p.add_option("-i", "--infile", action="store", help="작성하신 아라 파일의 경로", dest="infile", metavar="[아라 파일]")
p.add_option("-o", "--outfile", action="store", help="변환된 파일의 경로 (확장자는 자동으로 정해집니다)", dest="outfile", metavar="[출력될 파일 경로]")

# 변환할 언어를 지정
p.add_option("-p", "--python", action="store_const", help="Python으로 변환합니다. -c나 -b와 함께 쓰실 수 없습니다. (-b 참조)", const=1, dest="lang")
p.add_option("-c", action="store_const", const=2, help="C로 변환합니다. -p나 -b와 함께 쓰실 수 없습니다. (-b 참조)", dest="lang")
p.add_option("-b", "--both", action="store_const", help="Python과 C 모두로 변환합니다. -c나 -p와 함께 쓰실 수 없습니다.", const=3,  dest="lang")

# 옵션 파싱 및 변수 설정
opts, args = p.parse_args()
infile = opts.infile
outfile = opts.outfile
lang = opts.lang

# 잘못된 인수 사용에 대한 블럭
if(len(args) != 3) :
    print("잘못된 인수 사용입니다. 인수는 3개[-i, -o, (-p, -c, -b)]이어야 합니다.")
    sys.exit(2)