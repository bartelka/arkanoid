import random

def destroy_brick():
    global movement
    coord_ball = canvas.coords(ball)
    items_list = canvas.find_overlapping(coord_ball[0],coord_ball[1],coord_ball[2],coord_ball[3])
    for i in items_list:
        if i in bricks:
            coord_brick = canvas.coords(i)
            if coord_brick[0] == coord_ball[2]:
                bricks.remove(i)
                canvas.delete(i)
                movement[0] *= (-1)
            if coord_brick[2] == coord_ball[0]:
                bricks.remove(i)
                canvas.delete(i)
                movement[0] *= (-1)
            if coord_brick[3] == coord_ball[1]:
                bricks.remove(i)
                canvas.delete(i)
                movement[1] *= -1
            if coord_brick[1] == coord_ball[3]:
                bricks.remove(i)
                canvas.delete(i)
                movement[1] *= -1

def desk_hit(cd, cb):
    desk_middle = (cd[2]-cd[0])/2 + cd[0]
    if cb[2] <= desk_middle:
        return [-d,-d]
    elif desk_middle <= cb[0]:
        return [d,-d]
    elif cb[0] < desk_middle and desk_middle< cb[2]:
        return [0,-d]
    # list = [-1,0,1]
    # return [random.choice(list),-1]

def ball_move():
    global movement
    canvas.move(ball,movement[0],movement[1])
    coord_ball = canvas.coords(ball)
    coord_desk = canvas.coords(desk)
    destroy_brick()
    if ball in canvas.find_overlapping(coord_desk[0],coord_desk[1],coord_desk[2],coord_desk[3]):
        movement = desk_hit(coord_desk,coord_ball)
    if coord_ball[0] < 0: #horny pravy roh x, lava strana
        movement[0] *= (-1)
        canvas.itemconfig(ball,fill="black")
        canvas.configure(bg="white")
    if coord_ball[1] < 0: #horny pravy roh y, horna strana
        movement[1] *= (-1)
    if coord_ball[2] > w: #dolny lavy roh x, prava srana
        movement[0] *= (-1)
        canvas.itemconfig(ball,fill="white")
        canvas.configure(bg="black")
    if coord_ball[3] > h: #dolny lavy roh y, dolna strana
        canvas.configure(bg="black")
        canvas.delete("all")
        text = canvas.create_text(w/2,h/2, text="PREHRAL SI!", fill="white", font="Arial 20")
    if len(bricks) == 0:
        canvas.configure(bg="black")
        canvas.delete("all")
        text = canvas.create_text(w/2,h/2, text="VYHRAL SI!\nčas:"+str(ftime//count_click), fill="white", font="Arial 20")
        status = False
    canvas.after(35, ball_move)

def mover(e):
    global x
    if x != 0:
        mouse = e.x - x
        canvas.move(desk, mouse, 0)
        x = e.x

def starter(e):
    global x,count_click
    canvas.delete(text)
    zoz = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
    if desk in zoz:
        x = e.x
        ball_move()
        timer()
        count_click += 1
def timer():
    global ftime
    ftime += 1
    canvas.itemconfig(t, text=ftime)
    if status == True:
        canvas.after(1000, timer)


def prepare_bricks():
    for y in range(brick_count_y):
        for x in range(w//brick_w):
            bricks.append(canvas.create_rectangle(x*brick_w,y*brick_h,x*brick_w+brick_w, y*brick_h+brick_h, fill=colours[y%brick_count_y],  width=5, outline="black"))

colours = ["purple", "dark magenta", "orchid","violet", "plum", "white"]

import tkinter as tk

win = tk.Tk()

#width, height
w = 650
h = 450

canvas = tk.Canvas(width = w, height = h, bg = "black")
canvas.pack()

d=5
movement = [1*d,1*d]

status = True
ftime = 0
t = canvas.create_text(w/5*4,h/5*4, text=ftime, fill="orchid", font="Arial 30")
count_click = 0

brick_w = 65
brick_h = 20
brick_count_x = 10
brick_count_y = len(colours)
bricks = []

ball = canvas.create_oval(w/2-20,h/2-20,w/2,h/2, fill="white")
text = canvas.create_text(w/2,h/2+30,text="ZAČNI HRAŤ!", fill="white", font="Arial 20")
desk = canvas.create_rectangle(w/2-50, h-20, w/2+50, h, fill="purple")

prepare_bricks()

canvas.bind("<Button-1>", starter)
canvas.bind("<B1-Motion>", mover)


win.mainloop()
