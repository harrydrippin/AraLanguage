from setuptools import setup

setup(
    name='Ara',
    packages=['ara'],
    version='0.0.1',
    description='한글 프로그래밍 언어',
    author='홍승환',
    author_email='hj332921@naver.com',
    entry_points = {
        'console_scripts': [
            'ara = ara.AraCompiler:main',
        ],
    },
)