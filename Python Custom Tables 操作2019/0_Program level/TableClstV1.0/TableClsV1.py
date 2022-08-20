# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:59 2019
Reading from the custom table from PeriodCls series of programs.
Version 1.0
@author: Harry
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class TblC(object):
    
    def __init__(self, fname):
        self.fname = fname
        self.x_data_FullLength = self.ReadColumn(2)
        self.x_data_hours = self.ReadColumn(1)
        self.y_data_Slope = self.ReadColumn(4)
        self.x_data_FullLength_sorted, self.y_data_Slope_sorted = self.Organize()
        self.xhr_data_sorted, self.yhr_data_Slope_sorted = self.Organize(X = self.x_data_hours, Y = self.y_data_Slope)
        
        self.x_coord, self.y_avg = self.Statistics()[0]
        self.y_std = self.Statistics()[1][1]
        self.x_count = self.Statistics()[2]
        
        self.xhr_coord, self.yhr_avg = self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted )[0]
        self.yhr_std = self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted)[1][1]
        self.xhr_count = self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted)[2]
        
    def ReadColumn(self, column = 0):
        '''
        Table表格形式:
            FileName,	Hours(Roughly),	 Full Length,	 Half Length,	 Slope	,   Period,  AVG,	 Intercept, 	 R^2,  Std_Deviation
            0         1                2              3                4        5        6     7           8      9
        '''
        temp = 0
        if self.fname[-4:] =='.csv':
            temp = np.genfromtxt(self.fname, delimiter =',', usecols = column, skip_header =1)
        elif self.fname[-4:] =='.txt':
            temp = np.genfromtxt(self.fname, delimiter ='', usecols = column, skip_header =1)
        #print('read column temp = ', temp)
        return temp
    
    def Organize(self, X = None, Y = None):
        '''
        整理x y 序列，依x的大小重整排序，由x(橫軸，通常是full length的值)的小到大
        '''
        if X != None:
            x = X
        else:
            x = self.x_data_FullLength
        if Y != None:
            y = Y
        else:
            y = self.y_data_Slope
        
        dtype1 = [('x', float), ('y', float)]
        coord = np.array([(i[0], i[1]) for i in np.array([x,y]).T], dtype = dtype1)
        coord = np.sort(coord, order = 'x')
        coord = np.array([[i[0], i[1] ] for i in coord]).T
        #self.x_data_FullLength_sorted = coord[0]
        #self.y_data_Slope_sorted = coord[1]
        #return coord 形式: [[x0,x1...], [y0, y1...]]
        return coord
    
    def Statistics(self, Xd = None, Yd = None):
        '''
        輸入x, y
        吐出[x_coord, yavg], [xstd, ystd]
        '''
        xd, yd = self.x_data_FullLength_sorted, self.y_data_Slope_sorted
        if Xd!= None:  #用此判斷式順序的寫法，可以讓如果有提供Xd, Yd去複寫預設的xd, yd
            xd = Xd
        if Yd!= None:
            yd = Yd
        #x_ele = np.array([i for i in Counter(xd).keys()])
        #x_index = []
        #for j in range(0, len(x_ele)):
        #    for i in range(0, len(xd)):
        #        if xd[i] == x_ele[j]:
        #            x_index.append(i)
        x_count = [i for i in Counter(xd).values()]
        #print('x ele', x_ele)
        x_ele = np.array([i for i in Counter(xd).keys()])
        x_index_temp = [ [i for i in range(0, len(xd)) if xd[i] == x_ele[j] ] for j in range(0, len(x_ele))]
        x_index = np.hstack(x_index_temp)
#        print('x_index ', x_index)
        y_avg = [ np.average(yd[i]) for i in x_index_temp]
        y_std = [ np.std(yd[i])     for i in x_index_temp]
        x_yavg = np.vstack((x_ele, y_avg))
        x_ystd = np.vstack((x_ele, y_std))
#        print('x_yavg ', x_yavg)
        sts = [x_yavg, x_ystd, x_count]
        return sts
    
    def DrawTable(self, Xd = None, Yd = None, SaveFig = 0, ShowFig = 1, Connect_Line = None):
        '''
        繪圖器function本體
        預設為
            不跳過第一點 (=0)
            顯示完整擬合後的結果 (=1)
            不存圖       (=0)
        '''
#        xd, yd = self.Organize()
        xd, yd = self.x_data_FullLength_sorted, self.y_data_Slope_sorted
        if Xd!= None:
            xd = Xd
        if Yd!= None:
            yd = Yd

