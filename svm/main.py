import tkinter
import math

# helper point class
class Point():
  def __init__(self, type, x, y):
    self.type = type
    self.x = x
    self.y = y

def distance(p1, p2):
  r = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
  print(r)
  return r

CANVAS_HEIGHT = 500
CANVAS_WIDTH = 500

# global variables
root = tkinter.Tk()
cnv = tkinter.Canvas(root, bg="white", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
points = []
current_type = 1

# callbacks
def change_type_callback():
  global current_type
  current_type *= -1
b = tkinter.Button(root, text="Change type", command=change_type_callback)
b.pack()

def fill_callback():
  fill_region(lambda x, y: -0.01 * (x - 100)**2 + y - 50)

fill_button = tkinter.Button(root, text="Fill", command=fill_callback)
fill_button.pack()

def callback(event):
  points.append(Point(current_type, event.x, event.y))
  drawPoints()
  print("clicked at", event.x, event.y)

def delete_point_callback(event):
  global points
  currentPoint = Point(None, event.x, event.y)

  points = [p for p in points if distance(currentPoint, p) > 5]

  drawPoints()
  print("clicked delete at", event.x, event.y)

# drawing
def drawRO(x, y):
  cnv.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#ff0000", outline='')

def drawBX(x, y):
  cnv.create_line(x - 5, y - 5, x + 5, y + 5, fill="#0000ff")
  cnv.create_line(x - 5, y + 5, x + 5, y - 5, fill="#0000ff")

def drawLRO(x, y):
  cnv.create_oval(x - 2, y - 2, x + 2, y + 2, fill="#ffc5c5", outline='')

def drawLBO(x, y):
  cnv.create_oval(x - 2, y - 2, x + 2, y + 2, fill="#c5c5ff", outline='')

def fill_region(f):
  for x in range(0, CANVAS_WIDTH, 5):
    for y in range(0, CANVAS_HEIGHT, 5):
      if(f(x, y) > 0):
        drawLRO(x, y)
      else:
        drawLBO(x, y)

def drawPoints():
  cnv.delete('all')
  for p in points:
    drawRO(p.x, p.y) if p.type == -1 else drawBX(p.x, p.y)


cnv.bind("<Button-1>", callback)
cnv.bind("<Button-2>", delete_point_callback)
cnv.pack()

root.mainloop()

