# -*- coding: utf-8 -*-
# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.
# NewPyengine build, beta 0.0.3
# 만들어진 시각 : 2015. 07. 22. 20:19:53

 # 거북이로 정육각형을 그리는 쉬운 예제입니다.

 # 아라의 기본 규칙과 거북이에 대한 간단한 이해가 필요합니다.


import turtle
홍길동 = turtle.Turtle()

i = 0
while i < 6:
	i = i + 1
	홍길동.forward(50)
	홍길동.left(60)

turtle.mainloop()