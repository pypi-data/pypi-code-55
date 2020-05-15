import cv2
import pandas as pd

index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('https://raw.githubusercontent.com/sunnysinghnitb/color_detector/master/colors.csv', names=index, header=None)

def color_name(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def colo(img_path):
    img = cv2.imread(img_path)

    clicked = False
    r = g = b = xpos = ypos = 0

    def draw(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            nonlocal r, g, b, xpos, ypos, clicked
            clicked = True
            xpos = x
            ypos = y
            b,g,r = img[y,x]
            b = int(b)
            g = int(g)
            r = int(r)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw)

    while(1):
        cv2.imshow("image",img)
        if (clicked):
            cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
            text = color_name(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
            cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

            if(r+g+b>=600):
                cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            clicked=False

        if cv2.waitKey(20) & 0xFF ==27:
            break

    cv2.destroyAllWindows()
    
    return