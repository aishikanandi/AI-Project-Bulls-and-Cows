#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygame import *
import numpy.random as rd

class Mastermind(object):

    def __init__(self, human = False):
        self.human = human
        if human:
            self._build_mastermind()
        
        #This list will contain the int representation of combination
        #Each combination [x,y,z,t] is represented by an int between 0 and 1295
        self.list_action = self.create_list_action()
        
        #The current combination
        self.combi = []

    def _build_mastermind(self):
        #Build a graphic Mastermind game
        self.screen = display.set_mode((400,550))
        display.set_caption('MasterMind')

        self.mmbg    = image.load('MMbg2.jpg')
        self.palette = image.load('Palette3.png')
        self.myst    = image.load('myst.png')

        self.palet_rect = Rect(20,440,300,30)
        self.go_rect    = Rect(20,475,240,30)
        self.reset_rect = Rect(20,510,240,30)

        self.palet_mask = mask.from_surface(self.palette)

        self.combi = []
        self.ready = False

        self.screen.blit(self.mmbg,(0,0))
        self.screen.blit(self.palette,self.palet_rect)
        display.flip()
        

    def reset(self):
        #reset the environement
        if self.human:
            self.screen.blit(self.mmbg,(0,0))
            self.screen.blit(self.palette, self.palet_rect)
            self.ready = False
            display.flip()
        
        self.combi = []
        return('init')
    
    def create_list_action(self):
        #For a tissue to wipe your bleeding eyes, please come to my room: Fayolle building 11.30.31
        #Joke aside, this function compute the int representation of each combination
        res = dict()
        num = 0
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    for l in range(9):
                        res[num] = [i,j,k,l]
                        num = num + 1
        return res
        
    def human_agent(self):
        
        while (len(self.combi) < 4):
            ev = event.wait()
            
            if ev.type == MOUSEBUTTONUP:
                
                if self.palet_rect.collidepoint(ev.pos):
                    x,y = ev.pos
                    x -= self.palet_rect.x
                    y -= self.palet_rect.y
                    if self.palet_mask.get_at((x,y)):
                        self.combi.append(x//30)
                        self.scr.blit(self.palette,(80+(len(self.combi)-1)*30,20),(x//30*30,0,30,30))
                        display.flip()
                        
                if self.reset_rect.collidepoint(ev.pos):
                    self.reset()      


    def step(self, action, line):
        #This method is pretty complex due to the possibility to generate a game: computer agent vs human
        #In a first reading we recommend to skip the part starting with "if self.human"
        #These conditions are here solely for the graphical mode
        
        if self.human:
            if len(self.combi) == 0:
                self.human_agent()
                
            while (self.ready != True):
                ev = event.wait()
                if ev.type == MOUSEBUTTONUP:
                    if self.go_rect.collidepoint(ev.pos):
                        self.ready=True
        
        #Compute a random combination at the beginning of the game if the computer is playing against itself       
        elif len(self.combi) == 0:
            self.combi = [rd.randint(0,8), rd.randint(0,8), rd.randint(0,8), rd.randint(0,8)]
        
        if self.human:
            r = self.screen.blit(self.myst,(50,line*35+70))
            display.update(r)
            
        prediction = self.list_action[action]
        
        if self.human:
            for i in range(4):
                r = self.screen.blit(self.palette, ((i+1)*30+20, line*35+70),(prediction[i]*30,0,30,30))
                display.update(r)
            
        placed,misplaced = self.feedback(prediction)
        
        if self.human:
            for e,c in enumerate([(255,0,0)]*placed+[(255,255,255)]*misplaced):
                r = draw.circle(self.screen, c, (190+e*10,line*35+85), 2, 0)
                display.update(r)
        
        s_ = str(action) + str(placed) + str(misplaced)
        
        #Choose the reward you prefer
        return (s_, self.reward2(placed,misplaced,line), self.if_won(placed))

    def if_won(self, placed):
        return(placed==4)
        
    def reward1(self, placed):
        #classical reward
        if placed == 4:
            return 0
        else:
            return -1
        
    def reward2(self, placed,misplaced,line):
        #Second reward taking in account number of correct placed and misplaced pegs.
        reward = -1
        
        if(placed==4):
            reward = (10-line)*(10-line)
            return reward
        
        if (placed == 0 and misplaced == 0):
            return reward
        else: 
            reward += placed*0.1
            reward += misplaced*0.05
            return reward
        
        
    def feedback(self, prediction):
        #A function which take the secret code (self.combi), a prediction and return the couple (placed,misplaced) 
        try:
            a,b = zip(*[(a,b) for a,b in zip(self.combi, prediction) if a!=b])
            a   = list(a)
        except: return 4,0
        
        for i in b:
            try: a.remove(i)
            except: continue
        
        return 4-len(b),len(b)-len(a)
    

