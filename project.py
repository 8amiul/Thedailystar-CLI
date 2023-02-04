import sys, requests, re, curses
from curses.textpad import rectangle
from bs4 import BeautifulSoup

options = ['News','', 'Exit']
BASE_URL = 'https://www.thedailystar.net'
LATEST_NEWS = 'https://www.thedailystar.net/todays-news'


def main(term_screen):
    indx = menu(term_screen)
    if indx == "News":
        news_dictionary = get_news_lines()
        lines, cursor_pos = select_news(term_screen, news_dictionary)
        try:
            head, news_p = get_news(news_dictionary, lines, cursor_pos)
        except AttributeError:
            sys.exit('Page Not Found!')
        show_news(term_screen, head, news_p)
    else:
        sys.exit('Exited')


def menu(stdscr, test_= None):
    if test_ != None: return options[test_]
    indx = 0
    curses.curs_set(0)
    APP_NAME = "Thedailystar-CLI"
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        center_x = w//2 - 20
        center_y = h//2

        rectangle(stdscr, center_y,center_x , center_y + 6,center_x+40)
        stdscr.addstr(center_y-5,center_x+12, APP_NAME)
        for index, lines in enumerate(options):
            if index == indx:
                stdscr.addstr(center_y+index+2, center_x+3, lines, curses.A_REVERSE)
            else:
                stdscr.addstr(center_y+index+2, center_x+3, lines)
        k = stdscr.getch()
        if k == curses.KEY_UP and 0 < indx:
            indx -= 2
        elif k == curses.KEY_DOWN and indx < len(options)/2:
            indx += 2
        elif k == curses.KEY_ENTER or k == 10:
            stdscr.clear()
            break
    return options[indx]

def get_news_lines():
    NEWS_DATA = {}
    news_page = requests.get(LATEST_NEWS).text
    format_ = BeautifulSoup(news_page,'lxml')
    all_news = format_.find_all('td', class_="views-field views-field-title")
    for i in all_news:
        NEWS_DATA[i.a.text] = i.a.get('href')
    return NEWS_DATA

def select_news(scr,news_data: dict, test_=None):
    init_pos = 0
    cursor_pos = 0
    x_axis = 0
    TOTAL_NEWS = len(news_data.keys())
    maximum_width = max([len(i) for i in news_data.keys()])+1
    while True:
        scr.clear()
        h, w = scr.getmaxyx()
        n = h-3
        if TOTAL_NEWS < h:
            if TOTAL_NEWS == 1:
                n = TOTAL_NEWS
            else:
                n = TOTAL_NEWS-1

        nlist_pad = curses.newpad(TOTAL_NEWS+1, maximum_width)

        lines = list(news_data.keys())[init_pos:init_pos+n]

        if TOTAL_NEWS < h:
            if n == TOTAL_NEWS:
                rectangle(scr, 0,0, 2,w-1)
            else:
                rectangle(scr, 0,0, TOTAL_NEWS,w-1)
        else:
            rectangle(scr, 0,0, n+1,w-1)

        for position in range(n):
            if position == cursor_pos:
                if TOTAL_NEWS == 1:
                    nlist_pad.addstr(0,1,f'{lines[position]}'.strip(), curses.A_REVERSE)
                else:
                    nlist_pad.addstr(position,1,f'{lines[position]}'.strip(), curses.A_REVERSE)
            else:
                if TOTAL_NEWS != 1:
                    nlist_pad.addstr(position,1,lines[position].strip())

        scr.refresh()

        if TOTAL_NEWS < h:
            if TOTAL_NEWS == 1:
                nlist_pad.refresh(0,0, 1,1, 1,w-2)
            else:
                nlist_pad.refresh(0,x_axis, 1,1, TOTAL_NEWS-1,w-2)
        else:
            nlist_pad.refresh(0, x_axis, 1,1, n,w-2) ### !!!

        if test_ != None: return (nlist_pad.getmaxyx()[0], nlist_pad.getmaxyx()[1])

        k = scr.getch()
        if k == curses.KEY_UP:
            if cursor_pos == 0 and init_pos != 0:
                init_pos -= 1
            elif cursor_pos != 0:
                cursor_pos -=1
        elif k == curses.KEY_DOWN:
            if cursor_pos == n-1:
                if init_pos < TOTAL_NEWS-n:
                    init_pos += 1
            else:
                cursor_pos += 1
        elif k == curses.KEY_LEFT:
            if x_axis != 0:
                x_axis -= 1
        elif k == curses.KEY_RIGHT:
            if x_axis < maximum_width-(w-2):
                x_axis +=1
        elif k == curses.KEY_ENTER or k == 10:
            break
        elif k == 27:
            sys.exit()

    scr.clear()

    return lines, cursor_pos


def get_news(news_dict: dict, news_lines_list: list, selected_news: int):
    l = f'{BASE_URL}{news_dict[news_lines_list[selected_news]]}'
    l_source = requests.get(l).text
    format_ = BeautifulSoup(l_source, 'lxml')
    headline = format_.find('h1', itemprop="headline").text
    the_news = format_.find_all('p')
    news_p = []

    for i in the_news:
        if str(i).find('class="intro"') == -1:
            news_p.append(i.text)
    else:
        return headline, news_p


def show_news(scr, hl: str, n_p: list, test_=None):
    y_axis = 0
    while True:
        h, w = scr.getmaxyx()
        scr.clear()
        a = '\n'.join(n_p)
        a = '\n'.join(line.strip() for line in re.findall(r'.{1,%s}(?:\s+|$)' % (w-5), a))

        rectangle(scr, 0,0, 2,w-2)
        hl_pad = curses.newpad(1,len(hl)+1)
        hl_pad.addstr(hl, curses.A_BOLD)

        rectangle(scr, 4,0,h-1,w-2)
        news_pad = curses.newpad(a.count('\n')+2, w-3)
        scr.refresh()
        hl_pad.refresh(0,0, 1,2,2,w-3)
        if test_ == 1: return (hl_pad.getmaxyx()[0], hl_pad.getmaxyx()[1], news_pad.getmaxyx()[0], news_pad.getmaxyx()[1])
        news_pad.addstr(a)
        try:
            news_pad.refresh(y_axis,0, 5,2, h-2,w-3)
        except:
            continue
        k = scr.getch()
        if k == curses.KEY_UP:
            if y_axis != 0:
                y_axis -= 1
        elif k == curses.KEY_DOWN:
            if y_axis < a.count('\n'):
                y_axis += 1
        elif k == curses.KEY_ENTER or k == 10:
            break
        elif k == curses.KEY_BACKSPACE:
            scr.clear()
            loop(scr)
    sys.exit()

def loop(scr):
    news_dictionary = get_news_lines()
    lines, cursor_pos = select_news(scr, news_dictionary)
    head, news_p = get_news(news_dictionary, lines, cursor_pos)
    show_news(scr, head, news_p)

if __name__ == "__main__":
    curses.wrapper(main)