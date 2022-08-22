# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 21:25:42 2021
Code taken from Fernando Moya
Modified by Nilah Nair
"""
import numpy as np
import csv
import os
import sys
import datetime
import csv_reader
from sliding_window import sliding_window
import pickle


#enter the path where the dataset is saved
#FOLDER_PATH = "/Mbientlab/LARa_dataset_mbientlab/"
FOLDER_PATH = '/'

'''number of subject classes vary depending on the type of subset of data that is being considered for experiment
type 1 and type 2 = 7
type 3 = 6
type 4 = 5
all = 8
'''
NUM_CLASSES=8

SCENARIO = {'R01': 'L01', 'R02': 'L01', 'R03': 'L02', 'R04': 'L02', 'R05': 'L02', 'R06': 'L02', 'R07': 'L02',
            'R08': 'L02', 'R09': 'L02', 'R10': 'L02', 'R11': 'L02', 'R12': 'L02', 'R13': 'L02', 'R14': 'L02',
            'R15': 'L02', 'R16': 'L02', 'R17': 'L03', 'R18': 'L03', 'R19': 'L03', 'R20': 'L03', 'R21': 'L03',
            'R22': 'L03', 'R23': 'L03', 'R24': 'L03', 'R25': 'L03', 'R26': 'L03', 'R27': 'L03', 'R28': 'L03',
            'R29': 'L03', 'R30': 'L03'}

subselection= { 0:"type1" , 1:"type2", 2:"type3", 3:"type4", 4:"all"}

def opp_sliding_window(data_x, data_y, ws, ss, label_pos_end=True):
    
    print("Sliding window: Creating windows {} with step {}".format(ws, ss))

    data_x = sliding_window(data_x, (ws, data_x.shape[1]), (ss, 1))

    count_l = 0
    idy = 0
    # Label from the end
    #not used for the experiment
    if label_pos_end:
        data_y = np.asarray([[i[-1]] for i in sliding_window(data_y, (ws, data_y.shape[1]), (ss, 1))])
    else:
        if False:
            # Label from the middle
            # not used in experiments
            data_y_labels = np.asarray(
                [[i[i.shape[0] // 2]] for i in sliding_window(data_y, (ws, data_y.shape[1]), (ss, 1))])
        else:
            # Label according to mode
            try:
                data_y_labels = []
                for sw in sliding_window(data_y, (ws, data_y.shape[1]), (ss, 1)):
                    labels = np.zeros((1)).astype(int)
                    count_l = np.bincount(sw[:, 0], minlength=NUM_CLASSES)
                    idy = np.argmax(count_l)
                   
                    labels[0] = idy
                   
                    data_y_labels.append(labels)
                data_y_labels = np.asarray(data_y_labels)
            except:
                print("Sliding window: error with the counting {}".format(count_l))
                print("Sliding window: error with the counting {}".format(idy))
                return np.Inf

            # All labels per window
            data_y_all = np.asarray([i[:] for i in sliding_window(data_y, (ws, data_y.shape[1]), (ss, 1))])

    return data_x.astype(np.float32), data_y_labels.astype(np.uint8), data_y_all.astype(np.uint8)

def norm_mbientlab(data, subset):
    '''
    Normalizes all sensor channels
    Zero mean and unit variance

    @param data: numpy integer matrix
    @return data_norm: Normalized sensor data
    
    before running the preprocessing, please make sure that you have run the norm_imu.py file to obtain the mean and std deviation data and 
    updated the respective fields. 
    '''
    if subselection[subset] == "type1":
        mean_values = np.array([-0.604270513,  0.152956490,  0.322321324,  0.389408162,
                                0.197817624, -0.653126441,  0.0476041071,  1.00963016,
                                -0.142480054,  0.211524953,  1.17799808, -1.41275496,
                                -0.948744073, -0.0789351942,  0.163643662, -0.360987455,
                                0.598964311,  0.554854048, -0.615292038, -0.158791051,
                                0.404709821,  0.0822201238,  0.792620598,  1.37951844,
                                -0.229777369, -0.876349943, -0.206187437,  0.945720434,
                                0.510248324,  0.386259696])
        mean_values = np.reshape(mean_values, [1, 30])

        std_values = np.array([0.415765826,  0.541248524,  0.44502122,  53.1239674,
                               64.0457436,  54.3366985,  0.427268140,  0.226922238,
                               0.277689980,  30.3652109,  57.4548809,  62.9766391,
                               0.160528428,  0.210713906,  0.315062951,  37.0735847,
                               18.7201301,  17.9642357,  0.437347613,  0.532682080,
                               0.406481133,  58.4462137, 72.6094852,  59.6650363,
                               0.596013311,  0.425130372,  0.351205656,  42.0825727,
                               58.0533664,  64.0456206])
        std_values = np.reshape(std_values, [1, 30])
        
    elif subselection[subset] == "type2":
        mean_values =np.array([-0.60783108,  0.1640153,   0.39861219,  1.27958508, -0.31284539, -4.34756889,
                               -0.01402777,  1.03604567, -0.11950175,  4.56493369,  4.4879063,  -1.46518256,
                               -0.9852407,  -0.08997262,  0.12401219,  1.11027397,  1.77619783,  0.17006392,
                               -0.57983815, -0.220964,    0.44724146, -3.33079494,  0.59240603, -1.66851938,
                               -0.2840733,  -0.8191318,  -0.21932313, -0.13634647,  0.71114821,  0.62759753])
        mean_values = np.reshape(mean_values, [1, 30])
        
        std_values = np.array([ 1.97313975,   0.59050277,   0.92987198,  58.7537963,   84.64365545,
                               122.02761651,   1.59414569,   1.01901767,   1.14813707, 143.99941186,
                               153.23253408,  64.17515141,   0.63352773,   0.22322419,   0.30729428,
                               50.94892096,  33.29206898,  18.42448973,   0.48018568,   0.5157117,
                               0.55615973, 113.02446618,  80.81807919,  99.70208161,   1.09609546,
                               0.58862733,   0.85753087,  36.82159178,  62.39001861,  64.16056807])
        std_values = np.reshape(std_values, [1, 30])
    
    elif subselection[subset] == "type3":
        mean_values= np.array([-0.6200914,   0.14143905,  0.36254782,  0.98599565, -0.21967514, -2.97762359,
                               0.0116792,   1.02994192, -0.13389797,  3.21394732,  3.82663941, -1.59950976,
                               -0.9680652,  -0.09346404,  0.14538209,  0.50057431,  1.2562121,   0.36204835,
                               -0.58811174, -0.16992941,  0.43176594, -1.98321313,  0.47721201, -0.42428187,
                               -0.27843243, -0.84112026, -0.22087056,  0.58269852,  0.92448553,  0.44536153])
        mean_values = np.reshape(mean_values, [1, 30])
        
        std_values = np.array([  1.6596286,    0.58851056,   0.80059148,  56.00434659,  76.75496007,
                               105.70418751,   1.34815488,   0.86092765,   0.9684477,  121.49235389,
                               131.62000241,  67.33838001,   0.53938571,   0.21923004,   0.31818944,
                               46.76843155,  29.78979248,  18.52047611,   0.4731271,    0.53445842,
                               0.50229102, 100.09105194,  76.78732035,  88.96565595,   0.98935636,
                               0.55415324,   0.75100717,  42.62376115,  62.69705387,  67.55396168])
        std_values = np.reshape(std_values, [1, 30])
        
    elif subselection[subset] == "type4":
        mean_values= np.array([-0.59291547,  0.16510277,  0.39688181,  1.06174891,  0.03655466, -2.54978003,
                               0.0113082,   1.02285025, -0.13735555,  2.49047449,  2.90262683, -1.55012442,
                               -0.96827405, -0.11433454,  0.13784902,  0.46335482,  1.1964269,   0.3138417,
                               -0.5691449,  -0.19274769,  0.46068746, -1.72215207,  0.70927256, -0.14452921,
                               -0.3169523,  -0.80255785, -0.22178045,  0.51473459,  0.83091342,  0.33518692])
        mean_values = np.reshape(mean_values, [1, 30])
        
        std_values = np.array([  1.50468289,   0.58002835,   0.75289687,  58.34711067,  78.30835137,
                               98.8953262,    1.21128132,   0.77066658,   0.86914161, 108.49528975,
                               119.35092774,  64.29606825,   0.48262522,   0.21772873,   0.30442066,
                               45.41451804,  27.60438897,  18.59057502,   0.47634617,   0.53341564,
                               0.49594787,  94.47440142,  80.03186714,  85.56527538,   0.91948319,
                               0.54490135,   0.68835778,  41.7696377,   58.54988989,  63.32484912])
        std_values = np.reshape(std_values, [1, 30])
        
    elif subselection[subset]== "all":
        mean_values = np.array([-0.6018319,   0.234877,    0.2998928,   1.11102944,  0.17661719, -1.41729978,
                                0.03774093,  1.0202137,  -0.1362719,   1.78369919,  2.4127946,  -1.36437627,
                                -0.96302063, -0.0836716,   0.13035097,  0.08677377,  1.088766,    0.51141513,
                                -0.61147614, -0.22219321,  0.41094977, -1.45036893,  0.80677986, -0.1342488,
                                -0.02994514, -0.999678,   -0.22073192, -0.1808128,  -0.01197039,  0.82491874])
        mean_values = np.reshape(mean_values, [1, 30])
        
        std_values = np.array([1.17989719,   0.55680584,   0.65610454,  58.42857495,  74.36437559,
                               86.72291263,   1.01306,      0.62489802,   0.70924608,  86.47014857,
                               100.6318856,   61.02139095,   0.38256693,   0.21984504,   0.32184666,
                               42.84023413,  24.85339931,  18.02111335,   0.44021448,   0.51931148,
                               0.45731142,  78.58164965,  70.93038919,  76.34418105,   0.78003314,
                               0.32844988,   0.54919488,  26.68953896,  61.04472454,  62.9225945])
        std_values = np.reshape(std_values, [1, 30])
    
    try:
        mean_array = np.repeat(mean_values, data.shape[0], axis=0)
        std_array = np.repeat(std_values, data.shape[0], axis=0)

        max_values = mean_array + 2 * std_array
        min_values = mean_array - 2 * std_array

        data_norm = (data - min_values) / (max_values - min_values)

        data_norm[data_norm > 1] = 1
        data_norm[data_norm < 0] = 0
    except:
        raise("Error in normalisation")

    return data_norm

############################

def reader_data(path):
    print('Getting data from {}'.format(path))
    #counter = 0
    IMU = []
    time = []
    data = []
    with open(path, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            try:
                try:
                    if spamreader.line_num == 1:
                        # print('\n')
                        print(', '.join(row))
                    else:
                        if len(row) != 31:
                            idx_row = 0
                            IMU.append(row[idx_row])
                            idx_row += 1
                        else:
                            idx_row = 0
                        try:
                            time_d = datetime.datetime.strptime(row[idx_row], '%Y-%m-%d %H:%M:%S.%f')
                            idx_row += 1
                        except:
                            try:
                                time_d = datetime.datetime.strptime(row[idx_row.astype(int)], '%Y-%m-%d %H:%M:%S')
                                idx_row += 1
                            except:
                                print("strange time str {}".format(time_d))
                                continue
                        time.append(time_d)
                        data.append(list(map(float, row[idx_row:])))
                except:
                    print("Error in line {}".format(row))
            except KeyboardInterrupt:
                print('\nYou cancelled the operation.')
  
    if len(row) != 31:
        imu_data = {'IMU': IMU, 'time': time, 'data': data}
    else:
         
         #imu_data = {'time': time, 'data': data}
         data_new=np.asarray(data)
         print(data_new.shape)
    
    return data_new

#####################

def generate_data(subset, sliding_window_length, sliding_window_step, data_dir=None, identity_bool=False, usage_modus='train'):
    
    if subselection[subset]=='"type1"':
        #type1-avoiding person 12
        persons = ["S07", "S08", "S09", "S10", "S11", "S13", "S14"]
        ID = {"S07": 0, "S08": 1, "S09": 2, "S10": 3, "S11": 4, "S13": 5, "S14": 6}
        train_ids = ["R03", "R07", "R08", "R10", "R11"]
        val_ids = ["R12"]
        test_ids = ["R15"]
    elif subselection[subset]=="type2":
        #type2- avoiding person 11
        persons = ["S07", "S08", "S09", "S10", "S12", "S13", "S14"]
        ID = {"S07": 0, "S08": 1, "S09": 2, "S10": 3, "S12": 4, "S13": 5, "S14": 6}
        train_ids =["R11", "R12", "R15", "R18", "R19","R21"]
        val_ids = ["R22"]
        test_ids = ["R23"]
    elif subselection[subset]=="type3":
        #type3- Avoiding person 11 and 12
        persons = ["S07", "S08", "S09", "S10", "S13", "S14"]
        ID = {"S07": 0, "S08": 1, "S09": 2, "S10": 3, "S13": 4, "S14": 5}
        train_ids = ["R03", "R07", "R08", "R10", "R11", "R12", "R15", "R18"]
        val_ids = ["R19", "R21"]
        test_ids = ["R22", "R23"]
    elif subselection[subset]=="type4":
        #type4-Avoiding persons 11,12,10
        persons = ["S07", "S08", "S09", "S13", "S14"]
        ID = {"S07": 0, "S08": 1, "S09": 2, "S13": 3, "S14": 4}
        train_ids = ["R03", "R07", "R08", "R10", "R11", "R12", "R15", 
                     "R18", "R19", "R21", "R22"]
        val_ids = ["R23","R25", "R26"]
        test_ids = ["R27", "R28", "R29"]
    elif subselection[subset]=='all':
        #all subjects with IMU data
        persons = ["S07", "S08", "S09", "S10", "S11", "S12", "S13","S14"]
        ID = {"S07": 0, "S08": 1, "S09": 2, "S10": 3, "S11": 4, "S12":5, "S13": 6, "S14": 7}
        train_ids = ["R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10", 
                 "R13", "R14", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", 
                 "R24", "R25", "R26", "R27", "R28", "R29", "R30"]
        val_ids = ["R11","R12"]
        test_ids = ["R15"]
        
    counter_seq = 0
    #hist_classes_all = np.zeros((NUM_CLASSES))
    
    for P in persons:
        if usage_modus == 'train':
           recordings = train_ids
        elif usage_modus == 'val':
           recordings = val_ids
        elif usage_modus == 'test':
           recordings = test_ids
        print("\nModus {} \n{}".format(usage_modus, recordings))
        for R in recordings:
               try:
                    S = SCENARIO[R]
                    file_name_data = "{}/{}_{}_{}.csv".format(P, S, P, R)
                    file_name_label = "{}/{}_{}_{}_labels.csv".format(P, S, P, R)
                    print("\n{}\n".format(file_name_data))
                    try:
                        data = reader_data(FOLDER_PATH + file_name_data)
                        print("\nFiles loaded in modus {}\n{}".format(usage_modus, file_name_data))
                        data_x=data
                        print("\nFiles loaded")
                       
                    except:
                        print("\n1 In loading data,  in file {}".format(FOLDER_PATH + file_name_data))
                        continue
               
                    try:
                        # Getting labels and attributes
                        labels = csv_reader.reader_labels(FOLDER_PATH + file_name_label)
                        class_labels = np.where(labels[:, 0] == 7)[0]

                        # Deleting rows containing the "none" class
                        data_x = np.delete(data_x, class_labels, 0)
                        labels = np.delete(labels, class_labels, 0)

                        #data_t, data_x, data_y = divide_x_y(data)
                        #del data_t
                    except:
                        print("2 In generating data, Error getting the data {}".format(FOLDER_PATH
                                                                                       + file_name_data))
                        continue
                    #label given to the individual
                    labelid=ID[P]
                   
                    try:
                        #normalosation, deactivate this line to avoid normalisation
                        data_x = norm_mbientlab(data_x, subset)
                    except:
                        print("\n3  In generating data, Plotting {}".format(FOLDER_PATH + file_name_data))
                        continue
                    
                    try:
                        # checking if annotations are consistent
                        if data_x.shape[0] == data_x.shape[0]:
                            # Sliding window approach
                            print("\nStarting sliding window")
                            X, y, y_all = opp_sliding_window(data_x, labels.astype(int), sliding_window_length, sliding_window_step, label_pos_end=False)
                            print("\nWindows are extracted")
                            
                            for f in range(X.shape[0]):
                               
                                try:
                                    sys.stdout.write('\r' + 'Creating sequence file number {} with id {}'.format(f, counter_seq))
                                    sys.stdout.flush()

                                    #print("\nCreating sequence file number {} with id {}".format(f, counter_seq))
                                    
                                    seq = np.reshape(X[f], newshape=(1, X.shape[1], X.shape[2]))
                                    seq = np.require(seq, dtype=np.float)
                                    #print(seq.shape)
                                    #obj = {"data": seq, "label": labelid}
                                    '''
                                    not that the obj setting will influene the HARWindows.py code. If you make changes here, please make the respective
                                    changes to the file.
                                    '''
                                    obj = {"data": seq, "act_label": y[f], "act_labels_all": y_all[f], "label": labelid}
                                    file_name = open(os.path.join(data_dir,
                                                                  'seq_{0:06}.pkl'.format(counter_seq)), 'wb')
                                    
                                    pickle.dump(obj, file_name, protocol=pickle.HIGHEST_PROTOCOL)
                                    file_name.close()

                                    counter_seq += 1

                                except:
                                    raise ('\nError adding the seq')

                            print("\nCorrect data extraction from {}".format(FOLDER_PATH + file_name_data))

                            del data
                            del data_x
                            del X
                            del labels
                            del class_labels
                            
                           
                        else:
                            print("\n4 Not consisting annotation in  {}".format(file_name_data))
                            continue
                    except:
                        print("\n5 In generating data, No created file {}".format(FOLDER_PATH + file_name_data))
                    print("-----------------\n{}\n-----------------".format(file_name_data))
               except KeyboardInterrupt:
                    print('\nYou cancelled the operation.')
                    
    return   

##################

def generate_CSV(csv_dir, data_dir):
    f = []
    for dirpath, dirnames, filenames in os.walk(data_dir):
        for n in range(len(filenames)):
            f.append(data_dir + 'seq_{0:06}.pkl'.format(n))

    np.savetxt(csv_dir, f, delimiter="\n", fmt='%s')
        
    return f

###########################
          
def generate_CSV_final(csv_dir, data_dir1, data_dir2):
    '''
    Generate CSV file with path to all (Training and Validation) of the segmented sequences
    This is done for the DATALoader for Torch, using a CSV file with all the paths from the extracted
    sequences.

    @param csv_dir: Path to the dataset
    @param data_dir1: Path of the training data
    @param data_dir2: Path of the validation data
    '''
    f = []
    for dirpath, dirnames, filenames in os.walk(data_dir1):
        for n in range(len(filenames)):
            f.append(data_dir1 + 'seq_{0:06}.pkl'.format(n))

    for dirpath, dirnames, filenames in os.walk(data_dir2):
        for n in range(len(filenames)):
            f.append(data_dir1 + 'seq_{0:06}.pkl'.format(n))

    np.savetxt(csv_dir, f, delimiter="\n", fmt='%s')

    return f

##################################                    
                    
def create_dataset():

    #directory where the windows need to be saved along with labels
    #base_directory='/data/nnair/output/activities/type4/imu/'
    base_directory='/'
    
    data_dir_train = base_directory + 'sequences_train/'
    data_dir_val = base_directory + 'sequences_val/'
    data_dir_test = base_directory + 'sequences_test/'
    
    '''
    choose the subselection of data here. Enter the number in subset as per the subselection you require
    subselection= { 0:"type1" , 1:"type2", 2:"type3", 3:"type4", 4:"all"}
    '''
    
    subset=4
    
    ''' 
    to generate dara based on the selected window length, step, and directory.
    '''
    
    generate_data(subset, sliding_window_length=100, sliding_window_step=12, data_dir=data_dir_train, usage_modus='train')
    generate_data(subset, sliding_window_length=100, sliding_window_step=12, data_dir=data_dir_val, usage_modus='val')
    generate_data(subset, sliding_window_length=100, sliding_window_step=12, data_dir=data_dir_test, usage_modus='test')
    
    generate_CSV(base_directory + "train.csv", data_dir_train)
    generate_CSV(base_directory + "val.csv", data_dir_val)
    generate_CSV(base_directory + "test.csv", data_dir_test)
    generate_CSV_final(base_directory + "train_final.csv", data_dir_train, data_dir_val)

    return


if __name__ == '__main__':
    create_dataset()
    print("Done")