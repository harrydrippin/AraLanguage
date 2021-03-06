﻿from setuptools import setup
import os, sys

print("[*] 아라(Ara) : 한글 프로그래밍 언어\n")
if str(sys.version_info[:1]).replace("(", "").replace(",)", "") != "3":
    print("[!] 아라는 Python 3 이상에서 동작합니다. Python 최신 버전이 필요합니다.")
    print("[!] 관련된 정보는 https://www.python.org/downloads/ 에서 확인하실 수 있습니다.")
    print("[!] 만약 Python 3이 설치되어있다면, python3 setup.py install 로 다시 시도해주십시오.")
    sys.exit(0)

setup(
    name='Ara',
    packages=['ara'],
    version='1.0.0',
    author='홍승환',
    author_email='hj332921@naver.com',
    entry_points = {
        'console_scripts': [
            'ara = ara.AraCompiler:main',
        ],
    },
)
if os.name == 'nt':
    print("[?] 파이썬의 설치 경로를 입력해주세요. (일반적으로 C:\Python[버전] 입니다.)")
    ins_position = input("[!] 입력 : ")
    os.system("setx PATH \"%PATH%;" + ins_position.strip() + "\Scripts\"")
    print("[+] 완료되었습니다! 즐거운 프로그래밍 되세요 :)")


