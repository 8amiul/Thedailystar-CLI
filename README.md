# Thedailystar-CLI
#### Video Demo: <URL>

## Description
Thedailystar-CLI is a terminal based program written in python for CS50's Introduction to Programming with Python. This program does scrape news from [The Daily Star](https://www.thedailystar.net/)

## Files
- ```project.py```: The main program.
- ```test_project.py```: To test ```project.py``` using pytest.


## Used Libraries
-  ```BeautifulSoup4```: For scraping data from [The Daily Star](https://www.thedailystar.net/).
-  ```curses```: For handling keyboard input and user interface.
-  ``` requests```: For sending HTTP requests.
-  ```pytest```:  For testing functions built in program
## About Functions
```python
def menu(stdscr, test_= None):
```
This function shows the start menu. It does have 2 options, News and Exit.


- ```stdscr```: Is the curses window. Which is initialized in the main function.
-  ``test_``: Is used for unit testing.

```python
def  get_news_lines():
```
This function scrapes latest news from [Latest News](https://www.thedailystar.net/todays-news) and return the headlines including links in a dictionary.

```python
def  select_news(scr,news_data: dict, test_=None):
```
This function allows a user to choose a news.  It returns the selected news and total displayed lines.

- ```scr```: Is the screen window.
- ``` news_data```:  Is the returned list from ```get_news_lines(args)``` function.
- ```test_```: For unit testing

```python
def  get_news(news_dict: dict, news_lines_list: list, selected_news: int):
```
This function get the link and scrape the news paragraph from the website. and separate the headline and put all the news paragraph lines into a list. It returns headline as string and news paragraph as list.

- news_dict: It grabs the titles and links as news_dict which is a returned value of ```get_news_lines(args)```
- news_lines_list: The total displayed lines.
- selected_news: It returns the position of selected line. Which needs to used in news_lines_list to get the expected news.
```python
def  show_news(scr, hl: str, n_p: list, test_=None):
```
This function is responsible for showing the whole news paragraph including title on top. It doesn't return anything.

- ```hl```: Is the headline which is from ```get_news(args)``` function.
- n_p : Is the news paragraph as a list from ```get_news(args)``` function.

## How the program works?
At first the main function will sequentially call other functions. Inside the main function it will call ```menu(args)``` where selection between menu or exit will be returned. If returned value is news then ```get_news_lines(args)```  will be called and from [Latest News](https://www.thedailystar.net/todays-news) all news will be scraped and the data would be in a dictionary(which will be returned). By using the dictionary user will get a chance to select a news. The selected news will go through ```get_news(args)``` and it will use BeautifulSoup4 to scrape headline and the whole news from the website. Finally ```show_news(args)``` will modify the headline and news paragraph. The modification will effect the size of text per line subject to the height and weight of the terminal screen. At the end of the program the curses module will call the main function inside curses.wrapper().