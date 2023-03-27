

def light_on(file,light,up_error):
    
    import cv2 as cv
    import numpy as np
    
    i = 0
    lightup = []
    cap = cv.VideoCapture(file)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            img_cropped = frame[light[1]:light[1]+light[3], light[0]:light[0]+light[2]]              
            ret,thresh = cv.threshold((img_cropped),240,255,cv.THRESH_BINARY)
            num_exeed_thresh = np.sum(thresh == 255)
            
            if num_exeed_thresh >= up_error:
                lightup.append(i)
            i+=1
            
        else:
            break
        
    cap.release()  
    cv.destroyAllWindows()
    
    return lightup


def check_timestamps(lightup, shock_num):
    
    import numpy as np
    import time
    
    ivalues = [0]
    
    lightup = np.array(lightup)
    diff = np.ediff1d(lightup) 
    turning_point = np.where(diff > 500)

    ivalues.append(lightup[0])
    for idx in turning_point[0]:
        ivalues.append(lightup[idx+1])
    
    if len(ivalues) != shock_num+1:
        print("presentation number in video doesn't match...\n")
    
    timestamps = [time.strftime('%H:%M:%S', time.gmtime(round(x/30))) for x in ivalues]  
    
    return ivalues, timestamps


def light_off(file,light,ivalues,tone_duration,down_error):
    
    import cv2 as cv
    import numpy as np
    start = -99999
    
    check_range = tone_duration + 5
        
    i = 0
    lightdown = []
    ivalues_2 = []
    cap = cv.VideoCapture(file)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            
            if (i in ivalues) and (i != 0):
                if i != ivalues[1]:
                    diff = np.ediff1d(lightdown)
                    turning_point = np.where(diff == min(diff))
                    ivalues_2.append(start+turning_point[0][0])
                lightdown = []
                start = i 
                
            if i <= (start+check_range*30):
                img_cropped = frame[light[1]:light[1]+light[3], light[0]:light[0]+light[2]]              
                ret,thresh = cv.threshold((img_cropped),240,255,cv.THRESH_BINARY)
                num_exeed_thresh = np.sum(thresh == 255)
                lightdown.append(num_exeed_thresh)
                    
            i+=1
        else:
            break
        
    cap.release()  
    cv.destroyAllWindows()
    
    diff = np.ediff1d(lightdown)
    turning_point = np.where(diff == min(diff))
    ivalues_2.append(start+turning_point[0][0])
    
    return ivalues_2
    

def integrate_lights(ivalues, ivalues_2):
    
    initial = (ivalues[0],ivalues[1])
    light_timing = [initial]
    
    for x in range(1,len(ivalues)):
        pair = (ivalues[x],ivalues_2[x-1])
        light_timing.append(pair)
        
    return light_timing
    



if (__name__ == '__main__'):
    print('Executing light_timestamps_func.py\n')




    