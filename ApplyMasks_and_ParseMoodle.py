import sys
import os
import glob
import itertools

import cv2
import mediapipe as mp

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    print('Error: Must supply the directory containing course photos as an argument.')
else:
    photo_dir = sys.argv[1]

    try:
        os.mkdir('Class_PhotoRoster')
    except:
        pass
    
    try:
        os.mkdir('Class_PhotoRoster_masks')
    except:
        pass

    # INITIALIZING OBJECTS
    mp_face_mesh = mp.solutions.face_mesh

    ######## Mask List -- This identifies the indecies associated with different parts of the face.
    Nose = [197]
    Right = [371,266,425,411,416,364]
    chin_right = [394,395,369,396,175]
    chin_left = [175,171,140,170,169]
    Left = [135,192,187,205,36,142]
    Centerline = [197,195,5,4,1,19,94,2,164,0,11,12,13,14,15,16,17,18,200,199,175]
    Mask = Nose+Right+chin_right+chin_left+Left+Nose
    leftMask = Nose+Centerline+chin_left+Left+Nose
    rightMask = Nose+Right+chin_right+Centerline+Nose

    ######### It is possible to query specific face parts
    LEFT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
    RIGHT_EYE_INDEXES = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))

    ######################################  Here we define the file that we are analyzing
    # Get user supplied values
    image_opts = glob.glob('./'+photo_dir+'/*.jpg')
    image_opts2 = glob.glob('./'+photo_dir+'/*.png')

    image_opts = image_opts+image_opts2

    add_mask_flag = 1

    # DETECT THE FACE LANDMARKS
    for iii in image_opts:
        new_im_name = iii.split('/')[-1]
        image = cv2.imread(iii)
        with mp_face_mesh.FaceMesh(min_detection_confidence=0.4, min_tracking_confidence=0.4) as face_mesh:
            # Flip the image horizontally and convert the color space from BGR to RGB
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance
            image.flags.writeable = False

            # Detect the face landmarks
            results = face_mesh.process(image)

            # To improve performance
            image.flags.writeable = True

            # Convert back to the BGR color space
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            plt.figure()
            plt.imshow(np.fliplr(image[:,:,[2,1,0]]))

            iscale = image.shape

            try:
                for face_no, face_landmarks in enumerate(results.multi_face_landmarks):
                    mask_ol = np.zeros((2,len(Mask)))
                    leftmask_ol = np.zeros((2,len(leftMask)))
                    for counter,ind in enumerate(Mask):
                        i = face_landmarks.landmark[ind]
                        mask_ol[:,counter] = np.array([(1-i.x)*iscale[1],i.y*iscale[0]])
                    for counter,ind in enumerate(leftMask):
                        i = face_landmarks.landmark[ind]
                        leftmask_ol[:,counter] = np.array([(1-i.x)*iscale[1],i.y*iscale[0]])
                    if add_mask_flag == 1:
                        plt.plot(mask_ol[0,:],mask_ol[1,:],c='black')
                        plt.fill(mask_ol[0,:],mask_ol[1,:],c='white')
                        plt.fill(leftmask_ol[0,:],leftmask_ol[1,:],c=[0.9,0.9,0.9])
            except:
                pass
            plt.axis('off')
            if add_mask_flag == 0:
                plt.savefig('./Class_PhotoRoster/'+new_im_name[0:-4]+'.png')
            else:
                plt.savefig('./Class_PhotoRoster_masks/'+new_im_name[0:-4]+'.png')



    ################### This section is responsible for parsing the moodle page
    moodle_page = glob.glob('*.html')

    # Using readlines()
    file1 = open(moodle_page[0], 'r')
    Lines = file1.readlines()

    person_count = 0
    on_flag = 0
    # Strips the newline character

    email = []
    first_name = []
    last_name = []
    pronouns = []
    photo_filename = []
    photo_mask_filename = []
    for line in Lines:

        temp_line = line.strip()
        text_opts = temp_line.split('<')     
        pn = ''
        if '<ul class="report-roster"' in temp_line:
            on_flag = 1
        if '</ul>' in temp_line:
            on_flag = 0
        if on_flag == 1:
            for i in text_opts:
                if 'img src' in i:
                    person_count += 1
                    fn_opts_1 = i.split('"')
                    photo_filename.append('Class_PhotoRoster/'+fn_opts_1[1].split('/')[-1][:-4]+'.png')
                    photo_mask_filename.append('Class_PhotoRoster_masks/'+fn_opts_1[1].split('/')[-1][:-4]+'.png')
                elif '@' in i:
                    em_opts_1 = i.split('>')
                    email.append(em_opts_1[-1])
                elif 'span>' in i[0:5]:
                    if '/' in i:
                        if len(pronouns) < person_count-1:
                            pronouns.append('No Pronouns Provided')
                        pn = i.split('>')[-1]
                        pronouns.append(pn)
                    else:
                        name_opts_1 = i.split('>')
                        name_opts_2 = name_opts_1[-1].split(' ')
                        first_name.append(name_opts_2[0])
                        last_name.append(name_opts_2[1])
            #print(person_count,len(pronouns))
            #if len(pronouns) < person_count:
            #    print(line)
            if len(pronouns) < person_count-1:
                pronouns.append('No Pronouns Provided')
                
    data_dict = {'fn':first_name,'ln':last_name,'pronouns':pronouns,'photo':photo_filename,'photo_mask':photo_mask_filename,'email':email}
    data = pd.DataFrame(data_dict)
    data.to_csv('Moodle_DataFrame.csv')
