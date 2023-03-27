


def textfile(file):  #mouse ID here too?
    
    with open(file) as f:
            lines = [line.rstrip() for line in f.readlines()]
                
    for line in lines: 
        
        if line.startswith('mouse ID'):
            mouse_id = line.split()[-1]
        
        if line.startswith('number of cycles'):
            shock_num = int(float(line.split(' ')[-1]))
            
        if line.startswith('tone duration'):
            tone_duration = int(float(line.split()[-1]))
        
        if line.startswith('initial delay'):
            initial_delay = int(float(line.split()[-1]))
            
    return mouse_id, shock_num, tone_duration, initial_delay


def crop_frame(file, initial_delay):
    
    import cv2 as cv
    print('\nSelect the lightbulb and press the enter key')
    cap = cv.VideoCapture(file)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if i == (initial_delay*30-30):
                break
            i += 1
        else:
            break
        
    light_coordinates = cv.selectROIs('select_light', frame)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    return light_coordinates


def optimal_thresh(file,light,initial_delay):
    
    import cv2 as cv
    import numpy as np
    
    delay = 30*initial_delay-30
    
    cap = cv.VideoCapture(file)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            img_cropped = frame[light[1]:light[1]+light[3], light[0]:light[0]+light[2]]              
            ret,thresh = cv.threshold((img_cropped),240,255,cv.THRESH_BINARY)
            num_exeed_thresh = np.sum(thresh == 255)
            if i == (delay - 90):
                off = num_exeed_thresh
            if i == delay:
                on = num_exeed_thresh
                break
            i+=1
        else:
            break
        
    error = (on - off) / 5
    if on > (off + error*3):
        pass
    else: 
        print('Difference in light between on and off is not big enough')
    up_error = on - error
    down_error = off + error
    
    return up_error, down_error



if (__name__ == '__main__'):
    print('Executing txt_light_setup_func.py\n')
    
    
