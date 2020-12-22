# Author: Shiva Verma


import turtle as t
import math


class Paddle():

    def __init__(self):

        self.done = False
        self.reward = 0
        self.hit, self.miss = 0, 0
        self.best = 0
        self.state = None
        self.motivation = 0.9

        # Setup Background

        self.win = t.Screen()
        self.win.title('Paddle')
        self.win.bgcolor('black')
        self.win.setup(width=600, height=600)
        self.win.tracer(0)

        # Paddle

        self.paddle = t.Turtle()
        self.paddle.speed(0)
        self.paddle.shape('square')
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.color('white')
        self.paddle.penup()
        self.paddle.goto(0, -275)

        # Ball

        self.ball = t.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.color('red')
        self.ball.penup()
        self.ball.goto(0, 100)
        self.ball.dx = 3
        self.ball.dy = -3

        # Score

        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 250)
        self.score.write("Hit: {}   Missed: {}   Best: {}".format(self.hit, self.miss, self.best), align='center', font=('Courier', 24, 'normal'))

        # -------------------- Keyboard control ----------------------

        self.win.listen()
        self.win.onkey(self.paddle_right, 'Right')
        self.win.onkey(self.paddle_left, 'Left')

    # Paddle movement

    def paddle_right(self):

        x = self.paddle.xcor()
        if x < 225:
            self.paddle.setx(x+20)

    def paddle_left(self):

        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x-20)

    def run_frame(self):

        self.win.update()

        # Ball moving

        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

        # Ball and Wall collision

        if self.ball.xcor() > 290:
            self.ball.setx(290)
            self.ball.dx *= -1

        if self.ball.xcor() < -290:
            self.ball.setx(-290)
            self.ball.dx *= -1

        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball.dy *= -1

        if self.ball.dx > 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) < 250:
            self.state = "move_top_right_close"
        elif self.ball.dx > 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) < 250:
            self.state = "move_bot_right_close"
        elif self.ball.dx < 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) < 250:
            self.state = "move_top_left_close"
        elif self.ball.dx < 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) < 250:
            self.state = "move_bot_left_close"
        elif self.ball.dx > 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) > 250:
            self.state = "move_top_right_far"
        elif self.ball.dx > 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) > 250:
            self.state = "move_bot_right_far"
        elif self.ball.dx < 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) > 250:
            self.state = "move_top_left_far"
        elif self.ball.dx < 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor() - self.ball.xcor()) ** 2 + (self.paddle.ycor() - self.ball.ycor()) ** 2) > 250:
            self.state = "move_bot_left_far"

        # Ball Ground contact

        if self.ball.ycor() < -290:
            self.ball.goto(0, 100)
            self.miss += 1
            if self.hit > self.best:
                self.best = self.hit
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}   Best: {}".format(self.hit, self.miss, self.best), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 100
            self.done = True
            self.state = "miss"

        # Ball Paddle collision

        if abs(self.ball.ycor() + 250) < 2 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
            self.ball.dy *= -1
            self.hit += 1
            if self.hit > self.best:
                self.best = self.hit
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}   Best: {}".format(self.hit, self.miss, self.best), align='center', font=('Courier', 24, 'normal'))
            self.reward += 7
            self.state = "hit"

    # ------------------------ AI control ------------------------

    # 0 move left
    # 1 do nothing
    # 2 move right

    def reset(self):

        self.paddle.goto(0, -275)
        self.ball.goto(0, 100)
        self.reward = 0
        self.decay = 0.03
        self.hit = 0
        if self.ball.dx > 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) < 250:
            self.state = "move_top_right_close"
        elif self.ball.dx > 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) < 250:
            self.state = "move_bot_right_close"
        elif self.ball.dx < 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) < 250:
            self.state = "move_top_left_close"
        elif self.ball.dx < 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) < 250:
            self.state = "move_bot_left_close"
        elif self.ball.dx > 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) > 250:
            self.state = "move_top_right_far"
        elif self.ball.dx > 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) > 250:
            self.state = "move_bot_right_far"
        elif self.ball.dx < 0 and self.ball.dy > 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) > 250:
            self.state = "move_top_left_far"
        elif self.ball.dx < 0 and self.ball.dy < 0 and math.sqrt((self.paddle.xcor()-self.ball.xcor())**2+(self.paddle.ycor()-self.ball.ycor())**2) > 250:
            self.state = "move_bot_left_far"
        return [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball.dx, self.ball.dy, self.state]

    def step(self, action):

        self.done = 0

        if action == 0:
            self.paddle_left()
            self.reward -= self.decay

        if action == 2:
            self.paddle_right()
            self.reward -= self.decay

        self.run_frame()

        state = [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball.dx, self.ball.dy, self.state]
        return self.reward, state, self.done, self.best


# ------------------------ Human control ------------------------
#
# env = Paddle()
#
# while True:
#      env.run_frame()
