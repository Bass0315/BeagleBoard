#!/usr/bin/env python
# Author: Baozhu Zuo <zuobaozhu@gmail.com>
# Copyright (c) 2018 Seeed Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# +-------------------------------------+-----------------------+
# Test item: ok|                        |                       |
# Test item: ok|                        |                       |
# Test item: ok|                        |                       |
# Test item: ok|   PIC1                 |    PIC2               |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            +------------------------+-----------------------+
# |            |                                                |
# |            |         finish(failed or succeed)              |
# |            |                                                |
# +------------+------------------------------------------------+



import time
import os
import pygame, sys
from pygame.locals import *
import queue
import threading



class display(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        #Set up pygame
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.hight = self.screen_info.current_h
        self.wide = self.screen_info.current_w
        
        self.text_index = 0
        self.ethernet_ok_count = 0
        self.ethernet_failed_count = 0
        self.miniusb_ok_count = 0
        self.miniusb_failed_count = 0
        
        self.pic_w = self.wide / 3 + 150
        self.pic_h = self.hight*2/3
        #Set up the window
        self.windowSurface = pygame.display.set_mode((self.wide, self.hight), 0 , 32)
        pygame.display.set_caption('ReSpeaker v2')

        #Set up the colors
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)

        #Draw the white background onto the surface
        self.windowSurface.fill(self.BLACK)

        self.isExit = False
        self.complete = False
        self.data = queue.Queue()
    def run(self):
        while True:	
            if (self.isExit and self.complete):
                break
            if not self.data.empty():
                latest_data = self.data.get()
                if latest_data["type"] == "text":
                    self.print_text(latest_data)
                elif latest_data["type"] == "picture":
                    if latest_data["location"] == "left":
                        self.print_pic_left(latest_data["path"])
                    else:
                        self.print_pic_right(latest_data["path"])
                elif latest_data["type"] == "finish":
                    self.print_finish(latest_data["finish"])
                    self.complete = True
                self.show()
                #print(latest_data)

    def show(self):
        #Draw the window onto the screen
        pygame.display.update()
        
    def print_text(self,str_line): 
        if str_line["description"] == "ethernet":
            if str_line["result"] == "ok":
                self.ethernet_ok_count = self.ethernet_ok_count + 1
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.ethernet_ok_count,self.GREEN,50,320 - 20 - 16*2,20 + self.text_index*35)
            elif str_line["result"] == "failed":
                self.ethernet_failed_count = self.ethernet_failed_count + 1 
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + (self.text_index+1)*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.ethernet_failed_count,self.RED,50,320 - 20 - 16*2,20 + (self.text_index+1)*35)
            else:
                self.ethernet_ok_count = 0
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.ethernet_ok_count,self.GREEN,50,320 - 20 - 16*2,20 + self.text_index*35)
                self.ethernet_failed_count = 0 
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + (self.text_index+1)*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.ethernet_failed_count,self.RED,50,320 - 20 - 16*2,20 + (self.text_index+1)*35)
                
        elif str_line["description"] == "miniusb":
            if str_line["result"] == "ok":
                self.miniusb_ok_count = self.miniusb_ok_count + 1
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index+3*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.miniusb_ok_count,self.GREEN,50,320 - 20 - 16*2,20 + self.text_index+3*35)
            elif str_line["result"] == "failed":
                self.miniusb_failed_count = self.miniusb_failed_count + 1
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index+4*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.miniusb_failed_count,self.RED,50,320 - 20 - 16*2,20 + self.text_index+4*35)     
            else:
                self.miniusb_ok_count = 0
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index+3*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.miniusb_ok_count,self.GREEN,50,320 - 20 - 16*2,20 + self.text_index+3*35)
                self.miniusb_failed_count = 0
                self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index+4*35)
                self.print_str(str_line["result"]+" ,count: "+'%d'%self.miniusb_failed_count,self.RED,50,320 - 20 - 16*2,20 + self.text_index+4*35)               
        else:
            self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + (self.text_index+5)*35)
            self.print_str(str_line["result"],self.WHITE,50,320 - 20 - 16*5,20 + (self.text_index+5)*35)
    def print_str(self,str,color,f_size,x,y):
        f = pygame.font.Font(None, f_size)
        w,h = f.size(str)
        #print('wide: {} hight: {} '.format(w,h))
        pygame.draw.rect(self.windowSurface,self.BLACK,(x,y,320,h))

        text_surface = f.render(str, True, color)

        self.windowSurface.blit(text_surface, (x, y)) 
    def print_pic_right(self,pic="/opt/pic/rgb.png"):
        picture = pygame.image.load(pic)
        picture = pygame.transform.scale(picture, (int(self.pic_w), int(self.pic_h)))    
        rect = picture.get_rect() 
        rect = rect.move((self.wide - self.pic_w, 20 ))
        self.windowSurface.blit(picture, rect)  

    def print_pic_left(self,pic="/opt/pic/rgb.png"):
        picture = pygame.image.load(pic)
        picture = pygame.transform.scale(picture, (int(self.pic_w), int(self.pic_h)))   
        rect = picture.get_rect() 
        rect = rect.move((int(self.wide-self.pic_w*2) -5 , 20 ))
        self.windowSurface.blit(picture, rect)     
    

    def print_finish(self,r):
        if r == True:
            self.print_str(u"SUCCEED",self.GREEN,300,self.wide-1.5*self.pic_w , (self.hight + self.pic_h)/2 - 80)
        else:
            self.print_str(u"FAILED",self.RED,300,self.wide-1.5*self.pic_w, (self.hight + self.pic_h)/2 - 80)
    def __del__(self):
        self.isExit = True
#        pygame.quit()
    
if __name__ == "__main__":
    data_json = {}
    d = display()
    d.start()
    path="/opt/EMSTS/status/"   #the result of this path information is about port test
    files=os.listdir(path)      #return file they are come from "/opt/EMSTS/status/"
    while True:
    	data_json.clear()
        for file in files:
            fileName="/opt/EMSTS/status/"+file
            cmd = "cat " + fileName
#            print cmd
    	    l=os.popen(cmd)
            status=l.read()
            l.close()
            status=status.replace('\n','').replace('\r','')
#            print(status)
            flagNumber = status.find("#")
            typeNumber = status.find("&")
            if typeNumber > 2:
                cmd = "echo '' > " + fileName
                os.system(cmd)
                if status[0:typeNumber]== "text":
    	            data_json["type"] = status[0:typeNumber]
    	            data_json["description"] = status[typeNumber+1:flagNumber]
                    data_json["result"] = status[flagNumber+1:]   #information include ok or failed;ok count and failed count
                    d.data.put(data_json)
                if status[0:typeNumber]== "finish":
                    data_json["type"] = status[0:typeNumber]
                    if status[typeNumber+1:]=="True":
                        data_json["finish"] = True
                    else:
                        data_json["finish"] = False
                    d.data.put(data_json)
    	time.sleep(0.05)    
