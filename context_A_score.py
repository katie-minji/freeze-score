import time
a = time.time()

def temp(file, txt_file):
    
    start = time.time()
    
    # =============================================================================
    
    # change directory to where codes are for freezing data analyzing
    import os
    func_loc = r'Z:\Soo B\Katie\codes\mine\temp\context_A_score\functions'
    os.chdir(func_loc)
    
    # =============================================================================
    # =============================================================================
    
    import txt_light_setup_func as se
    import numpy as np
        
    # textfiles information
    mouse_id, shock_num, tone_duration, initial_delay = se.textfile(txt_file)
    
    # light stuff, crop frame, find optimal thresh value
    light = np.array([360,0,20,20])  #tighter ROI
    # light = se.crop_frame(file, initial_delay)[0]
    up_error, down_error = se.optimal_thresh(file, light, initial_delay)
        
    # =============================================================================
    # =============================================================================
    
    import light_timestamps_func as lt
    
    # light initiation, timestamps (when light comes on)
    lightup = lt.light_on(file, light, up_error)
    ivalues, timestamps = lt.check_timestamps(lightup, shock_num)
    
    # light going off
    ivalues_2 = lt.light_off(file,light,ivalues,tone_duration,down_error)
    
    # finalize on and off with tuples
    light_timing = lt.integrate_lights(ivalues, ivalues_2)
    
    # =============================================================================
    # =============================================================================
    
    import freeze_measure_func as fm
    
    # measure freezing
    freeze_list = fm.freeze_measure(file, ivalues, light_timing, initial_delay, tone_duration)
    
    # =============================================================================
    # =============================================================================
    
    
    final_dict = {'freeze_list': freeze_list, 'timestamps': timestamps}
    
    
    # =============================================================================
    # =============================================================================
    
    end = time.time()
    execution_time = time.strftime('%H:%M:%S', time.gmtime(end-start))
    print(f'This took {execution_time} to run!')
    
    return final_dict
    
    

batch = 'y'
import os
from tkinter import filedialog as fd


def data_extraction():

    maindir = fd.askdirectory()
    os.chdir(maindir)
    everything = list(os.walk(maindir))  #list of folder, subfolder, files
    mylist = []
    subfolder_dir = []
    for dirpath, dirnames, filenames in everything:
        videolist = []
        txtlist = []
        daylist = []
        sorted_files = filenames.copy()
        sorted_files.sort()
        subfolder_dir.append(dirpath)
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
    if len(subfolder_dir) != 1:
        subfolder_dir.pop(0)
        subfolder_dir = [os.path.normpath(path) for path in subfolder_dir]

    return files, subfolder_dir


files, sub_dir = data_extraction()
final_dict = {}

if batch == 'y':
    for mouse in files:
        mouse_id = '_'.join(mouse.split('_')[:2])
        for index, v in enumerate(sub_dir):
            if mouse_id in v:
                idx = index
        path = sub_dir[idx]
        for x in files[mouse]:
            print(mouse, x[0])  #mouse and day
            directories = x[1]
            for types in directories: 
                if types.endswith('.mp4'):
                    file = os.path.join(path,types)
                if types.endswith('.txt'):
                    txt_file = os.path.join(path,types)
            final = temp(file, txt_file)
            final_dict[f'{mouse} {x[0]}'] = final
            print(' ')                                                                                 



b = time.time()
execution_time = time.strftime('%H:%M:%S', time.gmtime(b-a))
print(f'\nTOTAL EXECUATION TIME: {execution_time}')




#%%


import pickle
import os

path = r'Z:\Soo B\Katie\projects\freezing_score\pickle_files'
os.chdir(path)

with open('ctxA_909', 'wb') as handle:
    pickle.dump(final_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    

#%%


import pickle
import os
os.chdir(r'Z:\Soo B\Katie\projects\freezing_score\pickle_files')

# open pickle
with open("ctxA", "rb") as f:
    rawdata = f.read()
    
ctxA = pickle.loads(rawdata)




