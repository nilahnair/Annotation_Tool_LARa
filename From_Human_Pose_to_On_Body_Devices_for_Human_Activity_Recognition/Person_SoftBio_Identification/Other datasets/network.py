'''
Created on Mar 28, 2019
code by fernando moya
modified by nilah nair
network file for opportunity and pamap
'''


from __future__ import print_function
import logging


import torch
import torch.nn as nn
import torch.nn.functional as F 
import torch.optim as optim

import numpy as np


class Network(nn.Module):
    '''
    classdocs
    '''

    def __init__(self, config):
        '''
        Constructor
        '''
        
        super(Network, self).__init__()
        
        logging.info('            Network: Constructor')
        
        self.config = config
        
        if self.config["reshape_input"]:
            in_channels = 3
            Hx = int(self.config['NB_sensor_channels'] / 3)
        else:
            in_channels = 1
            Hx = self.config['NB_sensor_channels']
        Wx = self.config['sliding_window_length']


        # Computing the size of the feature maps
        Wx, Hx = self.size_feature_map(Wx=Wx,
                                       Hx=Hx,
                                       F=(self.config['filter_size'], 1),
                                       P=0, S=(1, 1), type_layer='conv')
        logging.info('            Network: Wx {} and Hx {}'.format(Wx, Hx))
        Wx, Hx = self.size_feature_map(Wx=Wx,
                                       Hx=Hx,
                                       F=(self.config['filter_size'], 1),
                                       P=0, S=(1, 1), type_layer='conv')
        logging.info('            Network: Wx {} and Hx {}'.format(Wx, Hx))
        Wx, Hx = self.size_feature_map(Wx=Wx,
                                       Hx=Hx,
                                       F=(self.config['filter_size'], 1),
                                       P=0, S=(1, 1), type_layer='conv')
        logging.info('            Network: Wx {} and Hx {}'.format(Wx, Hx))
        Wx, Hx = self.size_feature_map(Wx=Wx,
                                       Hx=Hx,
                                       F=(self.config['filter_size'], 1),
                                       P=0, S=(1, 1), type_layer='conv')
        logging.info('            Network: Wx {} and Hx {}'.format(Wx, Hx))

        # set the Conv layers
        if self.config["network"] == "cnn":
            self.conv1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)
            self.conv1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)
            self.conv2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)
            self.conv2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            if self.config["reshape_input"]:
                self.fc3 = nn.Linear(self.config['num_filters'] * int(Wx) * int(self.config['NB_sensor_channels'] / 3),
                                     256)
            else:
                self.fc3 = nn.Linear(self.config['num_filters'] * int(Wx) * self.config['NB_sensor_channels'], 256)

        # set the Conv layers
        if self.config["network"] == "cnn_imu":
            # LA
            self.conv_LA_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_LA_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LA_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LA_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LA = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            int(self.config['NB_sensor_channels'] / 15), 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LA = nn.Linear(self.config['num_filters'] * int(Wx) * 10, 256)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LA = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            54, 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LA = nn.Linear(self.config['num_filters'] * int(Wx) * 13, 256)

            # LL
            self.conv_LL_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_LL_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LL_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LL_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LL = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            int(self.config['NB_sensor_channels'] / 15), 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LL = nn.Linear(self.config['num_filters'] * int(Wx) * 8, 256)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LL = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            52, 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LL = nn.Linear(self.config['num_filters'] * int(Wx) * 13, 256)

            # N
            self.conv_N_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_N_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_N_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_N_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)


            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_N = nn.Linear(self.config['num_filters'] * int(Wx) *
                                           int(self.config['NB_sensor_channels'] / 15), 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_N = nn.Linear(self.config['num_filters'] * int(Wx) * 6, 256)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_N = nn.Linear(self.config['num_filters'] * int(Wx) *
                                           45, 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_N = nn.Linear(self.config['num_filters'] * int(Wx) * 14, 256)


            # RA
            self.conv_RA_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_RA_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RA_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RA_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RA = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            int(self.config['NB_sensor_channels'] / 15), 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RA = nn.Linear(self.config['num_filters'] * int(Wx) * 10, 256)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RA = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            54, 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RA = nn.Linear(self.config['num_filters'] * int(Wx) * 13, 256)

            # RL
            self.conv_RL_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_RL_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RL_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RL_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RL = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            int(self.config['NB_sensor_channels'] / 15), 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RL = nn.Linear(self.config['num_filters'] * int(Wx) * 8, 256)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RL = nn.Linear(self.config['num_filters'] * int(Wx) *
                                            52, 256)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RL = nn.Linear(self.config['num_filters'] * int(Wx) * 13, 256)
                    
        # set the Conv layers
        if self.config["network"] == "lstm":
            # LA
            self.conv_LA_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_LA_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LA_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LA_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LA = nn.LSTM(input_size=(self.config['num_filters'] * 
                                            int(self.config['NB_sensor_channels'] / 15)),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LA = nn.LSTM(input_size=(self.config['num_filters'] * 10),hidden_size= 256, num_layers=1, batch_first=True)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LA = nn.LSTM(input_size=(self.config['num_filters'] *
                                            54),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LA = nn.LSTM(input_size=(self.config['num_filters'] *13),hidden_size= 256, num_layers=1, batch_first=True)

            # LL
            self.conv_LL_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_LL_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LL_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_LL_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LL = nn.LSTM(input_size=(self.config['num_filters'] *
                                            int(self.config['NB_sensor_channels'] / 15)),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LL = nn.LSTM(input_size=(self.config['num_filters'] * 8),hidden_size= 256, num_layers=1, batch_first=True)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_LL = nn.LSTM(input_size=(self.config['num_filters'] * 
                                            52),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_LL = nn.LSTM(input_size=(self.config['num_filters'] * 13),hidden_size= 256, num_layers=1, batch_first=True)

            # N
            self.conv_N_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_N_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_N_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_N_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)


            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_N = nn.LSTM(input_size=(self.config['num_filters'] * 
                                           int(self.config['NB_sensor_channels'] / 15)),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_N = nn.LSTM(input_size=(self.config['num_filters'] * 6),hidden_size= 256, num_layers=1, batch_first=True)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_N = nn.LSTM(input_size=(self.config['num_filters'] * 
                                           45),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_N = nn.LSTM(input_size=(self.config['num_filters'] * 14),hidden_size= 256, num_layers=1, batch_first=True)

            # RA
            self.conv_RA_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_RA_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RA_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RA_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RA = nn.LSTM(input_size=(self.config['num_filters'] * 
                                            int(self.config['NB_sensor_channels'] / 15)),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RA = nn.LSTM(input_size=(self.config['num_filters'] * 10),hidden_size= 256, num_layers=1, batch_first=True)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RA = nn.LSTM(input_size=(self.config['num_filters'] * 
                                            54),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RA = nn.LSTM(input_size=(self.config['num_filters'] * 13),hidden_size= 256, num_layers=1, batch_first=True)

            # RL
            self.conv_RL_1_1 = nn.Conv2d(in_channels=in_channels,
                                     out_channels=self.config['num_filters'],
                                     kernel_size=(self.config['filter_size'], 1),
                                     stride=1, padding=0)

            self.conv_RL_1_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RL_2_1 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            self.conv_RL_2_2 = nn.Conv2d(in_channels=self.config['num_filters'],
                                          out_channels=self.config['num_filters'],
                                          kernel_size=(self.config['filter_size'], 1),
                                          stride=1, padding=0)

            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RL = nn.LSTM(input_size=(self.config['num_filters'] * 
                                            int(self.config['NB_sensor_channels'] / 15)),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RL = nn.LSTM(input_size=(self.config['num_filters'] * 8),hidden_size= 256, num_layers=1, batch_first=True)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    self.fc3_RL = nn.LSTM(input_size=(self.config['num_filters'] *
                                            52),hidden_size= 256, num_layers=1, batch_first=True)
                elif self.config["dataset"] == 'pamap2':
                    self.fc3_RL = nn.LSTM(input_size=(self.config['num_filters'] * 13),hidden_size= 256, num_layers=1, batch_first=True)

        if self.config["network"] == "cnn":
            self.fc4 = nn.Linear(256, 256)
        elif self.config["network"] == "cnn_imu":
            if self.config["dataset"]=="pamap2":
                self.fc4 = nn.Linear(256 * 3, 256)
            else: 
                self. fc4.nn.Linear(256 *5, 256)
        elif self.config["network"] == "lstm":
            if self.config["dataset"]=='pamap2':
                self.fc4 = nn.LSTM(input_size=(256*3), hidden_size= 256, dropout=0.5, num_layers=2, batch_first=True)
            else:
                self.fc4 = nn.LSTM(input_size=(256 * 5), hidden_size= 256, dropout=0.5, num_layers=2, batch_first=True)
                
        if self.config['output'] == 'softmax': 
            self.fc5 = nn.Linear(256, self.config['num_classes'])
        elif self.config['output'] == 'attribute':  
            self.fc5 = nn.Linear(256, self.config['num_attributes'])
        
        self.softmax = nn.Softmax()
        
        self.sigmoid = nn.Sigmoid()
        
        return
    
    def forward(self, x):

        if self.config["network"] == "cnn":
            x = F.relu(self.conv1_1(x))
            x = F.relu(self.conv1_2(x))
            #x12 = F.max_pool2d(x12, (2, 1))

            x = F.relu(self.conv2_1(x))
            x = F.relu(self.conv2_2(x))
            # x = F.max_pool2d(x, (2, 1))

            # view is reshape
            x = x.view(-1, x.size()[1] * x.size()[2] * x.size()[3])
            x = F.relu(self.fc3(x))
        elif self.config["network"] == "cnn_imu":
            # LA
            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_LA = np.arange(0, 36)
                    idx_LA = np.concatenate([idx_LA, np.arange(63, 72)])
                    idx_LA = np.concatenate([idx_LA, np.arange(72, 81)])
                    x_LA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LA]))
                elif self.config["dataset"] == 'pamap2':
                    idx_LA = np.arange(1, 14)
                    x_LA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LA]))
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_LA = np.arange(0, 36)
                    idx_LA = np.concatenate([idx_LA, np.arange(63, 72)])
                    idx_LA = np.concatenate([idx_LA, np.arange(72, 81)])
                    x_LA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LA]))
                elif self.config["dataset"] == 'pamap2':
                    idx_LA = np.arange(1, 14)
                    x_LA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LA]))

            x_LA = F.relu(self.conv_LA_1_2(x_LA))
            x_LA = F.relu(self.conv_LA_2_1(x_LA))
            x_LA = F.relu(self.conv_LA_2_2(x_LA))
            # view is reshape
            if self.config["network"] == "cnn_imu":
                x_LA = x_LA.view(-1, x_LA.size()[1] * x_LA.size()[2] * x_LA.size()[3])
                x_LA = F.relu(self.fc3_LA(x_LA))
            elif self.config["network"] == "lstm":
                x_LA = x_LA.view(x_LA.size()[0], -1, x_LA.size()[1] * x_LA.size()[3])
                x_LA,_ = self.fc3_LA(x_LA)

            # LL
            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_LL = np.arange(0, 36)
                    idx_LL = np.concatenate([idx_LL, np.arange(81, 97)])
                    x_LL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LL]))
                elif self.config["dataset"] == 'pamap2':
                    idx_LL = np.arange(27, 40)
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_LL = np.arange(0, 36)
                    idx_LL = np.concatenate([idx_LL, np.arange(81, 97)])
                    x_LL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LL]))
                elif self.config["dataset"] == 'pamap2':
                    idx_LL = np.arange(27, 40)
                    x_LL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_LL]))

            x_LL = F.relu(self.conv_LL_1_2(x_LL))
            x_LL = F.relu(self.conv_LL_2_1(x_LL))
            x_LL = F.relu(self.conv_LL_2_2(x_LL))
            # view is reshape
            if self.config["network"] == "cnn_imu":
                x_LL = x_LL.view(-1, x_LL.size()[1] * x_LL.size()[2] * x_LL.size()[3])
                x_LL = F.relu(self.fc3_LL(x_LL))
            elif self.config["network"] == "lstm":
                x_LL = x_LL.view(x_LL.size()[0], -1, x_LL.size()[1] * x_LL.size()[3])
                x_LL,_ = self.fc3_LL(x_LL)
            # N
            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_N = np.arange(0, 36)
                    idx_N = np.concatenate([idx_N, np.arange(36, 45)])
                    x_N = F.relu(self.conv_LA_1_1(x[:, :, :, idx_N]))
                elif self.config["dataset"] == 'pamap2':
                    idx_N = np.arange(0, 1)
                    idx_N = np.concatenate([idx_N, np.arange(14, 27)])
                    x_N = F.relu(self.conv_LA_1_1(x[:, :, :, idx_N]))
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_N = np.arange(0, 36)
                    idx_N = np.concatenate([idx_N, np.arange(36, 45)])
                    x_N = F.relu(self.conv_LA_1_1(x[:, :, :, idx_N]))
                elif self.config["dataset"] == 'pamap2':
                    idx_N = np.arange(0, 1)
                    idx_N = np.concatenate([idx_N, np.arange(14, 27)])
                    x_N = F.relu(self.conv_LA_1_1(x[:, :, :, idx_N]))
            x_N = F.relu(self.conv_N_1_2(x_N))
            x_N = F.relu(self.conv_N_2_1(x_N))
            x_N = F.relu(self.conv_N_2_2(x_N))
            # view is reshape
            if self.config["network"] == "cnn_imu":
                x_N = x_N.view(-1, x_N.size()[1] * x_N.size()[2] * x_N.size()[3])
                x_N = F.relu(self.fc3_N(x_N))
            elif self.config["network"] == "lstm":
                x_N = x_N.view(x_N.size()[0], -1, x_N.size()[1] * x_N.size()[3])
                x_N,_ = self.fc3_N(x_N)

            # RA
            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_RA = np.arange(0, 36)
                    idx_RA = np.concatenate([idx_RA, np.arange(54, 63)])
                    idx_RA = np.concatenate([idx_RA, np.arange(63, 72)])
                    x_RA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RA]))
                elif self.config["dataset"] == 'pamap2':
                    idx_RA = np.arange(1, 14)
                    x_RA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RA]))
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_RA = np.arange(0, 36)
                    idx_RA = np.concatenate([idx_RA, np.arange(54, 63)])
                    idx_RA = np.concatenate([idx_RA, np.arange(63, 72)])
                    x_RA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RA]))
                '''
                elif self.config["dataset"] == 'pamap2':
                    idx_RA = np.arange(1, 14)
                    x_RA = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RA]))
                '''
            if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                x_RA = F.relu(self.conv_RA_1_2(x_RA))
                x_RA = F.relu(self.conv_RA_2_1(x_RA))
                x_RA = F.relu(self.conv_RA_2_2(x_RA))
                # view is reshape
                x_RA = x_RA.view(-1, x_RA.size()[1] * x_RA.size()[2] * x_RA.size()[3])
                x_RA = F.relu(self.fc3_RA(x_RA))

            # RL
            if self.config["reshape_input"]:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_RL = np.arange(0, 36)
                    idx_RL = np.concatenate([idx_RL, np.arange(81, 97)])
                    x_RL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RL]))
                elif self.config["dataset"] == 'pamap2':
                    idx_RL = np.arange(27, 40)
                    x_RL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RL]))
            else:
                if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                    idx_RL = np.arange(0, 36)
                    idx_RL = np.concatenate([idx_RL, np.arange(81, 97)])
                    x_RL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RL]))
                '''
                elif self.config["dataset"] == 'pamap2':
                    idx_RL = np.arange(27, 40)
                    x_RL = F.relu(self.conv_LA_1_1(x[:, :, :, idx_RL]))
                '''

            if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                x_RL = F.relu(self.conv_RL_1_2(x_RL))
                x_RL = F.relu(self.conv_RL_2_1(x_RL))
                x_RL = F.relu(self.conv_RL_2_2(x_RL))
                # view is reshape
                x_RL = x_RL.view(-1, x_RL.size()[1] * x_RL.size()[2] * x_RL.size()[3])
                x_RL = F.relu(self.fc3_RL(x_RL))
                
            if self.config["dataset"] == 'locomotion' or self.config["dataset"] == 'gesture':
                x = torch.cat((x_LA, x_LL, x_N, x_RA, x_RL), 1)
            elif self.config["dataset"]=='pamap2':
                if self.config["network"] == "cnn_imu":
                    x = torch.cat((x_LA, x_LL, x_N), 1)
                elif self.config["network"]=="lstm":
                    x = torch.cat((x_LA, x_LL, x_N), 2)
        
        x = F.dropout(x, training=self.training)
        x = F.relu(self.fc4(x))
        if self.config["network"]=="cnn_imu":
            x = F.dropout(x, training=self.training)
            x = self.fc5(x)
        elif self.config["network"]=="lstm":
           x = F.dropout(x, training=self.training)
           x= x[:,-1,:]
           x = self.fc5(x) 
        
        if self.config['output'] == 'attribute':
            x = self.sigmoid(x)

        if not self.training:
            if self.config['output'] == 'softmax':
                x = self.softmax(x)

        return x
    
    def init_weights(self):
        self.apply(Network._init_weights_orthonormal)
        
        return
    
    @staticmethod
    def _init_weights_orthonormal(m):
        if isinstance(m, nn.Conv2d):
            #n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
            #m.weight.data.normal_(0, (2. / n) ** (1 / 2.0))
            nn.init.orthogonal_(m.weight, gain = np.sqrt(2))
            nn.init.constant_(m.bias.data, 0)
        if isinstance(m, nn.Linear):          
            nn.init.orthogonal_(m.weight, gain = np.sqrt(2))
            nn.init.constant_(m.bias.data, 0)
        
        return
     
    def size_feature_map(self, Wx, Hx, F, P, S, type_layer = 'conv'):
        
        if type_layer == 'conv':
            Wy = 1 + (Wx - F[0] + 2 * P) / S[0]
            Hy = 1 + (Hx - F[1] + 2 * P) / S[1]
        
        elif type_layer == 'pool':
            Wy = 1 + (Wx - F[0]) / S[0]
            Hy = 1 + (Hx - F[1]) / S[1]
                    
        return Wy, Hy
    