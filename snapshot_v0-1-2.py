#!/usr/bin/env python3

'''
Snapshot - Media Carrier Intake Check Tool
Version: 0.1.2
Originally developed as part of the digital preservation workflow at the Met.
Previously: DigiPres Workflow Initial Steps Automation (clamscan, hashdeep, tree, exiftool)

last updated: 08/27/2026
developed by Jenny Hsu
'''

#1. Ask for user input (path to media carrier/directory)
#2. Run clamscan by dragging in artist-provided media carrier.
#3. Using hashdeep, generate a list of all files and checksums in DFXML.
#4. Run tree to get output that can be pasted into TMS.
#5. Run exiftool.

import os
import subprocess

# Color codes
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'  # Reset back to normal

#Welcome message!
print(CYAN + r"""               __
              / _)
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_|                                       
        __  |    __  __  |\  /|  __   
  |  | /__\ |   /  \/  \ | \/ | /__\  
  |/\|| ___||  |   | () ||    || ___| 
      |     |   \__/\__/ |    ||      
       \__/ |                   \__/  
            |__|                                            """)
print(CYAN + '''
snapshot v0.1.2
Automates clamscan, hashdeep, tree, and exiftool for artwork file ingestion.

Dependencies: clamav, md5deep, tree, exiftool through Homebrew
(See README.md for dependencies installation instructions)

Press Control+C at any time to exit.
''' + RESET)

#Take user input, path to media carrier/directory.
while True:
    media_path = input('Please enter path to the media carrier/directory you would like to examine: ').strip().replace('\\', '')
    if os.path.exists(media_path):
        # continue to ask about clamscan om the next section
        break
    else:
        print('Path invalid. Please try again.')

#Empty strings to collect all results.
clamscan_final_results = ""
hash_final_results = ""
tree_final_results = ""
exif_final_results = ""
# disk_final_results = ""

def error_handling_yn(message):
    while True:
        answer = input(message).strip().lower()
        if answer == 'y':
            break
        elif answer == 'n':
            exit()
        else:
            print('Invalid response. Try again.')

def save_files(results, servicename, extension, ui_date, ui_componentno, save_directory):
        filename = f'{ui_componentno}_{ui_date}-delivery_{servicename}.{extension}'
        path = os.path.join(save_directory, filename)
        with open(path, 'w') as f:
            f.write(results)
        print(f'Results saved to {path}')

#Ask to run clamscan.
while True:
    run_clamscan = input('Run clamscan? (y/n): ').strip().lower()
    if run_clamscan == 'y':
        print('Updating virus definitions with freshclam...')
        freshresult = subprocess.run(['freshclam'], capture_output=True, text=True)
        if freshresult.returncode !=0:
            error_handling_yn('freshclam not responding. clamscan anyway? (y/n, n will exit): ')
        else:
            print('freshclam updated!')

        print('running clamscan...please wait!')
        clamresult = subprocess.run(['clamscan', '-r', media_path], capture_output = True, text = True)
        print(clamresult.stdout)
        if clamresult.returncode != 0:
            error_handling_yn('clamscan not responding. Continue to hashdeep? (y/n, n will exit)')
        else:
            clamscan_final_results += clamresult.stdout #appended to empty string/file
        break
    elif run_clamscan == 'n':
        print('clamscan skipped.') #then continues in the next section to ask about hashdeep
        break
    else:
        print('Invalid response. Try again.')

#Ask to run hashdeep.
while True:
    run_hashdeep = input('Run hashdeep? (y/n): ').strip().lower()
    if run_hashdeep == 'y':
        print('running hashdeep...please wait!')
        hashresult = subprocess.run(['hashdeep', '-r', '-d', media_path], capture_output = True, text = True)
        print(hashresult.stdout)
        if hashresult.returncode != 0:
            error_handling_yn('hashdeep not responding. Continue to tree? (y/n, n will exit.): ')
        else:
            hash_final_results += hashresult.stdout
        break
    elif run_hashdeep == 'n':
        print('hashdeep skipped.') #then continues in the next section to ask about hashdeep
        break
    else:
        print('Invalid response. Try again.')

