import cv2 as cv

LEFT = 30  # Color of the left side of the crown
RIGHT = 25 # Color of the right side of the crown

# Note: When passing in x and y points, you need to be very careful. I pushed
# an image named "example_for_cc.png", the green dot is approx the position of the point you need to push in.
# You may need to change the MOE.
 
def color_check(img, xpos, ypos):
    # This functions takes in a black and white image being looked at and
    # the center point of what we believe is potentially the crown.
    # The output is false if the color to the left and right of the given point
    # does not match the color of the crown or the output is true if the color
    # to he left and right of the given point matches the color of the crown
        
    # Getting left and right pixel intensity values
    left_of_point = img[xpos - 5, ypos]
    right_of_point = img[xpos + 5, ypos]
    MOE = 5
    # print(left_of_point)
    # print(right_of_point)
    
    # Checking the left to see if it matches the color of the crown
    if(LEFT - MOE <= left_of_point and LEFT + MOE >= left_of_point) :
        left_test = True
    else:
        left_test = False        
    
    # Checking the right to see if it matches the color of the crown
    if(RIGHT - MOE <= right_of_point and RIGHT + MOE >= right_of_point):
        right_test = True
    else:
        right_test = False 
    
    # Checking to see if both tests passe or not
    if(left_test == True and right_test == True):
        return True
    else:
        return False

#Code used to test funcion
#This will display all the available mouse click events  
#events = [i for i in dir(cv) if 'EVENT' in i]
#print(events)
#img = cv.imread('example2.png')
#img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#def click_event(event, x, y, flags, params):

    #right-click event value is 2
#    if event == cv.EVENT_LBUTTONDOWN:
#        print (color_check(img, x, y))
        
#print(img[182, 345]) #right
#print(img[160, 345]) #left

#cv.imshow("image", img)
#cv.namedWindow('image')
#cv.setMouseCallback("image", click_event)
#cv.waitKey(0)