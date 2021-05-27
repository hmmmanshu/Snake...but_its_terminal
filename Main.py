# Snake game
import random
import curses
from curses import textpad
import time
ANTI_DIR = {
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT
}

DIR = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]


def randomgen(snake, box):
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food

def main(stdscr, highscore):
    
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]] 
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    for y,x in snake:
        stdscr.addstr(y, x, '▅')

    food = randomgen(snake, box)
    stdscr.addstr(food[0], food[1], 'o')

    score = 0
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)
    highscore_text = "High Score: {}".format(highscore)
    stdscr.addstr(2, sw//2 - len(highscore_text)//2, highscore_text)

    while 1:
        key = stdscr.getch()

        if key in DIR and key != ANTI_DIR[direction]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]

        stdscr.addstr(new_head[0], new_head[1], '▅')
        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            score_text = "Score: {}".format(score)
            highscore_text = "High Score: {}".format(highscore)
            stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)
            stdscr.addstr(2, sw//2 - len(highscore_text)//2, highscore_text)
            stdscr.refresh()
            food = randomgen(snake, box)
            stdscr.addstr(food[0], food[1], 'o')

            stdscr.timeout(100 - (len(snake)//3)%90)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        if (snake[0][0] in [box[0][0], box[1][0]] or 
            snake[0][1] in [box[0][1], box[1][1]] or 
            snake[0] in snake[1:]):
            msg = "Game Over!"
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            return score


menu = ['Start', 'High Score', 'Exit']

def print_menu(stdscr, current_selection):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for index, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + index
        if(index == current_selection):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def menu_init(stdscr):
    highscore = 0
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_selection = 0
    print_menu(stdscr, current_selection)
    
    while(1):
        key = stdscr.getch()

        if(key == curses.KEY_UP and current_selection>0):
            current_selection-=1
        elif(key == curses.KEY_DOWN and current_selection<len(menu)-1):
            current_selection+=1
        elif(key == curses.KEY_ENTER or key in [10, 13]):
            if(current_selection == 0): # Start
                stdscr.clear()
                highscore = max(main(stdscr, highscore), highscore)
            elif(current_selection == len(menu)-1): # Exit
                break
            else:
                # Could be a file IO but ... meh
                h, w = stdscr.getmaxyx()
                stdscr.clear()
                stdscr.addstr(h//2, w//2, str(highscore))
                stdscr.refresh()
                time.sleep(2)
                stdscr.getch()

            stdscr.clear()
        print_menu(stdscr, current_selection)

curses.wrapper(menu_init)
