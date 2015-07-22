# -*- coding: utf-8 -*-
# 이 파일은 한글 프로그래밍 언어, 아라(Ara)에 의해 작성되어진 Python 파일입니다.
# NewPyengine build, beta 0.0.3
# 만들어진 시각 : 2015. 07. 22. 20:14:14

 # 이 예제는 거북이의 기본적인 사용 방법을 다루고 있습니다.


 # 1. 거북이 호출

import turtle
 # 2. 거북이 이름 짓고 등장시키기

홍길동 = turtle.Turtle()

 # 3. 전진

홍길동.forward(100)

 # 4. 후진

홍길동.backward(50)

 # 5. 간단한 회전

홍길동.right(90)
홍길동.forward(50)
홍길동.left(90)
홍길동.forward(50)

 # 6. 각도를 이용한 회전

홍길동.left(30)
홍길동.forward(50)
홍길동.right(30)
홍길동.forward(50)

turtle.mainloop()