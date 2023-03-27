

def freeze_measure(file,circle):
    
    import cv2 as cv
    import numpy as np
    
    i = 0
    pxl_shift = []
    cap = cv.VideoCapture(file)
    
    while(cap.isOpened()):
        
        ret, frame = cap.read()
        if ret == True:
            
            mask = np.zeros(frame.shape[:2], dtype="uint8")
            cv.circle(mask, (circle[0], circle[1]), circle[2], 255, -1)
            frame = cv.bitwise_and(frame, frame, mask=mask)
            
            if i == 0:
                previous = frame
                current = frame

            elif i != 0:
                current = frame
                diff = cv.absdiff(previous,current)
                ret,diff_ = cv.threshold((diff),80,255,cv.THRESH_BINARY)
                pixel_shift = np.sum(diff_ == 255)
                pxl_shift.append(pixel_shift)
        
            previous = current
            i+=1
            
        else:
            break
        
            
    cap.release()  
    cv.destroyAllWindows()
        
    
    return pxl_shift
    


def freeze_measure2(file,circle):
    
    import cv2 as cv
    import numpy as np
    
    i = 0
    pxl_shift = []
    cap = cv.VideoCapture(file)
    
    while(cap.isOpened()):
        
        ret, frame = cap.read()
        if ret == True:
            
            frame = frame[circle[1]:circle[1]+circle[3], circle[0]:circle[0]+circle[2]]    

            if i == 0:
                previous = frame
                current = frame

            elif i != 0:
                current = frame
                diff = cv.absdiff(previous,current)
                ret,diff_ = cv.threshold((diff),80,255,cv.THRESH_BINARY)
                pixel_shift = np.sum(diff_ == 255)
                pxl_shift.append(pixel_shift)
        
            previous = current
            i+=1
            
        else:
            break
        
            
    cap.release()  
    cv.destroyAllWindows()
        
    return pxl_shift




if (__name__ == '__main__'):
    print('Executing freeze_measure_func.py\n')
    
    
    
    
    
    
