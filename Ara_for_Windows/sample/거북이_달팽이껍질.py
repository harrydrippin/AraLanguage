# -*- coding: utf-8 -*-
# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.
# NewPyengine build, beta 0.0.3
# 만들어진 시각 : 2015. 07. 22. 20:16:33

 # 이 예제는 거북이를 활용해서 달팽이 껍질 모양을 그리는 예제입니다.

 # 아라의 기본 사용 규칙과 거북이의 사용 방법을 잘 알고 있어야 합니다.


import turtle
홍길동 = turtle.Turtle()

횟수 = 1

i = 0
while i < 50:
	i = i + 1
	홍길동.forward(10*횟수)
	홍길동.right(90)
	횟수 += 1

turtle.mainloop()