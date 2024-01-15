import pyxel
import random

class App():
    game_end = False
    missed = 0

    def __init__(self):
        # 変数の定義や初期設定
        pyxel.init(200, 200)
        self.player = Player()
        self.enemies = []
        self.line = []
        self.time = 0
        self.sec = 20
        self.screen = Screen()

       # BGMの設定 chay gpt 使用
        pyxel.sound(1).set("a3e2c2e2g2e2c2e2a2", "s", "7", "n", 25)
        pyxel.play(1, [1], loop=True)

        # いつもの
        pyxel.run(self.update, self.draw)

    def update(self):
        # クリアもしくはゲームオーバー状態ならば何も処理しない
        if App.game_end:
            return
        
        self.player.update()
        
        
        for i in reversed(range(len(self.enemies))):
            if not self.enemies[i].update():
                del self.enemies[i]
        for i in reversed(range(len(self.line))):
            if not self.line[i].update():
                del self.line[i]
        
        # 10秒経過までは20フレームごとに敵のインスタンスを追加
        if pyxel.frame_count <= 300 and pyxel.frame_count % 20 == 0:
                self.enemies.append(Enemy())
        # 20秒経過からゲーム終了までは15フレームごとに敵のインスタンスを追加
        elif pyxel.frame_count > 300 and pyxel.frame_count % 15 == 0:
                self.enemies.append(Enemy())

        # 当たり判定の処理
        for i in range(len(self.enemies)-1, -1, -1):
            # ボールが敵に当たった場合、敵のインスタンスを削除しミスカウントを1増やす
            if self.player.hit(self.enemies[i]):
                del self.enemies[i]
                App.missed += 1
                # ミスカウントが3に達した場合はゲームオーバー
                if App.missed == 3:
                    self.screen = Gameover()
                    App.game_end = True
        
        # 600フレーム(20秒)間耐えられたらゲームクリア
        if pyxel.frame_count == 600:
            self.screen = Gameclear()
            App.game_end = True
        
        # 時間のカウントダウン処理
        self.time = pyxel.frame_count // 30
        self.sec = 20 - self.time

    def draw(self):
        # ゲームクリア・ゲームオーバーならそれに対応する静的な画面を表示する
        if App.game_end:
            self.screen.draw()
            return

        # ゲーム中であれば以下の描画を行う
        else:
            # 背景
            pyxel.cls(0)
            
            # 敵
            for b in self.enemies:
                b.draw()
            # ボール
            self.player.draw()
            # 残り時間・残りライフ
            self.screen.draw(self.sec, self.missed)


# ボールの描画を行うクラス
class ball:
    def __init__(self):
        pass
    
    # 四角と丸を組み合わせて車を描画する
    def draw(self, x, y, c):
            pyxel.circ(x , y, 10, 10)
       


# ゲームオーバー画面を描画するクラス
class Gameover:
    def __init__(self):
        self.ball = ball()
    
    # ゲームオーバーの文言とともに、ボールを表示
    def draw(self):
        pyxel.rect(0, 0, 200, 200, 0)
        pyxel.text(80,80,"Game Over !!",8)
        self.ball.draw(100, 100, 2)


# ゲームクリア画面を描画するクラス
class Gameclear:
    def __init__(self):
        self.ball = ball()

    # ゲームクリアの文言とともに、ボールを1個表示する
    def draw(self):
        pyxel.rect(0, 0, 200, 200, 7)
        pyxel.text(80,80,"Game Clear !!",9)
        self.ball.draw(91, 90, 8)


# 文字を表示するフレームを描画するクラス
class Frame:
    def __init__(self):
        pass
    
    # 描画する位置と文字を引数に取って、フレームの描画を行う
    def draw(self, x, y, message):
        pyxel.rect(x, y, 32, 12, 7)
        pyxel.line(x, y, x+32, y, 12)
        pyxel.line(x, y, x, y+12, 12)
        pyxel.line(x+32, y+12, x+32, y, 12)
        pyxel.line(x+32, y+12, x, y+12, 12)
        pyxel.text(x+2, y+4, message, 14)


# 文字を表示するクラス
class Screen:
    def __init__(self):
        self.point = Frame()
        self.life = Frame()
    
    # 残り時間とミスカウントを引数に取り、残り時間と残りライフを表示する
    def draw(self, sec, miss):
        self.point.draw(8, 6, 'TIME:'+str(sec))
        self.life.draw(48, 6, 'LIFE:'+str(3-miss))


# ボールの処理を行うクラス
class Player:
    def __init__(self):
        self.x = 56
        self.y = 88
        self.c = 8
        self.speed = 3
        self.car = ball()

    def update(self):
        # キーボードの↑ボタンを押したらボールを上に移動する
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        
        # キーボードの↓ボタンを押したらボールを下に移動する
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        
        # ボールが上下の境界線を乗り越えないようにする
        if self.y < 25:
            self.y = 25
        elif self.y > 178:
            self.y = 178
    
    # 敵との当たり判定の処理
    # 当たったらTrue, そうでなかったらFalseを返す
    def hit(self, enemies):
        if (self.x + 24 >= enemies.x - 6) and (self.x - 6 <= enemies.x + 24):
            if (self.y <= enemies.y + 22) and (self.y + 22 >= enemies.y):
                return True
        else:
            return False
    
    # 描画
    def draw(self):
        self.car.draw(self.x, self.y, self.c)


# 敵の処理を行うクラス
class Enemy:
    #ランダムな色で出現させる
    def __init__(self):
        self.x = 200
        self.y = random.randrange(29, 200, 35)
        self.c = random.randint(1, 4)
        self.speed = 5
        self.ball = ball()
        
    def update(self):
        # 左に進ませ続ける
        self.x -= self.speed

        # 画面外に出たらインスタンス削除のためにFalseを返す
        if self.x < 0:
            return False
        else:
            return True
    
    # 描画
    def draw(self):
        self.ball.draw(self.x, self.y, self.c)

App()
