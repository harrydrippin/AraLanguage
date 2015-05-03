import optparse

__author__ = 'Seunghwan Hong'
("이 파일은 아라로 작성된 파일을 인자값으로 받고 그것을 다른 언어로 바꾸어주는 파일입니다.\n"
 "변환할 파일을 입력받고 Cmodule과 Pymodule을 이용하여 각각 C와 Python으로 변환합니다. \n"
 "변환되는 파일은 사용자가 직접 선택할 수 있으며, 원하는 경우 둘 다로 바꿀 수도 있습니다."
 )

p = optparse.OptionParser()

# 본 파일과 변환된 파일의 경로를 지정
p.add_option("-i", action="store", dest="infile")
p.add_option("--input", action="store", dest="infile")
p.add_option("-o", action="store", dest="outfile")
p.add_option("--outfile", action="store", dest="outfile")

# 변환할 언어를 지정
p.add_option("-c", action="store_const", const=1, dest="lang")
p.add_option("-p", action="store_const", const=2, dest="lang")
p.add_option("--py", action="store_const",const=2,  dest="lang")
p.add_option("-b", action="store_const",const=3,  dest="lang")
p.add_option("--both", action="store_const",const=3,  dest="lang")

# 옵션 파싱 및 변수 설정
opts, args = p.parse_args()
infile = opts.infile
outfile = opts.outfile
lang = opts.lang

print(infile)
print(outfile)
print(lang)