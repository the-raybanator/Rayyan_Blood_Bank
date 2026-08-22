from turtle import RawTurtle, TurtleScreen
from tkinter import *
import time

def draw(sc, length, width):
    sc.title('Rayyan Blood Bank')

    canvas = Canvas(master = sc, width = length, height = width)
    canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
    screen = TurtleScreen(canvas)
    screen.register_shape('Assets/giphy.gif')
    t = RawTurtle(screen)
    b = RawTurtle(screen)
    b.shape('Assets/giphy.gif')

    t.hideturtle()

    b.penup()
    b.goto(-450, -230)
    b.lt(90)

    sc.deiconify()

    b.showturtle()
    b.speed(1)
    b.bk(100)

    fly_to(-300, 150, t)
    t.pencolor('blue')
    t.write("RAYYAN - ", font=('courier', 50, 'bold'))
    t.pencolor('red')
    fly_to(70, 175, t)
    t.write("Your gateway to", font=('courier', 40))
    fly_to(90, 110, t)
    t.write("donate blood", font=('courier', 40))
    fly_to(-100, 30, t)
    t.pencolor("blue")
    t.pensize(3)
    t.write('Give the gift of life', font=('arial', 40))
    fly_to(-70, -50, t)
    t.write("Donate blood!", font=('arial', 40))

    time.sleep(3)

    sc.withdraw()
    t.reset()
    b.reset()


def fly_to(x, y, turtle_):
    turtle_.penup()
    turtle_.goto(x, y)
    turtle_.pendown()

if __name__ == "__main__":
    length = 1500
    width = 850
    turtle_sc = Tk()
    turtle_sc.withdraw()
    turtle_sc.geometry(f"{length}x{width}+0+0")

    draw(turtle_sc, length, width)

    turtle_sc.destroy()

    turtle_sc.mainloop()
