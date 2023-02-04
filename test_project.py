import pytest, curses, random
from project import *

scr = curses.initscr()

def test_menu():
    assert menu(scr,0) == 'News'
    assert menu(scr,2) == 'Exit'
    assert menu(scr,1) == ''

    with pytest.raises (IndexError):
        assert menu(scr, 3)
        assert menu(scr, 4)

def test_show_news():
    assert show_news(scr,'', '', 1) == (1,1,2, scr.getmaxyx()[1]-3)
    hl, n_p = "It's my final project", ['I have made a news scraper']
    assert show_news(scr,hl,n_p,1) == (1, len(hl)+1, n_p.count('\n')+2, scr.getmaxyx()[1]-3)
    hl, n_p = 3.1416, 2.71828
    with pytest.raises (TypeError):
        assert show_news(scr,hl,n_p)
        assert show_news(scr)

def test_get_news():
    with pytest.raises (KeyError):
        assert get_news([], {}, int())
        assert get_news({}, [], int())
        assert get_news({}, [], str())


def test_select_news():
    test = dict.fromkeys(["key_" + str(i) for i in range(10)], 0)
    assert select_news(scr, test, 1) == (len(test.keys())+1, max([len(i) for i in test.keys()])+1)
    test = dict.fromkeys(["key_" + str(i) for i in range(1)], 0)
    assert select_news(scr, test, 1) == (len(test.keys())+1, max([len(i) for i in test.keys()])+1)
