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
        self.kalman_prtcles =[[223,5],[227,167],[268,6],[282,267],[303,36],[199,456],[235,526],[262,236]] # 8 particles
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


    def draw_tracking_dots(self, xCoord, yCoord, rot, loc):
        #self.screen.fill(self.white)  # draw background
        # draws mouse cursor below####
        #self.screen.blit(pygame.transform.rotate(self.asteroid, rot),
        #                 (loc[0] + self.offset[0], loc[1] + self.offset[1]))
        for i in range(len(self.kalman_prtcles)): #Draw particles
            self.kalman_prtcles[i][0] = xCoord  #random.randint(x+25, x+25) #[i][j0][j1]
            #print("kal X", self.kalman_prtcles[i][0])
            self.kalman_prtcles[i][1] = yCoord#random.randint(y+25, y+25)
            #print("kal y", self.kalman_prtcles[i][1])
            self.screen.blit(self.prticle_pixel,(self.kalman_prtcles[i][0],self.kalman_prtcles[i][1]))
            #print("drawing ", i)
            #    self.kalman_prtcles[x][y] = random.randint(1, 21)

    ################################################
    #Input: surface is a pygame object that is used to output graphics. x,y,
    # x, and y are the kalman dot coordinates
    # loc is for mouse [x,y] coordinates
    # rot is used for mouse
    #draws objects to screen. Also maintains 60 FPS

    def draw(self,surface,x,y,rot,loc):
        self.screen.fill(self.white) #draw background
        # draws mouse cursor below####
        self.screen.blit(pygame.transform.rotate(self.asteroid, rot),(loc[0] + self.offset[0], loc[1] + self.offset[1]) )#

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
        if self.drawFlag ==1:
            for i in range(len(self.kalman_prtcles)):  # Draw particles
                self.kalman_prtcles[i][0] = x  # random.randint(x+25, x+25) #[i][j0][j1]
                # print("kal X", self.kalman_prtcles[i][0])
                self.kalman_prtcles[i][1] = y  # random.randint(y+25, y+25)
                # print("kal y", self.kalman_prtcles[i][1])
                self.screen.blit(self.prticle_pixel, (self.kalman_prtcles[i][0], self.kalman_prtcles[i][1]))


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
        pygame.display.set_caption("Cs7638 kalman filter")

        while self.runProgram:
            #event handling
            for event in pygame.event.get():
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
            self.draw(self.screen,self.muX,self.muX,rot,locate)
            self.drawFlag = 1
            pygame.display.update()
            ########### Mouse Speed ##################

            mousEndT = timer()+.3
            print("mousEndT",mousEndT)
            mouseX1, mouseY1 =pygame.mouse.get_rel()
            #print("mouseX1, mouseY1", mouseX1, mouseY1)
            #print("mousEndT", mousEndT)

            #self.mouseSpeed =(( (mouseX1-mouseX0 )**2 + (mouseY1- mouseY0 )**2 )**(1/2))/(mouseT0-mousEndT) #distance formula
            self.xDiff = (mouseX1 - mouseX0)/19226
            self.yDiff = (mouseY1 - mouseY0)/19226

            self.mouseSpeedX =((mouseX1-mouseX0)/ (mouseT0-mousEndT))/5
            print("self.mouseSpeedX ",self.mouseSpeedX )
            self.mouseSpeedY = ((mouseY1 - mouseY0) / (mouseT0 - mousEndT))/5
            #print(" self.mouseSpeedX ", self.mouseSpeedX   )
            ############# kalman #####################

            #self.state_Mtrx = [self.displacement,self.measur_sig,self.muX ,self.sigX]
            #self.state_Mtrx = [mouseX1,self.mouseSpeedX,mouseY1,self.mouseSpeedY]  #using the most recent mouse speed

            [self.muX, self.sigX] = self.update(self.xDiff, self.measur_sig, self.muX, self.sigX)
            print("muX difference ", self.muX )
            [self.muX, self.sigX] = self.predict(self.muX, self.measur_sig, self.mouseSpeedX, self.motion_sig)
            print("muX predict(motion) ", self.muX)
            [self.muY, self.sigY] = self.update(self.yDiff, self.measur_sig, self.muY, self.sigY)
            [self.muY, self.sigY] = self.predict(self.muY, self.measur_sig, self.mouseSpeedY, self.motion_sig)
            #[mu, sig] = predict(mu, sig, motion[x], motion_sig)
            #print [mu, sig]



            #print("self.muX, self.sigX", self.muX, self.sigX)
            self.draw(self.screen, self.muX, self.muY, rot, locate)
            #self.draw_tracking_dots(self.muX,self.muX,rot,locate)
            #muX and muY are measurement update sigX and sigY are errors
            pygame.display.update()

if __name__ == "__main__":
    window = init_window()

    window.run()