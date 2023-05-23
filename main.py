
import numpy as np
import os
import time
from datetime import datetime

func_loc = r'D:\freeze-score'
new_path = r'G:\My Drive\lab\pickle\fz_score'  #folder to store score output (versioning, one dict) and progress txt file

os.chdir(func_loc)

from function import Process
from function import Setup
from function import UserSelect
from function import LightTime
from function import Video
from function import Pickle

new_folder_path, master_path, individual_path = Process.initiate(new_path)
files, sub_dir = Setup.get_files()
## Setup.filter(), remove ones already existing from pickle. 

# initial video light and arena check/crop
arena_dict = {}
light_dict = {}
for mouse in files:
    path = Setup.find_path(mouse,sub_dir)
    
    # light and arena for B
    for by_day in files[mouse]:
        file, txt_file, context = Setup.select_file_ctx(mouse, by_day, path, files, sub_dir)     
        
        if context == 'B':
            print('')
            print(mouse, by_day[0])
            mouse_id, shock_num, tone_duration, initial_delay = UserSelect.get_info_txt(txt_file)
            
            if 'wt8' in mouse:                   #if rectangle contextBO
                light = np.array([350,0,30,30])
            else:                                #if circle contextB
                arena = UserSelect.circle(file)
                arena_dict[mouse] = arena
            
                light = UserSelect.light_crop(file, initial_delay)[0]
           
            light_dict[mouse] = light
            up_error, down_error = UserSelect.optimal_thresh(file, light, initial_delay)

    # thresh hold check for A
    for by_day in files[mouse]:
        file, txt_file, context = Setup.select_file_ctx(mouse, by_day, path, files, sub_dir)
        
        if context == 'A':
            mouse_id, shock_num, tone_duration, initial_delay = UserSelect.get_info_txt(txt_file)
            light = np.array([360,0,20,20])
            up_error, down_error = UserSelect.optimal_thresh(file, light, initial_delay)


print("\n\n=======================================================")
print("Passed light tests...! Starting video analyzation...\n\n")


# progress indication
total = 0
for _ in files.values():
    total = total + len(_)
vid_rn = 0

a = time.time()
final_start = datetime.now().strftime('%I:%M %p')

final_dict = {}
pres_error = {}

# video processing
for mouse in files:
    
    path = Setup.find_path(mouse,sub_dir)
    for by_day in files[mouse]:
        
        vid = f'{mouse} {by_day[0]}'  #name of vid
        Process.mouse(new_folder_path, vid)
        start = time.time()
        
        file, txt_file, context = Setup.select_file_ctx(mouse, by_day, path, files, sub_dir)
        
        if context == 'A':
            light = np.array([360,0,20,20])
            
        elif context == 'B':
            light = light_dict[mouse]

        mouse_id, shock_num, tone_duration, initial_delay = UserSelect.get_info_txt(txt_file)
        up_error, down_error = UserSelect.optimal_thresh(file, light, initial_delay)
        
        # light initiation, timestamps (when light comes on)
        lightup = LightTime.light_on(file, light, up_error)
        ivalues, timestamps, pres_error = LightTime.check_timestamps(lightup, shock_num, new_folder_path, vid, pres_error)
        
        # light going off
        ivalues_2 = LightTime.light_off(file,light,ivalues,tone_duration,down_error)
        
        # finalize on and off with tuples
        on_off_idx = LightTime.integrate_lights(ivalues, ivalues_2)
            
        if context == 'A':
            pxl_shift = []
            pxl_shift = Video.square(file)
        
        elif context == 'B':
            if 'wt8' in mouse:                   #if rectangle contextB
                pxl_shift = Video.squareB(file)
            else:                                #if circle contextB
                pxl_shift = Video.circle(file,arena_dict[mouse])
            
            
        final = {'pxl_shift': pxl_shift, 'on_off_idx': on_off_idx, 'timestamps': timestamps}    
        final_dict[vid] = final

        vid_rn = Process.append(vid_rn, new_folder_path, start, a, total)


# append final message to text file that it is all done
Process.final_append(a, final_start, new_folder_path)
Process.error_append(new_folder_path, pres_error)

# pickle save
Pickle.version(final_dict, master_path)
Pickle.by_mouse(final_dict, individual_path)


