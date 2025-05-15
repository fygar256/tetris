#!/usr/bin/python3
import supertext as st
import random
import time

sx=15
sy=0
mx=10
number_of_tetris=0
nextt=-1
tetriscolor=[(255,0,0),(0,255,0),(255,0,255),(0,255,255),(255,255,0),(0,0,255),(255,255,255)]

tetris=[ [['#',
           '#',
           '#',
           '#'],

          ['####']],

         [['# ',
           '##',
           ' #'],

          [' ##',
           '## ']],

         [[' #',
           '##',
           '# '],

          ['## ',
           ' ##']],

         [[' # ',
           ' ##',
           ' # '],

          [' # ',
           '###'],

          [' #',
           '##',
           ' #'],

          ['###',
           ' # ']],

         [['##',
           '##']],

         [[' ##',
           '  #',
           '  #'],

          ['###',
           '#  '],

          ['# ',
           '# ',
           '##'],

          ['  #',
           '###']],

         [['##',
           '# ',
           '# '],

          ['#  ',
           '###'],

          ['  #',
           '  #',
           ' ##'],

          ['###',
           '  #']] ]

def erase_next(tetris):
    if nextt!=-1:
        erase(-10,7,0,nextt,tetris)

def disp_next(tetris):
    st.locate(0,5)
    st.color((0,255,0))
    st.putstr("NEXT")
    put(-10,7,0,nextt,tetris)

def getpat(m,t,tetris):
    m=m%len(tetris[t])
    return (tetriscolor[t],m,tetris[t][m])

def canputp(x,y,m,t,tetris):
    ay=0
    (col,m,pat)=getpat(m,t,tetris)

    for i in pat:
        ax=0
        for c in i:
            if c=='#':
                if st.peek(sx+x+ax,sy+y+ay)!=chr(0):
                    return 0
            ax+=1
        ay+=1
    return 1

def put(x,y,m,t,tetris):
    (col,m,pat)=getpat(m,t,tetris)
    st.color(col)
    ay=0
    for i in pat:
        ax=0
        for c in i:
            if c=='#':
                st.locate(sx+x+ax,sy+y+ay)
                st.putchar(chr(0x97))
            ax+=1
        ay+=1

def erase(x,y,m,t,tetris):
    ay=0
    (col,m,pat)=getpat(m,t,tetris)
    for i in pat:
        ax=0
        for c in i:
            if c=='#':
                st.locate(sx+x+ax,sy+y+ay)
                st.putchar(chr(0))
            ax+=1
        ay+=1

def draw_frame():
    for y in range(0,25):
        st.locate(sx,y)
        st.color((255,255,255))
        st.putchar(chr(0x90))
        st.locate(sx+11,y)
        st.putchar(chr(0x90))

    for x in range(mx):
        st.locate(sx+x+1,24)
        st.color((255,255,255))
        st.putchar(chr(0x90))

    st.refresh()

def place_tetris(tetris):
    global number_of_tetris
    global nextt

    erase_next(tetris)
    t=nextt if nextt!=-1 else random.randrange(0,7)
    nextt=random.randrange(0,7)
    disp_next(tetris)
    m=0
    x=5
    y=0
    if canputp(x,y,m,t,tetris):
        put(x,y,m,t,tetris)
        number_of_tetris+=1
        return (x,y,m,t)
    else:
        return (-1,0,0,0)

def linechecksub(y):
    for j in range(sx,sx+mx+1):
        if st.peek(j,y)==chr(0x0):
            return False
    return True

def linecheck():
    cnt=0
    for i in range(0,24):
        if linechecksub(i):
            st.scrolldown(sx+1,0,mx,i+1)
            cnt+=1
    return cnt

def difficulty(n):
    if n<40:
        r=3
    if n>=40 and n<=70:
        r=2.5
    if n>=71 and n<=100:
        r=2.0
    if n>=101 and n<=130:
        r=1.5
    if n>=131 and n<=160:
        r=1.0
    if n>=161:
        r=0.5
    return r

def main():
    st.setscreen("TETRIS")
    draw_frame()
    (x,y,m,t)=place_tetris(tetris)
    gameover=0
    score=0
    counter=0
    spf=0
    number_of_lines=0
    st.locate(17,12)
    st.color((0,255,0))
    st.putstr("HIT ENTER")
    st.refresh()
    st.locate(17,12)
    st.putstr("         ")
    while(1):
        if st.getkey('return'):
            break
        if st.getkey('q'):
            return
    land=False
    lend=False
    while(1):
        counter+=1
        erase(x,y,m,t,tetris)
        (savem,savex,savey)=(m,x,y)
        dx=0
        if st.getkey('q'):
            return
        if st.getkey('4'):
            dx=-1
        if st.getkey('6'):
            dx=1
        if st.getkey('space'):
            if not spf:
                m=m+1
                spf=1
        else:
            spf=0

        y+=1 if counter%2 and not land else 0

        if canputp(x+dx,y,m,t,tetris):
            put(x+dx,y,m,t,tetris)
            x=x+dx
            if land:
                if not canputp(x,y+1,m,t,tetris):
                    lend=True
                else:
                    land=False
        else:
            m=savem
            if canputp(x,y,m,t,tetris):
                put(x,y,m,t,tetris)
            else:
                x=savex
                y=savey
                put(x,y,m,t,tetris)
                land=True
                st.sleep(wait)
                a1,b1,pat1=getpat(m,t,tetris)
                a2,b2,pat2=getpat(savem,t,tetris)
                if land and len(pat1)<len(pat2):
                    land=False
                    lend=False
                continue

        a1,b1,pat1=getpat(m,t,tetris)
        a2,b2,pat2=getpat(savem,t,tetris)
        if land and len(pat1)<len(pat2):
            land=False
            lend=False

        if lend:
            l=linecheck()
            number_of_lines+=l
            score+=2**l*100
            (x,y,m,t)=place_tetris(tetris)
            land=False
            lend=False
            gameover=x==-1

        if gameover:
            st.locate(17,12)
            st.color((255,0,0))
            st.putstr("GAMEOVER")
            st.color((0,0,255))
            st.bgcolor((0,255,0))
            st.locate(14,14)
            st.putstr("\'q\'key to quit")
            st.bgcolor((0,0,0))
            st.refresh()
            while(st.getkey('q')==0):
                st.sleep(0.1)
            return

        score+=1
        st.locate(0,0)
        st.color((0,255,0))
        st.putstr("SCORE:")
        st.color((255,255,255))
        st.putstr(str(score))
        st.color((255,255,0))
        st.locate(0,1)
        st.putstr("TETRIS:"+str(number_of_tetris))
        st.locate(0,2)
        st.color((0,255,255))
        st.putstr("LINES: ")
        st.color((255,255,255))
        st.putstr(str(number_of_lines))
        st.refresh()
        wait=difficulty(number_of_tetris)
        if st.getkey('2'):
            wait=0.05
        st.sleep(wait)
        

if __name__=='__main__':
    main()
    exit(0)