#        print('xd', xd)
#        print('yd', yd)
        fig1, ax1 = plt.subplots(1,1)
        fig1.set_size_inches([20,10])
        fig1.subplots_adjust(right = 1)
        fig1.suptitle('Length-Exponent Comparison from\n%s'%self.fname, fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
        #ax1.set_aspect('equal')
        ax1.set_aspect('auto')
        ax1.grid(True)
        ax1.set_title(self.fname+'\n')
        ax1.set_xlabel('Full Sequential Length of Source Data (num)')
        ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        
            #固定x y軸範圍
        #floor_x = np.round( self.xwindow_data_IntrinsicLowerLimit_log )
#        floor_y = np.floor( np.min(yd))
#        Lowlim_x = np.min(xd)
#        Lowlim_y = floor_y
#        ax1.set_xlim(Lowlim_x, 0)
#        ax1.set_ylim(Lowlim_y, 0)
                #繪製x 軸標示
        #xticks_new = np.arange(Lowlim_x, 0+1)  #因為normalization，使的範圍是由「最低可能頻率」到1
        #xlabels_new = [ str(np.power(self.log_to, i)) + '\n' + '%.f'%i for i in xticks_new ]
        #ax1.set_xticks(xticks_new)
        #ax1.set_xticklabels(xlabels_new)
                #繪製y 軸標示
        #yticks_new = np.arange(floor_y, 0+1)  #因為normalization，使的範圍是由最低值到1
        #ylabels_new = [ str(np.power(self.log_to, i)) + '\n' + '%.f'%i for i in yticks_new ]
        #ax1.set_yticks(yticks_new)
        #ax1.set_yticklabels(ylabels_new)
        
        
        #繪製數據點，點與線雙重疊圖
        if Connect_Line == True:
            ax1.plot( xd, yd, 'r', linewidth = 0.5)
        ax1.scatter( xd, yd, s = 3)
        return 0

    def DrawTableStatistics(self, Xd = None, Yd = None, YErr= None,SaveFig = 0, ShowFig = 1, Connect_Line = 1, Mode = 'Seq'):
        '''
        繪圖器function本體
        預設為
            不跳過第一點 (=0)
            顯示完整擬合後的結果 (=1)
            不存圖       (=0)
        '''
#        xd, yd = self.Organize()
        xd, yd = self.x_coord, self.y_avg
        yErr = self.y_std
        if Xd!= None:
            xd = Xd
        if Yd!= None:
            yd = Yd
        if YErr != None:
            yErr = YErr

#        print('xd', xd)
#        print('yd', yd)
        fig1, ax1 = plt.subplots(1,1)
        fig1.set_size_inches([20,10])
        fig1.subplots_adjust(right = 1)
        if Mode == 'Seq':
            fig1.suptitle('Statistics of Length-Exponent Comparison from\n%s'%self.fname, fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
            #ax1.set_aspect('equal')
            ax1.set_aspect('auto')
            ax1.grid(True)
            ax1.set_title(self.fname+'\n')
            ax1.set_xlabel('Full Sequential Length of Source Data (num)')
            ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        elif Mode == 'Hour':
            fig1.suptitle('Statistics of Hours-Exponent Comparison from\n%s'%self.fname, fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
            #ax1.set_aspect('equal')
            ax1.set_aspect('auto')
            ax1.grid(True)
            ax1.set_title(self.fname+'\n')
            ax1.set_xlabel('Approximated Time of Source Data (Hours)')
            ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        
            #固定x y軸範圍
        #floor_x = np.round( self.xwindow_data_IntrinsicLowerLimit_log )
#        floor_y = np.floor( np.min(yd))
#        Lowlim_x = np.min(xd)
#        Lowlim_y = floor_y
#        ax1.set_xlim(Lowlim_x, 0)
#        ax1.set_ylim(Lowlim_y, 0)
                #繪製x 軸標示
        #xticks_new = np.arange(Lowlim_x, 0+1)  #因為normalization，使的範圍是由「最低可能頻率」到1
        #xlabels_new = [ str(np.power(self.log_to, i)) + '\n' + '%.f'%i for i in xticks_new ]
        #ax1.set_xticks(xticks_new)
        #ax1.set_xticklabels(xlabels_new)
                #繪製y 軸標示
        #yticks_new = np.arange(floor_y, 0+1)  #因為normalization，使的範圍是由最低值到1
        #ylabels_new = [ str(np.power(self.log_to, i)) + '\n' + '%.f'%i for i in yticks_new ]
        #ax1.set_yticks(yticks_new)
        #ax1.set_yticklabels(ylabels_new)
        
        
        #繪製數據點，點與線雙重疊圖
        if Mode == 'Seq':
            x_count = self.x_count
        elif Mode == 'Hour':
            x_count = self.xhr_count
        for i in range(0, len(x_count)):
            ax1.annotate(x_count[i], (xd[i], yd[i]) , (xd[i], yd[i]), xycoords = 'data')
        ax1.errorbar(xd, yd, yerr = yErr, uplims=True, lolims=True, fmt = None, mfc = 'green')
        if Connect_Line == True:
            ax1.plot( xd, yd, 'r', linewidth = 1.3)
        ax1.scatter( xd, yd, s = 8)
        
        return 0
    
    def RunInitiate(self):
        self.DrawTable()
        self.DrawTableStatistics()
        self.DrawTableStatistics(Xd= self.xhr_coord, Yd= self.yhr_avg, YErr= self.yhr_std, Mode= 'Hour')
        return 0