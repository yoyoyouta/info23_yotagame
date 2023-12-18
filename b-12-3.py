import pyxel

class Ball:
    speed = 1

    def __init__(self):
        self.restart()

    def move(self):
        self.x += self.vx * Ball.speed
        self.y += self.vy * Ball.speed
        if (self.x < 0) or (self.x >= field_size):
            self.vx = -self.vx

    def restart(self):
        self.x = pyxel.rndi(0, field_size - 1)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

class Pad:
    def __init__(self):
        self.size = field_size / 5
        self.x = field_size / 2

    def catch(self, ball):
        if ball.y >= field_size-field_size/40 and (self.x-self.size/2 <= ball.x <= self.x+self.size/2):
            pyxel.play(0, 0)
            ball.restart()
            return True
        else:
            return False

field_size = 150

pyxel.init(field_size, field_size)
pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
pyxel.sound(1).set(notes='C2', tones='N', volumes='3', effects='S', speed=30)

# classを書いたら必要
balls = [Ball()]
pad = Pad()

alive = True
life = 10
receive = 0
pad.x = field_size / 2
score = 0

def update():
    global balls, padx, score, alive, life, receive
    if not alive:
        return
    pad.x = pyxel.mouse_x
    for b in balls:
        b.move()
        if pad.catch(b):
            pyxel.play(0, 0)
            score += 1
            Ball.speed += 0.2
            b.restart()
            receive += 1
            if receive >= 10:
                Ball.speed = 1
                receive = 0
                balls.append(Ball())

        elif b.y >= field_size:
            pyxel.play(0,1)
            Ball.speed += 0.2
            b.restart()
            life -= 1
            alive = (life > 0)

def draw():
    global balls, padx, score, alive
    if alive:
        pyxel.cls(7)
        for b in balls:
            pyxel.circ(b.x, b.y, field_size/20, 6)
        pyxel.rect(pad.x-pad.size/2, field_size-field_size/40, pad.size, 5, 14)
        pyxel.text(5, 5, "score:" + str(score), 0)
    else:
        pyxel.text(field_size/2-20, field_size/2-20, "Game Over!!!", 0)

pyxel.run(update, draw)