#Ask to run tree.
while True:
    run_tree = input('Run tree? (y/n): ').strip().lower()
    if run_tree == 'y':
        treeresult = subprocess.run(['tree', '-a', '-N', '-h', '--du', '-D', media_path], capture_output = True, text = True)
        print(treeresult.stdout)
        if treeresult.returncode != 0:
            error_handling_yn('tree is not responding. continue to results? (y/n, n will exit.): ')
        else:
            tree_final_results += treeresult.stdout
        break
    elif run_tree == 'n':
        print('tree skipped.') #then continues in the next section to ask about hashdeep
        break
    else:
        print('Invalid response. Try again.')

#Ask to run exiftool.
while True:
    run_exif = input('Run exiftool? (y/n): ').strip().lower()
    if run_exif == 'y':
        exifresult = subprocess.run(['exiftool', '-r', '-a', media_path], capture_output = True, text = True, encoding='latin-1')
        print(exifresult.stdout)
        # Check if there's output FIRST
        if exifresult.stdout:
            # Save the results
            exif_final_results += exifresult.stdout
            # Note any warnings
            if exifresult.returncode != 0:
                print(f"\nNote: exiftool completed with warnings (exit code: {exifresult.returncode})")
        else:
            # No output - ask user
            error_handling_yn('exiftool produced no output. Continue? (y/n, n will exit.): ')

        break

# #Ask to run disktype.
# while True:
#     run_disk = input('Run disktype? (y/n): ').strip().lower()
#     if run_disk == 'y':
#         diskresult = subprocess.run(['disktype', media_path], capture_output = True, text = True)
#         print(diskresult.stdout)
#         if diskresult.returncode != 0:
#             error_handling('disktype is not responding. continue to results? (y/n, n will exit.): ')
#         else:
#             disk_final_results += diskresult.stdout
#         break
#     elif run_disk == 'n':
#         print('disktype skipped.') #then continues in the next section to ask about hashdeep
#         break
#     else:
#         print('Invalid response. Try again.')


#check if any 'service' ran
if clamscan_final_results or hash_final_results or tree_final_results or exif_final_results:

    while True:
        saveorno = input('Would you like to save your results? (y/n): ').strip().lower()

        if saveorno == 'y':
            save_directory = input('Where would you like to save results file? (provide path to directory): ').strip()
            ui_date = input('Component date of delivery? (YYYYMMDD): ').strip()
            ui_componentno = input('Insert component number of physical media (i.e. 2002-228-ECx2): ').strip()

           #if clamscan ran, save it
            if clamscan_final_results:
                save_files(clamscan_final_results, 'clamscan', 'txt', ui_date, ui_componentno, save_directory)

            #if hashdeep ran, save it
            if hash_final_results:
                filename_hash = f'{ui_componentno}_{ui_date}-delivery_hashdeep.xml'
                save_path_hash = os.path.join(save_directory, filename_hash)
                with open(save_path_hash, 'w') as f:
                    f.write(hash_final_results)
                print(f'Results saved to {save_path_hash}')

            #if tree ran, save it
            if tree_final_results:
                filename_tree = f'{ui_componentno}_{ui_date}-delivery_tree.txt'
                save_path_tree = os.path.join(save_directory, filename_tree)
                with open(save_path_tree, 'w') as f:
                    f.write(tree_final_results)
                print(f'Results saved to {save_path_tree}')

            #if exiftool ran, save it
            if exif_final_results:
                filename_exif = f'{ui_componentno}_{ui_date}-delivery_exiftool.txt'
                save_path_exif = os.path.join(save_directory, filename_exif)
                with open(save_path_exif, 'w') as f:
                    f.write(exif_final_results)
                print(f'Results saved to {save_path_exif}')

            # #if disktype ran, save it
            # if disk_final_results:
            #     filename_disk = f'{ui_date}-delivery_{ui_componentno}_disktype.txt'
            #     save_path_disk = os.path.join(save_directory, filename_disk)
            #     with open(save_path_disk, 'w') as f:
            #         f.write(disk_final_results)
            #     print(f'Results saved to {save_path_disk}')

            break

        elif saveorno == 'n':
            exit()
        else:
            print('Invalid response. Try again')

else:
    print('No commands were run. Nothing to save.')
