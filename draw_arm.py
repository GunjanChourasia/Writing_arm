import cv2
import numpy as np 
import math
import time
import pypot.dynamixel

drawing=False 
mode=True 

ports = pypot.dynamixel.get_available_ports()
dxl = pypot.dynamixel.DxlIO(ports[0])

def pos(x,y):   #gives coordinates for the arm to move
    d = math.hypot(x, y)
    theta = math.degrees(math.atan2(y, x))
    alpha = math.acos(d/30)
    alpha = math.degrees(alpha)
    beta = math.acos(1 - ((d**2) / 450))
    beta = math.degrees(beta)
    return (alpha+theta) - 90, beta-180

def move(Dxl, x, y):    #Dxl code for moving the arm
    ids = [1, 2]
    angs = pos(x, y)
    moves = {}
    j = 0
    for i in ids:
        moves[i] = angs[j]
        j += 1
    Dxl.set_moving_speed({1:1000, 2:1000})
    Dxl.set_goal_position(moves)
    print moves
    time.sleep(0.2)


dxl.set_moving_speed({1:50, 2:50})
print(dxl.scan(range(5)))

def interactive_drawing(event,x,y,flags,param):     #Draws the path for arm to follow by dragging a mouse
    global ix,iy,drawing, mode
    global dxl
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy=x,y

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                #cv2.circle(img,(x,y),1,(0,0,255),-1)
                assert x<=400 and y<=200 and x>=0 and y>=0



                cv2.line(img,(ix,iy),(x,y),(0,0,255),1)
                ix=x
                iy=y
                X1= (400-x)/40.0
                Y1=((200-y)/200.0)*8
                #X=X1*math.cos(50)-Y1*math.sin(50)+5
                #Y=X1*math.cos(50)+Y1*math.sin(50)-19
                #X=(X1+Y1+24)/(2*math.cos(-50))
                #Y=(Y1-X1+14)/(2*math.sin(-50))
                X=X1+5
                Y=Y1+19

                #move(dxl, X, Y)
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.circle(img,(x,y),1,(0,0,255),-1)
            #print x,y
            #cv2.line(img,(x,y),(x,y),(0,0,255),10)
    return x,y

img = np.zeros((200,400,3), np.uint8)
#dxl.set_goal_position({1:0, 2:0})
cv2.namedWindow('draw_here')
cv2.setMouseCallback('draw_here',interactive_drawing)
while(1):
    cv2.imshow('draw_here',img)
    k=cv2.waitKey(1)
    if k==27:
        break
cv2.destroyAllWindows()


