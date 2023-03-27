
import numpy as np
import os
import time
from datetime import timedelta
from datetime import datetime

func_loc = r'Z:\Soo B\Katie\codes\mine\temp\test'
os.chdir(func_loc)

from function import Setup
from function import UserSelect
from function import LightTime
from function import Video

files, sub_dir = Setup.get_files()

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
            
            if 'wt8' in mouse:                   #if rectangle contextB
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


# video processing
for mouse in files:
    
    path = Setup.find_path(mouse,sub_dir)
    for by_day in files[mouse]:
        
        print(mouse, by_day[0])
        start = time.time()
        #========================================
        
        file, txt_file, context = Setup.select_file_ctx(mouse, by_day, path, files, sub_dir)
        
        if context == 'A':
            light = np.array([360,0,20,20])
            
        elif context == 'B':
            light = light_dict[mouse]

        mouse_id, shock_num, tone_duration, initial_delay = UserSelect.get_info_txt(txt_file)
        up_error, down_error = UserSelect.optimal_thresh(file, light, initial_delay)
        
        # light initiation, timestamps (when light comes on)
        lightup = LightTime.light_on(file, light, up_error)
        ivalues, timestamps = LightTime.check_timestamps(lightup, shock_num)
        
        # light going off
        ivalues_2 = LightTime.light_off(file,light,ivalues,tone_duration,down_error)
        
        # finalize on and off with tuples
        on_off_idx = LightTime.integrate_lights(ivalues, ivalues_2)
            
        if context == 'A':
            pxl_shift = Video.square(file)
        
        elif context == 'B':
            if 'wt8' in mouse:                   #if rectangle contextB
                pxl_shift = Video.square(file)
            else:                                #if circle contextB
                pxl_shift = Video.circle(file,arena_dict[mouse])
            
            
        final = {'pxl_shift': pxl_shift, 'on_off_idx': on_off_idx, 'timestamps': timestamps}    
        final_dict[f'{mouse} {by_day[0]}'] = final

        #========================================    
        time.sleep(3)
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
End approximatly {endtime}. {time_left} left.\n
        '''
        print(_)



b = time.time()
total_time = time.strftime('%H:%M:%S', time.gmtime(b-a))
final_end = datetime.now().strftime('%I:%M %p')
_ = f'''
\n=======================================================
Finished video analyzation!

TOTAL EXECUATION TIME: {total_time}
START TIME: {final_start}
END TIME: {final_end}'''
print(_)





import pickle
import os

path = r'D:\picklefile'
os.chdir(path)

with open('my_final', 'wb') as handle:
    pickle.dump(final_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)





