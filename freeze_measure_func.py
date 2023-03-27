

def freeze_measure(file,ivalues,light_timing,initial_delay,tone_duration):
    
    import cv2 as cv
    import numpy as np
    
    i = 0
    between, after = [], []
    between_list, after_list = [], []
    cap = cv.VideoCapture(file)
    
    while(cap.isOpened()):
        
        ret, frame = cap.read()
        if ret == True:
            
            if i == 0:
                previous = frame
            
            if i in ivalues:
                if i != 0:
                    between_list.append(between)
                    after_list.append(after)
                    between, after = [], []
                idx = ivalues.index(i)
                focus = light_timing[idx]
            
            if i in range(focus[0],focus[1]):   #between
                if (idx == 0):    #initial delay
                    current = frame
                    diff = cv.absdiff(previous,current)
                    ret,diff_ = cv.threshold((diff),80,255,cv.THRESH_BINARY)
                    pixel_shift = np.sum(diff_ == 255)
                    between.append(pixel_shift)
            
            if i in range(focus[1],focus[1]+1801):  #after, for 1 min
                if idx != 0:
                    current = frame
                    diff = cv.absdiff(previous,current)
                    ret,diff_ = cv.threshold((diff),80,255,cv.THRESH_BINARY)
                    pixel_shift = np.sum(diff_ == 255)
                    after.append(pixel_shift)
            
            previous = current
            i+=1
            
        else:
            break
        
    cap.release()  
    cv.destroyAllWindows()
    
    between_list.append(between)
    after_list.append(after)
    
    my_initial = [between_list[0]]
    my_after = after_list[1:]
    freeze_list = my_initial+my_after
    
    return freeze_list



if (__name__ == '__main__'):
    print('Executing freeze_measure_func.py\n')
    
    
    
    
    
    
