# -*- coding: cp949 -*-
# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.
# NewPyengine build, beta 0.0.3
# 만들어진 시각 : 2015. 07. 21. 11:19:54

import turtle
홍승환 = turtle.Turtle()

배수 = 10

for 카운터 in range(1, 100):
	홍승환.forward(배수+카운터)
	홍승환.left(30)

turtle.mainloop()