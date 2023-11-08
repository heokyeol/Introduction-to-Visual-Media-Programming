import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800


def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("assets/diyong.mp3")
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 150
    h = 20
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    gw = 50
    gh = 10
    Y = np.array([ [0,0], [gw, 0], [gw, gh], [0, gh] ])
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]
    jointangle1 = 10
    jointangle2 = -30

    ang1 = 0
    ang2 = 0
    ang3 = 0
    ang4 = 0
    grip = False
    gripAng = 0
    
    
    tick = 0
    done = False
    while not done:
        tick += 1
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grip = not grip
        if grip == False :
            if gripAng > 0 :
                gripAng -= 1
        elif grip == True :
            if gripAng< 90 :
                gripAng += 1
            
        key_1 = pygame.key.get_pressed()
        key_2 = pygame.key.get_pressed()
        if key_1[pygame.K_1]:
            ang4 -= 2
        elif key_2[pygame.K_2]:
            ang4 += 2

        key_q = pygame.key.get_pressed()
        key_w = pygame.key.get_pressed()
        if key_q[pygame.K_q]:
            ang3 -= 2
        elif key_w[pygame.K_w]:
            ang3 += 2

        key_a = pygame.key.get_pressed()
        key_s = pygame.key.get_pressed()
        if key_a[pygame.K_a]:
            ang2 -= 1
        elif key_s[pygame.K_s]:
            ang2 += 1
        
        key_z = pygame.key.get_pressed()
        key_x = pygame.key.get_pressed()
        if key_z[pygame.K_z]:
            ang1 -= 0.5
        elif key_x[pygame.K_x]:
            ang1 += 0.5


        # drawing
        screen.fill( (200, 254, 219))

        # base
        pygame.draw.circle(screen, (255,0,0), position, radius=3)
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(X, H0, screen, (0,0,0)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)  
        x, y = H1[0,2], H1[1,2] # joint position
        H11 = H1 @ Rmat(-90) @ Tmat(0,-h/2)
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H12 = H11 @ Tmat(0, h/2) @ Rmat(ang1) @ Tmat(0, -h/2)    
        draw(X, H12, screen, (200,200,0)) # arm 1, 90 degree

        # arm 2
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H21 = H2 @ Rmat(ang2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0,0, 200))

        #arm3
        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2)
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3)
        H31 = H3 @ Rmat(ang3) @ Tmat(0, -h/2)
        draw(X, H31, screen, (0, 200, 0))

        #gripper
        H4 = H31 @ Tmat(w, 0) @ Tmat(0, h/2)
        x, y = H4[0,2], H4[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3)

        H411 = H4 @ Rmat(-30 - gripAng + ang4) @ Tmat(0, -gh/2)
        draw(Y, H411, screen, (0, 0, 0))
        H412 = H411 @ Tmat(gw, gh/2) @ Rmat(60) @Tmat(0, -gh/2)
        draw(Y, H412, screen, (0, 0, 0))

        H421 = H4 @ Rmat(30 + gripAng + ang4) @ Tmat(0, -gh/2)
        draw(Y, H421, screen, (0, 0, 0))
        H422 = H421 @ Tmat(gw, gh/2)@ Rmat(-60)  @Tmat(0, -gh/2)
        draw(Y, H422, screen, (0, 0, 0))

    
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()