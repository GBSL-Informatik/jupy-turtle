# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from gturtle import *

t = makeTurtle()
home()

left(30)
forward(50)
rightArc(50, 90)
forward(50)
rightArc(50, 90)
forward(50)
rightArc(50, 90)
forward(50)
rightArc(50, 90)
forward(50)
setPenColor('red')

left(30)
leftArc(20, 90)
forward(20)
leftArc(20, 90)
dot(5)
forward(20)
leftArc(20, 90)
forward(20)
leftArc(20, 90)
forward(20)
dot(5)
forward(40)
dot(15)

t2 = Turtle(t.canvas)

t2.setPenColor('yellow')
t2.setFillColor('yellow')
t2.forward(50)
t2.dot(30)


t3 = Turtle(Canvas(200, 200))
t3.right(90)
t3.setPenColor('yellow')
t3.setFillColor('yellow')
t3.forward(50)
t3.dot(30)
