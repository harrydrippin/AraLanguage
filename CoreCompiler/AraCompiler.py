import optparse

__author__ = 'Seunghwan Hong'
("이 파일은 아라로 작성된 파일을 인자값으로 받고 그것을 다른 언어로 바꾸어주는 파일입니다.\n"
 "변환할 파일을 입력받고 Cmodule과 Pymodule을 이용하여 각각 C와 Python으로 변환합니다. \n"
 "변환되는 파일은 사용자가 직접 선택할 수 있으며, 원하는 경우 둘 다로 바꿀 수도 있습니다."
 )

p = optparse.OptionParser()
usage = "%prog -i [아라 파일] -o [출력될 파일 경로] (-c, -p, -b)"

p.set_usage(usage)

# 본 파일과 변환된 파일의 경로를 지정
p.add_option("-i", "--infile", action="store", help="작성하신 아라 파일의 경로", dest="infile", metavar="[아라 파일]")
p.add_option("-o", "--outfile", action="store", help="변환된 파일의 경로 (확장자는 자동으로 정해집니다)", dest="outfile", metavar="[출력될 파일 경로]")

# 변환할 언어를 지정
p.add_option("-c", action="store_const", const=1, help="C로 변환합니다. -p와 함께 쓰실 수 없습니다. (-b 참조)", dest="lang")
p.add_option("-p", "--python", action="store_const", help="Python으로 변환합니다. -c와 함께 쓰실 수 없습니다. (-b 참조)", const=2, dest="lang")
p.add_option("-b", "--both", action="store_const", help="C와 Python 모두로 변환합니다. -c나 -p와 함께 쓰실 수 없습니다.", const=3,  dest="lang")

# 옵션 파싱 및 변수 설정
opts, args = p.parse_args()
infile = opts.infile
outfile = opts.outfile
lang = opts.lang

print(infile)
print(outfile)
print(lang)