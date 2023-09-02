import tkinter as tk
from functools import partial
from wordesafunctions import *
from time import sleep

abc = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
letter_size = 64
field_num = 5
field_color = '#def'
word_color = '#9cf'
liter_now_color = '#d8d'
field_letter_color = '#48c'
field_char = []
done_color = '#def'
field_char_set = set()
gessed = []
wordchain = []
score = 0.0

def alert(message):
    wconsole['text'] = message
##    xwc = -5 * letter_size
##    while xwc < 0:
##        wconsole.place(x = xwc)
##        xwc += 5
##        wconsole.after()
##        print(xwc)
    wconsole.place(x = 0)
#    print(-5 * letter_size)
        
        
def click(x, y):
    if wordchain:
        if not [x, y] in wordchain:
            if abs(wordchain[-1][0] - x) <= 1 and abs(wordchain[-1][1] - y) <= 1:
                a, b = wordchain[-1]
                field[a][b]['bg'] = word_color
                field[x][y]['bg'] = liter_now_color
                wordchain.append([x,y])
                word.insert(tk.END,field[x][y]['text'])
    else:
        wordchain.append([x,y])
        field[x][y]['bg'] = liter_now_color
        word.insert(tk.END,field[x][y]['text'])

#    field[x][y]['bg'] = 'red'

def field_renew():
    global wordchain
    word.delete(0, tk.END)
    wordchain = []
    wconsole.place(x = -letter_size * 5)
    for i in range(field_num):
        for j in range(field_num):
            field[i][j]['bg'] = field_color
            field[i][j]['fg'] = field_letter_color

def check(self):
    global score
    global gessed
    if btnStart['text'] == 'Начать':
        start()
    else:
        wr = word.get().lower()
        field_renew()
#        print('wr',wr)
        if len(wr) < 3:
            alert('минимум 3 буквы')
        if not wr in voc:
            alert('не знаю слова\n'+wr)
            score -= 0.1
        elif wordexist(wr, field_char, field_char_set) != [[]]:
#            print(wordexist(wr, field_char, field_char_set),wr,field_char)
            if wr in gessed:
                alert('уже было слово\n'+wr)
            else:
                gessed.append(wr)
                score += (len(wr) - 2) ** 2
#                print('gessed')
        else:
            alert('нельзя составить\n слово '+wr)
            score -= 0.1
    wscore['text'] = str(score)[:8]
            
#    print(word.get())
#    field_renew()
    

def bcsp(self):
    global wordchain
    if wconsole.winfo_x() >= 0:
        wconsole.place(x = -5 * letter_size)
    if wordchain:
        x, y = wordchain.pop()
        field[x][y]['bg'] = field_color
        if wordchain:
            x, y = wordchain[-1]
            field[x][y]['bg'] = liter_now_color

def clear(self):
    field_renew()
    
def start():
    global field_char_set
    global field_char
    global score
    gn = word.get()
    if gn.isdigit():
        field_char = get_game(int(gn))
        word.delete(0, tk.END)
    else:
        field_char = get_game()
    field_renew()
    for i in range(field_num):
        for j in range(field_num):
            field[i][j]['text'] = field_char[i][j].upper()
            field_char_set.add(field_char[i][j])
    btnStart['text'] = 'Новая'
    wscore['text'] = '0.0'
    score = 0
#    print(field_char_set)

window = tk.Tk()
window.resizable(False, True)
window.title("wordesa")
window.geometry(f'{letter_size * field_num}x{letter_size * (field_num + 3)}')
field = [[[] for _ in range(field_num)] for _ in range(field_num)]
for i in range(field_num):
    for j in range(field_num):
        field[i][j] = tk.Button(text = '',
                                font = f'mono {letter_size//2}',
                                command = partial(click, i, j),
                                width = 1)
        field[i][j].place(x = j * letter_size, y = (i + 1) * letter_size, width = letter_size, height = letter_size)
#        field[i][j]['text'] = qabc[i * field_num + j].upper()
        field[i][j]['bg'] = field_color
        field[i][j]['fg'] = field_letter_color
word = tk.Entry(master = window,font = f'arial {letter_size//2}', justify = tk.CENTER)
word.place(x = 0, y = letter_size * (field_num + 1), width = letter_size * field_num, height = letter_size)
word['bg'] = field_color
#word['enabled'] = False
wscore = tk.Label(font = f'arial {letter_size//2}', justify = tk.CENTER)
wscore['text'] = '0.0'
wscore.place(x = 0, y = 0, width = letter_size * field_num)
word.focus()
btnStart = tk.Button(text="Начать",
                     font = f'arial {letter_size//2}',
                     command = start)
btnStart.place(x = letter_size,
               y = 7 * letter_size,
               height = letter_size,
               width = letter_size * (field_num - 2))
wconsole = tk.Label(font = f'arial {letter_size//4}',
                    justify = tk.CENTER,
                    text = 'словеса',
                    bg = field_color,
                    relief = 'raised')
wconsole.place(x = 0, y = 3 * letter_size ,
               width = letter_size * field_num,
               height = letter_size)

word.bind('<Return>', check)
word.bind('<BackSpace>', bcsp)
wconsole.bind('<Button-1>', clear)
window.mainloop()
