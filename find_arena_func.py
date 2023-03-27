


def find_arena(file):
    
    import cv2 as cv
    import numpy as np
    import copy
    import tkinter as tk
    global happy, circle
    
    def draw_circle(img_copy, pt):
        pt = np.uint16(np.around(pt))  #round numbers
        a, b, r = pt[0], pt[1], pt[2]
        cv.circle(img_copy, (a, b), r, (0, 255, 0), 2)
        cv.imshow("Detected Circle", img_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()
            
    
    def circle_select(num):  #output circle
        
        m = tk.Tk()
        m.geometry("250x500")
        m.title('Condition Select')
        
        tk.Label(m, text='choose circle number').pack(anchor=tk.W, pady=1.5)
        Circle = tk.IntVar(m)
        
        for i in range(1,num+1):
            tk.Radiobutton(m, text=f'circle {str(i)}', variable=Circle, value=i).pack(anchor=tk.W)
        tk.Radiobutton(m, text='none of the above', variable=Circle, value=i+1).pack(anchor=tk.W)
        
        def submit():
            global circle
            circle = Circle.get()
            m.quit()
            m.destroy()  
        def circle_again():
            img_copy = copy.deepcopy(img_copy_2)           
            for pt in detected_circles[0, :]:
                draw_circle(img_copy, pt)
        tk.Button(m, text="Done", command=submit).pack(anchor=tk.W, pady=8)
        tk.Button(m, text="See again", command=circle_again).pack(anchor=tk.W, pady=8)
        m.mainloop()
        
        return circle
      
     
    def manual_circle(file):
        
        cap = cv.VideoCapture(file)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                print('press enter after selecting around the arena.')
                my_c = cv.selectROIs('manual circle', frame)
                cv.waitKey(0)
                cv.destroyAllWindows()
                break
            
        my_c = my_c[0]
        a = my_c[0]+0.5*my_c[2]
        b = my_c[1]+0.5*my_c[3]
        r = 0.5*my_c[2]
        pt = np.array([a,b,r])
    
        return pt
    
    
    def yes_or_no(file, pt):
        
        m = tk.Tk()
        m.geometry("250x200")
        m.title('Condition Select')
        
        tk.Label(m, text='Are you happy with this circle?').pack(anchor=tk.W, pady=1.5)
    
        def Yes():
            global happy
            happy = True        
            m.quit()
            m.destroy()  
            global circle
            circle = pt
        def No():
            global happy
            happy = False
            m.quit()
            m.destroy()
            global circle
            circle = manual_circle(file)
        tk.Button(m, text="yes", command=Yes).pack(anchor=tk.W, pady=8)
        tk.Button(m, text="no", command=No).pack(anchor=tk.W, pady=8)
        
        m.mainloop()
        
        return circle
        
        
    def are_you_happy(pt, file):    
        
        print("Are you happy with this circle?")
        global happy
        happy = False
        while happy == False:
            img_copy = copy.deepcopy(img_copy_2)    
            draw_circle(img_copy, pt)
            pt = yes_or_no(file, pt)
        
        return pt

    
    cap = cv.VideoCapture(file)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            img = frame
            break
        else:
            break
    img_copy = copy.deepcopy(img)
    img_copy_2 = copy.deepcopy(img)
    img = cv.medianBlur(img,3)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    detected_circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, 
                                       minRadius=200, maxRadius=230)


    if detected_circles is None:
        print("No circles found... \nDirecting to manual circle...\n")
        pt = manual_circle(file)
    
    else:
        num_circles = len(detected_circles[0])
        
        if num_circles == 1:
            print("One circle found! \nCheck if it is the right circle.\n")
            pt = detected_circles[0][0]
            
        if (num_circles > 1) and (num_circles <= 10):  #if more then 1 but less than 10
            print(f"Total of {len(detected_circles[0])} circles found.")
            print("which is the right circle?\n")
            for pt in detected_circles[0, :]:
                draw_circle(img_copy, pt)
            pt = circle_select(num_circles)
            if pt > num_circles: 
                pt = manual_circle(file)
            else:
                pt = detected_circles[0][pt-1]
        
        elif num_circles > 10: #if more than 10 circles
            print("Too many circles found... \nDirecting to manual circle...\n")
            pt = manual_circle(file)
        
    # manual until satisfied
    circle = are_you_happy(pt, file)
    circle = np.uint16(np.around(circle)) 
    del happy
    
    return circle




def crop_frame(file):
    
    import cv2 as cv
    print('\nSelect the lightbulb and press the enter key')
    cap = cv.VideoCapture(file)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if i == 0:
                break
            i += 1
        else:
            break
        
    light_coordinates = cv.selectROIs('select_light', frame)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    return light_coordinates






















if (__name__ == '__main__'):
    print('Executing find_arena_func.py\n')
    
    
    
    
    