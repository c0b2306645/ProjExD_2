import os
import random
import sys
import pygame as pg
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))


WIDTH, HEIGHT = 1200, 700
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ALFA = {#向き転換辞書
    (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0), #初期状態 
    (0, -5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), 90, 2.0), #右斜め上
    (+5, -5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), 45, 2.0), #右
    (+5, 0):  pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 0, 2.0), #右斜め下
    (+5, +5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -45, 2.0), #下
    (0, +5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), 270, 2.0), #
    (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
    (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
    (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0),
    }


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect，または，爆弾Rect
    戻り値：真理値タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def gameOver(screen):
    """
    こうかとんが爆弾に衝突した際に
    ・画面をブラックアウトする
    ・泣いているこうかとんと
    ・「Game Over」の文字列を表示する
    ・表示時間は５秒間
    """

    black_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black_img,(0,0,0), pg.Rect(0,0,WIDTH, HEIGHT))
    black_img.set_alpha(200)
    black_rct = black_img.get_rect()
    screen.blit(black_img,black_rct)
    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game Over",True,(255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center=WIDTH/2, HEIGHT/2
    # block = pg.Surface((WIDTH,HEIGHT))
    # block_rct = block.get_rect()
    # screen.blit(block, block_rct)
    screen.blit(txt,txt_rct)
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH/2-250, HEIGHT/2
    screen.blit(kk_img,kk_rct)
    kk_rct.center = WIDTH/2+250, HEIGHT/2
    screen.blit(kk_img,kk_rct)
    pg.display.update()
    time.sleep(5)
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 1辺が20の空のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の横方向速度，縦方向速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            gameOver(screen)
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        dx = ALFA[tuple(sum_mv)]
        screen.blit(dx, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()