# -*- coding: utf-8 -*-
# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.
# NewPyengine build, beta 0.0.3
# 만들어진 시각 : 2015. 07. 22. 19:26:35

첫째 = 10
둘째 = 20
합 = 첫째 + 둘째
print(합)

i = 0
while True:
	print(i)
	break
i = 0
while i < 3:
	i = i + 1
	print(합)
	합 = 합 + 1
if i >= 0:
	i = 30 + 50
	print(i)
elif i >= 0:
	i = i + 20
	print(i)
else:
	print(i)

a = True
True인_값 = 10

print(a)
print(True인_값)

i += 1 # 주석입니다.

i -= 1
i *= 1
i /= 1

for x in range(1, 4):
	print("현재 x는 " + str(x))

def 안녕():
	print("안녕")
	return

def 제곱(a):
	a = a ** 2
	print(a)

c = int(input("c를 입력하세요 : "))
print(c)

a = 10

if a == 10:
	print("테스트")

 # 이것은 주석입니다.


print("주석 테스트") # 이것도 주석이지요.

