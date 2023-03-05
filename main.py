import pygame, sys, random, time, math
from pygame.locals import *
from timeit import default_timer as timer


#trying to make a graphic background for asteroid sim
class init_window:

    def __init__(self):
        print("initializing")
        self.runProgram = True
        self.file = "mario.PNG"
        self.prticle_pixel = pygame.image.load("kalman_dot.png")
        self. y = 1
        self.white =(255,255,255)
        self.black =(0,0,0)
        self.asteroid =pygame.image.load("asteroid.PNG") #asteroid size is 21x21 pixels

        #starting location of kalman dots
        self.x_KalDot = 136
        self.y_KalDot = 388
        #starting location of asteroids
        self.x_Asteroid0 = 150
        self.y_Asteroid0 = 250

        #kalman stuff
        self.kalman_prtcles =[[223,5]] # 8 particles
        self.state_Mtrx = [0, 0, 0, 0 ]#x,Vx, y, Vy
        self.motion_sig = 2
        self.measur_sig = 4
        self.muX = 0         #mu is a function of either x or y
        self.sigX = 10    #sig is a function of x or y
        self.muY = 0  # mu is a function of either x or y
        self.sigY = 10  # sig is a function of x or y


        self.drawFlag = 0
        #mouse
        self.offset = [0,0]
        self.mouseSpeedX = 0
        self.mouseSpeedY = 0
        self.displacement = 0
        self.xDiff = 0
        self.yDiff = 0

        #load image
        self.screen = pygame.display.set_mode((1240,720))





    ################################################
    #Input: surface is a pygame object that is used to output graphics.
    # loc is for mouse [x,y] coordinates
    # rot is used for mouse
    #draws objects to screen. Also maintains 60 FPS
    def draw_asteroid(self,rot,loc):
        self.screen.fill(self.white) #draw background
        # draws mouse cursor below####
        self.screen.blit(pygame.transform.rotate(self.asteroid, rot),(loc[0] + self.offset[0], loc[1] + self.offset[1]) )

        #ensure 60 fps
        start = timer()
        #print("start time", start)
        end = timer()
        dif = end - start
        while dif < (1/60):
            end = timer()
            dif = end-start
        #why do my random seeds need to be after my while statement!
        #seeds for random numbers
        start = 25
        stop = 57
        #self.draw_tracking_dots()



    # x, and y are the kalman dot coordinates
    def draw_tracking_dot(self,dot_x,dot_y,):
        for i in range(len(self.kalman_prtcles)):  # Draw particles
            print("running loop", i)
            self.kalman_prtcles[i][0] = dot_x
            # print("kal X", self.kalman_prtcles[i][0])
            self.kalman_prtcles[i][1] = dot_y
            # print("kal y", self.kalman_prtcles[i][1])
            # Draw tracking dot
            self.screen.blit(self.prticle_pixel, ( self.kalman_prtcles[0][0], self.kalman_prtcles[0][1]))

    #################  kalman  #########################
    def update(self, mean1, var1, mean2, var2):
        new_mean = float(var2 * mean1 + var1 * mean2) / (var1 + var2)
        new_var = 1./(1./var1 + 1./var2)
        return [new_mean, new_var]

    def predict(self, mean1, var1, mean2, var2):
        new_mean = mean1 + mean2
        new_var = var1 + var2
        return [new_mean, new_var]


    ################ pygame loop  ########################
    def run(self):
        self.drawFlag = 0
        pygame.init()
        logo = pygame.image.load(self.file)
        pygame.display.set_icon(logo)
        pygame.display.set_caption("kalman filter")

        while self.runProgram:
            for event in pygame.event.get(): #event handling
                if event.type == pygame.QUIT:
                    self.runProgram = False

            ############### mouse ##########################
            mouseX0, mouseY0 = pygame.mouse.get_pos()
            print("mouseX0, mouseY0",mouseX0, mouseY0)
            mouseT0 = timer()
            #print("mouseT0", mouseT0)
            rot = 0  # roation
            locate = [mouseX0, mouseY0]

            ########### draw screen #################
            self.draw_asteroid(rot,locate)
            pygame.display.update()
            ########### Mouse Speed ##################

            mousEndT = timer()+.3
            print("mousEndT",mousEndT)
            mouseX1, mouseY1 =pygame.mouse.get_rel()
            self.xDiff = (mouseX1 - mouseX0)/19226
            self.yDiff = (mouseY1 - mouseY0)/19226

            self.mouseSpeedX =((mouseX1-mouseX0)/ (mouseT0-mousEndT))/5
            self.mouseSpeedY = ((mouseY1 - mouseY0) / (mouseT0 - mousEndT))/5

            ############# kalman #####################
            # muX and muY are measurement update sigX and sigY are errors
            #                                     mean1,       var1,            mean2,  var2)
            [self.muX, self.sigX] = self.update(self.xDiff, self.measur_sig, self.muX, self.sigX)
            #print("muX difference ", self.muX )
            #                                     mean1,       var1,            mean2,  var2)
            [self.muX, self.sigX] = self.predict(self.muX, self.measur_sig, self.mouseSpeedX, self.motion_sig)
            print("muX predict(motion) ", self.muX)
            [self.muY, self.sigY] = self.update(self.yDiff, self.measur_sig, self.muY, self.sigY)
            [self.muY, self.sigY] = self.predict(self.muY, self.measur_sig, self.mouseSpeedY, self.motion_sig)

            ########### draw tracking dot#############
            self.draw_tracking_dot(self.muX,self.muY)


            pygame.display.update()

if __name__ == "__main__":
    window = init_window()

    window.run()