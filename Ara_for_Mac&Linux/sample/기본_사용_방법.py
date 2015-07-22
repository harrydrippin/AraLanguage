# -*- coding: utf-8 -*-
# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.
# NewPyengine build, beta 0.0.3
# 만들어진 시각 : 2015. 07. 22. 19:44:12

 # 이 파일은 기본적으로 알아두어야 할 명령어들을 연습하는 예제입니다.

 # 이것은 주석으로, 앞에 #을 붙이고 글을 쓰면 컴파일러가 무시합니다.

 # 자세한 내용은 사용설명서를 참고하세요. http://aralanguage.oa.to


 # 1. 넣기

a = 10
b = 10 + 13
c = a + b

 # 2. 보여주기

print(c)
print(c + 10)

 # 3. 연산자 (더하기, 빼기, 곱하기, 나누기)

a += 1
a -= 1
a *= 2
a /= 2

 # 4. 입력받기

d = str(input("이름을 입력하세요 : "))
print(d + "님이시군요!")

 # 5. 만약 ~ 아니고 만약 ~ 아니면

if a == 8:
	print("a는 8입니다.")
elif a == 9:
	print("a는 9입니다.")
elif a >= 10:
	print("a는 10 이상입니다.")
else:
	print("잘 모르겠어요...")

 # 6. 무한 반복하기, n번 반복하기, 넣어가며 반복하기

a = 1

while True:
	print("a는 " + str(a)) # a는 숫자이므로, 문자로 바꾸어야 문자열과 합쳐집니다.

	a += 1
	if a == 10:
		break

i = 0
while i < 3:
	i = i + 1
	print("아라는 훌륭한 언어입니다.")

for i in range(1, 51):
	print("현재 i는 " + str(i))

 # 7. 함수

def 합_구하기(첫째, 둘째):
	print(첫째 + 둘째)

print(합_구하기(10, 20)) # 30이 나옵니다.

