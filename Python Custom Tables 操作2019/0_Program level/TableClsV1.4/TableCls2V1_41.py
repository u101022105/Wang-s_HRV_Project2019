# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 16:12:19 2019
version 1.4
@author: Harry
"""

import os as os
import numpy as np
import matplotlib.pyplot as plt
import TableClsV1_4 as TblC1
from io import StringIO
from collections import Counter
from collections.abc import Iterable

class TblC2(TblC1.TblC):
    '''
    path is a dictionary {'Path_in':, 'Path_out':, 'Path_neutral':}
    FileName	Hours(Roughly)	Full Length of current data	 Half Length	Slope	Period AVG	Intercept	R^2	Std_Deviation	Left Position	Right Position(ref to original data)
    0816_DEP_on_Plat_Can.csv_S1										
    0816_DEP_on_Plat_Can.csv	2.4	 10000	 5000	-0.459461465	 0.84630869	-4.458539352	-0.191876407	0.174679819	100	10100
    '''
    def __init__(self, fname, Path= ''):
        self.fname = fname
        self.path = Path
        

    def Read_Data(self, fname = '', SkipHeader = 0, path_in='', path_out='', path_neu =''):
        '''
        Table表格形式:
            FileName	Hours(Roughly)	Full Length      Half Length	  Slope	 Period AVG	Intercept	  R^2	        Std_Deviation	 Left Pos 	Right Pos
            0         1                2              3                4        5          6          7           8              9          10
        '''
        if path_in=='':
            path_in = self.path['Path_in']
        if path_out=='':
            path_out = self.path['Path_out']
        if path_neu=='':
            path_neu = self.path['Path_neutral']
        
        if fname == '':
            fname = self.fname
        else:
            fname = fname
        #temp = 0
        #names  = []
        #ndtype = ('U30', float, float, float, float, float, float, float, float, float, float, str)
        ndtype = ('U30', float, float, float, float, float, float, float, float, float, float)
        SkipHeader = SkipHeader
        if fname[-4:] =='.csv':
            dlmt = ','
        elif fname[-4:] =='.txt':
            dlmt = ''
        else:
            print('Folder Structure was not aligned with the design.')
        os.chdir(path_in)
        mis_dict = {'empty':'','newline':'\n'}
        fil_dict = {'empty':'X', 'newline':'N'}
        #convert_rule = lambda f: f.decode()
        #data_matrix = np.genfromtxt(fname, delimiter = dlmt, skip_header = SkipHeader, names = True, dtype = ndtype, converters = {'FileName':convert_rule}, missing_values = mis_dict, filling_values = fil_dict)
        data_matrix = np.genfromtxt(fname, delimiter = dlmt, skip_header = SkipHeader, names = True, dtype = ndtype, missing_values = mis_dict, filling_values = fil_dict)
        profile = (fname, path_in, path_out, path_neu)
        #data_matrix_mask = np.genfromtxt(fname, delimiter = dlmt, skip_header = SkipHeader, names = True, dtype = ndtype, missing_values = mis_dict, filling_values = fil_dict, usemask = True)
        os.chdir(path_neu)
        data_matrix_mask = []
        return data_matrix, data_matrix_mask, profile
    
    
    def Seperate_Data(self, data_m, profile):
        data_matrix                        = data_m
        fname, path_in, path_out, path_neu = profile
        col0 = data_matrix['FileName']
        col1 = data_matrix['Slope']
        dtype_n = data_matrix.dtype
        print(dtype_n)
        index = []
        one_slice   = []
        data_slices = []  
        for i in range(0, len(col1)):
            if np.isnan(col1[i]) == True:
                index.append(i)
        index = [i for i in index] #(因為我的csv的結構，使得index =0其實是表格在不看header下的第二列)
        index.append(len(col0))
        ln_ind = len(index)
#        file_tag = [col0[index[i]+1].decode() for i in range(0, ln_ind-1 )]
        file_tag = [col0[index[i]+1] for i in range(0, ln_ind-1 )]
        print('File name as \n{:<65s}'.format(str(file_tag)))
        #print('Row1 name %s'%str(data_matrix[1]) )
        one_slice   = []
        data_slices = []
        for i in range(0, ln_ind-1):
            one_slice   = [file_tag[i]]
            #slice_ele   = data_matrix[index[i]+1:index[i+1]]
            slice_ele   = data_matrix[index[i]+1:index[i+1]]
            one_slice.append(slice_ele)
            #print('LEN ONESLICE',index[i+1]-index[i]-1)
            data_slices.append(one_slice)
        #print(index)
        #print(data_slices[0])      
        return data_slices, file_tag
    
    
    def Org_Stat(self, Xd = '', Yd = ''):
        '''
        運用cls1的排序和統計，回傳統計過後的各檔案的數值
        [x_yavg, x_ystd, x_count] = Sts
        '''
        Coord = self.Organize(X = Xd, Y = Yd)
        X_1, Y_1 = Coord
        Sts = self.Statistics(Xd = X_1, Yd = Y_1)
        #[x_yavg, x_ystd, x_count] = Sts
        return Coord, Sts
       
    def Save_sep(self, Data_slices, FileTags, Path = []):
        '''
        save Data slices from one target file.
        '''
        if Path != []:
            Path = Path
            Path_res = Path['Path_out']
        else:
            Path_res = self.path['Path_out']
        
        #cus_fmt = ''.join(['%s']+ [',%f']*10 + [',%s'])
        cus_fmt = ''.join(['%s']+ [',%f']*10)
        
        cur_path = os.getcwd()
        os.chdir(Path_res)
        if os.path.exists(str(self.fname)[:-4]) != True:
            os.mkdir(str(self.fname)[:-4])
        os.chdir(str(self.fname)[:-4])
        hd = ['FileName','	Hours(Roughly)','	Full Length of current data',	 'Half Length',	'Slope',	'Period AVG',	'Intercept'	,'R^2',	'Std_Deviation',	'Left Position',	'Right Position (ref to original data)	']
        
        temp = ''
        for i in hd:
            temp+= i.strip()+','
        hd = temp[:-1]
        
        for i in range(0, len(FileTags)):
            #for j in range(0, len(Data_slices[i]))
            #print('\n####DataSlices\n', Data_slices[i][1][0:12])
            #print('\n####DataSlices\n', np.shape(Data_slices[i][1][0:12]))
            np.savetxt(FileTags[i][:-4]+'.csv', Data_slices[i][1], fmt = cus_fmt, delimiter= ',', header = hd)
#            np.savetxt(FileTags[i], Data_slices[i][1], delimiter= ',', header = hd)
        os.chdir(cur_path)
        return 0
    
    def Save_avg(self, Data_avgs, FileTags, Path = [], hd = ''):
        '''
        save Data slices from one target file.
        '''
        if Path != []:
            Path = Path
            Path_res = Path['Path_out']
        else:
            Path_res = self.path['Path_out']
        
        #cus_fmt = ''.join(['%s']+ [',%f']*10 + [',%s'])
        cus_fmt = ''.join(['%d']+ [',%f']*2 +[',%d'])
        
        cur_path = os.getcwd()
        os.chdir(Path_res)
        if os.path.exists(str(self.fname)[:-4]) != True:
            os.mkdir(str(self.fname)[:-4])
        os.chdir(str(self.fname)[:-4])
        if hd =='':
            hd = ['Full Length','Slope AVG', 'Std_Deviation AVG', 'Amount of Data points for this AVG']
        else:
            hd = hd
        temp = ''
        for i in hd:
            temp+= i.strip()+','
        hd = temp[:-1]
        
        Data_avgs = np.array(Data_avgs).T
        
        for i in range(0, len(FileTags)):
            np.savetxt(FileTags[i][:-4]+'_avg.csv', Data_avgs, fmt = cus_fmt, delimiter= ',', header = hd)
        os.chdir(cur_path)
        return 0
    
    def Run_ini(self, fname = '', SkipHeader = 0, path_in='', path_out='', path_neu ='', Mode = 'Seq', SaveFig= 0,ShowFig= 0, Save_each = 1, Save_avg =1):
        '''
        可以被提取的資訊有
        Data_Slices, FileTags per File
        [Xd, Xhr, Yd, YErr, obj] per FileTag
        Sts_per_filetag = self.RunInitiate_refresh 得到的是 序列 及 小時 兩版本的 x, y_avg, y_std, x_count
        [[self.x_coord, self.y_avg, self.y_std, self.x_count],[self.xhr_coord, self.yhr_avg, self.yhr_std, self.xhr_count]]
        '''
        if path_in=='':
            path_in = self.path['Path_in']
        if path_out=='':
            path_out = self.path['Path_out']
        if path_neu=='':
            path_neu = self.path['Path_neutral']
        Data_Matrix, Data_Matrix_Mask, Profile = self.Read_Data(fname = fname, SkipHeader = SkipHeader, path_in=path_in, path_out=path_out, path_neu =path_neu)
        Data_Slices, FileTags = self.Seperate_Data(Data_Matrix, Profile)
        
        if Save_each == 1:
            self.Save_sep(Data_Slices, FileTags)
        
        Sts_for_filetags = []
        for i in range(0, len(FileTags)):
            #print('curr iter i: {:>10s}'.format(str(i)))
            #obj = TblC1.TblC(FileTags[i])
            #print(Data_Slices[i][1])
            Xd = Data_Slices[i][1]['Full_Length_of_current_data']
            #print(len(Xd),'\nnext')
            Xhr = Data_Slices[i][1]['HoursRoughly']
            Yd = Data_Slices[i][1]['Slope']
            YErr = Data_Slices[i][1]['Std_Deviation']
            Sts_per_filetag = self.RunInitiate_refresh(Mode = Mode, SaveFig= SaveFig,ShowFig=ShowFig, Xd = Xd, Xhr = Xhr, Yd = Yd)
            Sts_for_filetags.append(Sts_per_filetag)
            #Raw_out_per_tag = [Xd, Xhr, Yd, YErr, obj]
        if Save_avg ==1:
            if Mode == 'Seq':
                print('TEST', Sts_per_filetag[0])
                Data_Avg = Sts_per_filetag[0]
            elif Mode == 'Hour':
                Data_Avg = Sts_per_filetag[1]              
            self.Save_avg(Data_Avg, FileTags)
        
        return Sts_for_filetags, FileTags
    

#TblC2.Run_ini()
    