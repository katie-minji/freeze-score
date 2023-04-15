
class Process:
    
    def initiate(new_path):
        
        import os
        from datetime import datetime
        
        ori_path = os.getcwd()
        os.chdir(new_path)
        
        now = datetime.now()
        filename = now.strftime("%Y_%m_%d__%H_%M_%S")
        os.mkdir(filename)
        new_folder_path = os.path.join(new_path, filename)
        os.chdir(new_folder_path)
        
        with open("Video Process Checker.txt","w") as log:
            log.write("Video Processing Start")
        
        os.chdir(ori_path)
        
        return new_folder_path
    
    
    def append(vid_rn, new_folder_path, start, a, total):
        
        import os
        import time
        from datetime import timedelta
        from datetime import datetime
        
        ori_path = os.getcwd()
        os.chdir(new_folder_path)
        
        end = time.time()
        execution_time = time.strftime('%H:%M:%S', time.gmtime(end-start))
        vid_rn = vid_rn+1
        elapsed = end-a
        temp = time.strftime('%H:%M:%S', time.gmtime(end-a))
        perc = round((vid_rn/total),3)
        time_left = time.strftime('%H:%M:%S', time.gmtime(elapsed*((1-perc)/perc)))
        _ = datetime.now()+timedelta(seconds=(elapsed*(1/perc)))
        endtime = _.strftime('%I:%M %p')
        
        _ = f'''video elapsed: {execution_time}
        total elapsed: {temp}
        progress: {vid_rn}/{total} ({perc*100}%)
        End approximatly {endtime}. {time_left} left.\n\n
        '''
        
        with open("Video Process Checker.txt", 'a') as log:
            log.write(_)
        
        os.chdir(ori_path)
        print(_)
           
        
        return vid_rn
    
   
        
#%%

