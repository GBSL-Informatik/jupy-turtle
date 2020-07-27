# Version 0.2 (in progress)
from IPython.core.display import display
from IPython.core.display import HTML
from IPython.core.display import Javascript
from js_executor import JsExecutor
import time
import math
import random

JsExecutor.configure('./javascript')


class Vec2D:
    x: float = 0
    y: float = 0

    def __init__(self, xVal, yVal):
        self.x = xVal
        self.y = yVal

    def __neg__(self):
        return Vec2D(-self.x, -self.y)

    def __add__(self, other):
        if type(other) != Vec2D:
            raise TypeError(
                "unsupported operand type(s) for +: 'Vec2D'  and '" + type(other).__name__ + "'")
        xNew = self.x + other.x
        yNew = self.y + other.y
        return Vec2D(xNew, yNew)

    def __sub__(self, other):
        xNew = self.x + other.x
        yNew = self.y + other.y
        return Vec2D(xNew, yNew)

    def __mul__(self, other):
        if not (isinstance(other, int) or isinstance(other, float) or isinstance(other, Vec2D)):
            raise TypeError(
                "unsupported operand type(s) for *: 'Vec2D'  and '" + type(other).__name__ + "'")

        if type(other) == Vec2D:
            return self.x * other.x + self.y * other.y
        return Vec2D(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ";" + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Vec2D(self.x, self.y)

    def norm(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        n = self.norm()
        return Vec2D(self.x / n, self.y / n)

    def rotate(self, angle, counterclockwise=True):
        n = self.normalized()
        angleRad = math.radians((1 if counterclockwise else -1) * angle)
        cos = math.cos(angleRad)
        sin = math.sin(angleRad)

        vX = Vec2D(cos, -sin)
        vY = Vec2D(sin, cos)
        return Vec2D(n * vX, n * vY) * self.norm()

    @staticmethod
    def sign(num, zero=1):
        if num > 0:
            return 1
        elif num < 0:
            return -1
        return zero

    def absRotation(self, counterclockwise=True, relTo=None) -> float:
        toRotation = 0 if relTo is None else relTo.absRotation(None)

        rot = math.degrees(math.acos(self.normalized().y))
        rot = (360 - Vec2D.sign(self.x) * rot) % 360

        if counterclockwise:
            return (rot - toRotation) % 360
        else:
            return (toRotation - rot) % 360


class Canvas:
    # class variable to get the next available id
    _id: int = 0

    width: int = 600
    height: int = 600
    id: str
    origin: Vec2D
    htmlCanvasCreated: bool = False

    def __init__(self, width=600, height=600, origin=None):
        self.width = width
        self.height = height
        self.id = f'canvas{Canvas.nextId()}'
        if origin is None:
            self.origin = Vec2D(width / 2, height / 2)
        else:
            self.origin = origin.copy()
        # self.display()

    def transform(self, vec2d) -> Vec2D:
        if not isinstance(vec2d, Vec2D):
            return None
        return Vec2D(vec2d.x + self.origin.x, self.origin.y - vec2d.y)

    @classmethod
    def nextId(cls) -> int:
        cls._id += 1
        return cls._id - 1

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.__str__()

    def htmlCanvas(self) -> HTML:
        htmlCode = f'''
            <canvas id="{self.id}" width="{self.width}" height="{self.height}" style="border: 1px solid black; margin: 0; padding: 0;"></canvas>
        '''
        return HTML(htmlCode)

    def display(self):
        if self.htmlCanvasCreated:
            return

        self.htmlCanvasCreated = True
        display(self.htmlCanvas())


class Turtle:
    pos: Vec2D = Vec2D(0, 0)
    direction: Vec2D = Vec2D(0, 1)
    delay: float = 0.1
    lineWidth: int = 1
    strokeStyle: str = 'blue'
    fillStyle: str = 'cyan'  # "#00000000" transparent (alpha channel 0)
    canvas: Canvas

    def __init__(self, canvas=None):
        if canvas is None:
            self.canvas = Canvas(600, 600, Vec2D(300, 300))
        else:
            self.canvas = canvas
        self.canvas.display()
        self.canvas.display()

    def heading(self) -> float:
        return self.direction.absRotation()

    def position(self) -> Vec2D:
        return self.pos.copy()

    def rotate(self, angle, counterclockwise=True):
        self.direction = self.direction.rotate(angle, counterclockwise)

    def canvasPos(self) -> Vec2D:
        return self.canvas.transform(self.pos)

    def home(self):
        self.pos = Vec2D(0, 0)
        self.direction = Vec2D(0, 1)
        JsExecutor.call('moveTurtleTo', self.canvas.id,
                        turtle.canvasPos().x, turtle.canvasPos().y)

    def forward(self, distance):
        self.pos += self.direction * distance

        JsExecutor.call('lineTo', self.canvas.id,
                        self.canvasPos().x, self.canvasPos().y)
        time.sleep(self.delay)

    def back(self, distance):
        self.forward(-distance)

    def right(self, angle):
        self.left(-angle)

    def left(self, angle):
        self.rotate(angle)

    def dot(self, diameter):
        JsExecutor.call('dot', self.canvas.id, self.canvasPos().x,
                        self.canvasPos().y, diameter)
        time.sleep(self.delay)

    def arc(self, radius, angle, counterclockwise=True):
        toCenter = self.direction.rotate(90, counterclockwise) * radius
        fromCenter = -toCenter
        center = self.pos + toCenter

        startAngle = fromCenter.absRotation(False, Vec2D(-1, 0))
        rotDirection = -1 if counterclockwise else 1
        endAngle = startAngle + rotDirection * angle

        JsExecutor.call('arc', self.canvas.id, self.canvas.transform(center).x, self.canvas.transform(
            center).y, radius, math.radians(startAngle), math.radians(endAngle), counterclockwise)

        self.rotate(angle, counterclockwise)
        self.pos = center + fromCenter.rotate(angle, counterclockwise)

    def leftArc(self, radius, angle):
        self.arc(radius, angle, True)

    def rightArc(self, radius, angle):
        self.arc(radius, angle, False)

    def setPos(self, x, y):
        self.pos = Vec2D(x, y)
        JsExecutor.call('moveTurtleTo', self.canvas.id,
                        self.canvasPos().x, self.canvasPos().y)

    def setColor(self, strokeStyle):
        pass

    def setPenColor(self, strokeStyle):
        self.strokeStyle = strokeStyle
        JsExecutor.call('setPenColor', self.canvas.id,
                        strokeStyle, self.canvasPos().x, self.canvasPos().y)

    def setFillColor(self, fillStyle):
        self.fillStyle = fillStyle
        JsExecutor.call('setFillColor', self.canvas.id, fillStyle)

    def setPenWidth(self, lineWidth):
        self.lineWidth = lineWidth
        JsExecutor.call('setPenWidth', self.canvas.id, lineWidth)

    def hideTurtle(self):
        pass

    def fill(self):
        JsExecutor.call('floodFill', self.canvas.id)

    def startPath(self):
        JsExecutor.call('startPath', self.canvas.id)

    def fillPath(self):
        JsExecutor.call('fillPath', self.canvas.id)


turtle: Turtle = None


def home():
    global turtle
    turtle.home()


def makeTurtle() -> Turtle:
    global turtle
    turtle = Turtle()

    JsExecutor.call('makeTurtle', turtle.canvas.id, turtle.lineWidth,
                    turtle.strokeStyle, turtle.fillStyle)
    turtle.home()
    return turtle


def forward(distance):
    global turtle
    turtle.forward(distance)


def back(distance):
    forward(-distance)


def right(angle):
    left(-angle)


def left(angle):
    global turtle
    turtle.rotate(angle)


def dot(diameter):
    global turtle
    turtle.dot(diameter)


def arc(radius, angle, counterclockwise=True):
    global turtle
    turtle.arc(radius, angle, counterclockwise)


def leftArc(radius, angle):
    arc(radius, angle, True)


def rightArc(radius, angle):
    arc(radius, angle, False)


def setPos(x, y):
    global turtle
    turtle.setPos(x, y)


def setColor(strokeStyle):
    pass


def setPenColor(strokeStyle):
    global turtle
    turtle.setPenColor(strokeStyle)


def setFillColor(fillStyle):
    global turtle
    turtle.setFillColor(fillStyle)


def setPenWidth(lineWidth):
    global turtle
    turtle.setPenWidth(lineWidth)


def hideTurtle():
    pass


def fill():
    global turtle
    turtle.fill()


def startPath():
    global turtle
    turtle.startPath()


def fillPath():
    global turtle
    turtle.fillPath()
