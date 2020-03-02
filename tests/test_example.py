from flask import Flask

from fundooapp.example import calc


app = Flask(__name__)


def test_calc():
    assert calc(2, 5) == 10