class Pickle:
    
    def version(final_dict, new_folder_path):
        
        import pickle
        import os
        
        os.chdir(new_folder_path)
        with open('master.pkl', 'wb') as handle:
            pickle.dump(final_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    
    def by_mouse(final_dict):
        
        import pickle
        import os
        
        os.chdir()
        separated = {}
        
        for vid_name in final_dict.keys():
            mouse = vid_name.split()[0]
            separated[mouse] = {}
        for vid_name, data in final_dict.items():
            mouse = vid_name.split()[0]
            separated[mouse][vid_name] = data
            
        for mouse, data in separated.items():    
            with open(mouse, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        return separated
    
    
#%%
    
 
class Setup:
    
    def redundent_filter(final_path, files, sub_dir):
        
        import glob
        import os
        
        ori_path = os.getcwd()
        os.chdir(final_path)
        
        already_list = glob.glob('*')
        
        new_list = []
        for x in sub_dir:
            vid = os.path.basename(sub_dir[0])
            new_list.append(vid)
        
        to_process = []
        for x in new_list:
            if x in already_list:
                pass
            else:
                to_process.append(x)
        
        # make new file with only files from to process
        
        os.chdir(ori_path)
        
        return files, sub_dir
        

    def get_files():
        
        import os
        from tkinter import filedialog as fd
        
        maindir = fd.askdirectory()
        os.chdir(maindir)
        everything = list(os.walk(maindir))  #list of folder, subfolder, files
        mylist = []
        sub_dir = []
        for dirpath, dirnames, filenames in everything:
            videolist = []
            txtlist = []
            daylist = []
            sorted_files = filenames.copy()
            sorted_files.sort()
            sub_dir.append(dirpath)
            for idx, file in enumerate(sorted_files):
                if file.endswith('.txt'):
                    txtlist.append(file)
                    day = file.split('_')
                    day = [x for x in day if 'D' in x] 
                    for y in day: 
                        if y.isalpha() == False:
                            daylist.append(y)
                if file.endswith('.mp4'):
                    videolist.append(file)
            if dirnames == []:
                bymouse = list(zip(videolist,txtlist))  #combine video and txt into tuples
                mylist.append(list(zip(daylist,bymouse)))
            if len(everything) == 1:  #if mouse folder selected
                mouselist = ['_'.join(os.path.basename(everything[0][0]).split('_')[1:4])]
            else:
                mouselist = [x for x in everything[0][1]]  #list mouse in cohort
        files = {mouselist[i]: mylist[i] for i in range(len(mouselist))}  #make dictionary key=mouse, value=directory&files
        if len(sub_dir) != 1:
            sub_dir.pop(0)
            sub_dir = [os.path.normpath(path) for path in sub_dir]
    
        return files, sub_dir

    
    def find_path(mouse,sub_dir):
        
        for index, v in enumerate(sub_dir):
            if mouse in v:
                idx = index
        path = sub_dir[idx]
        
        return path
    

    def select_file_ctx(mouse, by_day, path, files, sub_dir):
       
        import os
        
        directories = by_day[1]
        for types in directories: 
            if types.endswith('.mp4'):
                file = os.path.join(path,types)
            if types.endswith('.txt'):
                txt_file = os.path.join(path,types)
            
        if len(files[mouse]) == int(by_day[0][1]):  #if contextB
            context = 'B'
        else:    #if contextA
            context = 'A'
        
        return file, txt_file, context
    
    

#%%

class UserSelect:
    
    def circle(file):
        
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
            print("No circles found... \nDirecting to manual circle...")
            pt = manual_circle(file)
        
        else:
            num_circles = len(detected_circles[0])
            
            if num_circles == 1:
                print("One circle found! \nCheck if it is the right circle.")
                pt = detected_circles[0][0]
                
            if (num_circles > 1) and (num_circles <= 10):  #if more then 1 but less than 10
                print(f"Total of {len(detected_circles[0])} circles found.")
                print("which is the right circle?")
                for pt in detected_circles[0, :]:
                    draw_circle(img_copy, pt)
                pt = circle_select(num_circles)
                if pt > num_circles: 
                    pt = manual_circle(file)
                else:
                    pt = detected_circles[0][pt-1]
            
            elif num_circles > 10: #if more than 10 circles
                print("Too many circles found... \nDirecting to manual circle...")
                pt = manual_circle(file)
            
        # manual until satisfied
        circle = are_you_happy(pt, file)
        circle = np.uint16(np.around(circle)) 
        del happy
        
        return circle

    
    def get_info_txt(file):  #mouse ID here too?
        
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


    def light_crop(file, initial_delay):
        
        import cv2 as cv
        print('Select the lightbulb and press the enter key')
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
                # shift.append(num_exeed_thresh)
                if i == (delay - 90*30):
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
            print('\nDifference in light between on and off is not big enough\n')
        up_error = on - error
        down_error = off + error
        
        return up_error, down_error

#%%

class LightTime:
    
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
        
        ivalues.pop(0)
        on_off_idx = list(zip(ivalues, ivalues_2))
            
        return on_off_idx
    
    

#%%

class Video:
    
    def square(file):
        
        import cv2 as cv
        import numpy as np
        
        i = 0
        pxl_shift = []
        cap = cv.VideoCapture(file)
        
        while(cap.isOpened()):
            
            ret, frame = cap.read()
            if ret == True:
                
                if i == 0:
                    previous = frame
                    current = frame

                elif i != 0:
                    current = frame
                    diff = cv.absdiff(previous,current)
                    diff = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
                    ret,diff_ = cv.threshold((diff),20,255,cv.THRESH_BINARY)
                    pixel_shift = np.sum(diff_ == 255)
                    pxl_shift.append(pixel_shift)
            
                previous = current
                i+=1
                
            else:
                break
            
        cap.release()  
        cv.destroyAllWindows()
        
        # thres = pxl_shift[20760:22560]
        # import cv2
        # cv2.imshow('window', diff_)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        
        return pxl_shift
    
    
    
    
    
    def circle(file,circle):
        
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
                    ret,diff_ = cv.threshold((diff),20,255,cv.THRESH_BINARY)
                    pixel_shift = np.sum(diff_ == 255)
                    pxl_shift.append(pixel_shift)
            
                previous = current
                i+=1
                
            else:
                break
            
                
        cap.release()  
        cv.destroyAllWindows()
            
        
        return pxl_shift
        
    
