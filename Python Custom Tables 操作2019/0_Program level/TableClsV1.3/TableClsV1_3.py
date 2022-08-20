# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:59 2019
Reading from the custom table from PeriodCls series of programs.
Version 1.3
@author: Harry
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from collections.abc import Iterable

class TblC(object):
    def __init__(self, fname):
        self.fname = fname
        print('\n',self.fname)
        self.x_data_FullLength = self.ReadColumn(2)
        self.x_data_hours = self.ReadColumn(1)
        self.y_data_Slope = self.ReadColumn(4)
        if np.size(self.x_data_FullLength) <2:
            print('This Table only contains 1 dataset, please be aware.')
        #print('Organizing along Seq')
        self.x_data_FullLength_sorted, self.y_data_Slope_sorted = self.Organize()
        #print('Organizing along Hour')
        self.xhr_data_sorted, self.yhr_data_Slope_sorted = self.Organize(X = self.x_data_hours, Y = self.y_data_Slope)
        
        [A,B,C] = self.Statistics()
        self.x_coord, self.y_avg = A
        self.y_std = B[1]
        self.x_count = C
#        self.x_coord, self.y_avg = self.Statistics()[0]
#        self.y_std = self.Statistics()[1][1]
#        self.x_count = self.Statistics()[2]
        
        [A,B,C]= self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted)
        #[[xcrd,ya],[xc_again,std],[xcnt]] = [A,B,C]
        self.xhr_coord, self.yhr_avg = A
        self.yhr_std = B[1]
        self.xhr_count = C
#        self.xhr_coord, self.yhr_avg = self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted )[0]
#        self.yhr_std = self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted)[1][1]
#        self.xhr_count = self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted)[2]
        
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
    
    def Organize(self, X = 'none', Y = 'none'):
        '''
        整理x y 序列，依x的大小重整排序，由x(橫軸，通常是full length的值)的小到大
        '''
        if X != 'none':
            x = X
        else:
            x = self.x_data_FullLength
        if Y != 'none':
            y = Y
        else:
            y = self.y_data_Slope
        
        dtype1 = [('x', float), ('y', float)]
        while True:
            try:
                coord = np.array([(i[0], i[1]) for i in np.array([x,y]).T], dtype = dtype1)
                coord = np.sort(coord, order = 'x')
                coord = np.array([[i[0], i[1] ] for i in coord]).T
                #return coord 形式: [[x0,x1...], [y0, y1...]]
                break
            except IndexError:
                #print('There\'s only 1 dataset in this file, which would cause problem.')
                coord = np.array([x, y])
                break
        #print('x',x,'\ny',y)       
        return coord
    
    def Statistics(self, Xd = 'none', Yd = 'none'):
        '''
        輸入x, y
        吐出[x_coord, yavg], [xstd, ystd]
        '''
        xd, yd = self.x_data_FullLength_sorted, self.y_data_Slope_sorted
        if Xd!= 'none':  #用此判斷式順序的寫法，可以讓如果有提供Xd, Yd去複寫預設的xd, yd
            xd = Xd
        if Yd!= 'none':
            yd = Yd
        if isinstance(xd, Iterable):
            x_count = [i for i in Counter(xd).values()]
            x_ele = np.array([i for i in Counter(xd).keys()])
            x_index_temp = [ [i for i in range(0, len(xd)) if xd[i] == x_ele[j] ] for j in range(0, len(x_ele))]
            x_index = np.hstack(x_index_temp)
            y_avg = [ np.average(yd[i]) for i in x_index_temp]
            y_std = [ np.std(yd[i])     for i in x_index_temp]
            x_yavg = np.vstack((x_ele, y_avg))
            x_ystd = np.vstack((x_ele, y_std))
            sts = [x_yavg, x_ystd, x_count]
        else:
            #print('Be Aware, this file only contain one datapoint. The statistics performed on it is just a placeholder here.')
            x_count = [1]
            x_yavg = np.vstack((xd, yd))
            x_ystd = np.vstack((xd, 0))
            sts = [x_yavg, x_ystd, x_count]
        return sts
    
    def DrawTable(self, Xd = 'none', Yd = 'none', SaveFig = 0, ShowFig = 1, Connect_Line = 'None'):
        '''
        繪圖器function本體
        預設為
            不跳過第一點 (=0)
            顯示完整擬合後的結果 (=1)
            不存圖       (=0)
        '''
        xd, yd = self.x_data_FullLength_sorted, self.y_data_Slope_sorted
        if Xd!= 'none':
            xd = Xd
        if Yd!= 'none':
            yd = Yd

        fig1, ax1 = plt.subplots(1,1)
        fig1.set_size_inches([20,10])
        fig1.subplots_adjust(right = 1)
        fig1.suptitle('Length-Exponent Comparison from\n%s'%self.fname, fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
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
        
        if SaveFig == 1:
            fig1.savefig('Length-Exponent %s Graph.png'%self.fname[:-4], dpi = fig1.dpi, bbox_inches='tight')
            print('Graph was saved.\n')
        
        if ShowFig ==0:
            plt.close()
        return 0

    def DrawTableStatistics(self, Xd = 'none', Yd = 'none', YErr= 'none',SaveFig = 0, ShowFig = 1, Connect_Line = 1, Mode = 'Seq'):
        '''
        繪圖器function本體
        預設為
            不跳過第一點 (=0)
            顯示完整擬合後的結果 (=1)
            不存圖       (=0)
        '''
        if Mode == 'Seq':
            xd, yd = self.x_coord, self.y_avg
            yErr = self.y_std
        elif Mode == 'Hour':
            xd, yd = self.xhr_coord, self.yhr_avg
            yErr = self.yhr_std
        if Xd!= 'none':
            xd = Xd
        if Yd!= 'none':
            yd = Yd
        if YErr != 'none':
            yErr = YErr
        fig1, ax1 = plt.subplots(1,1)
        fig1.set_size_inches([20,10])
        fig1.subplots_adjust(right = 1)
        if Mode == 'Seq':
            fig1.suptitle('Statistics of Length-Exponent Comparison from\n%s'%self.fname, fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
            ax1.set_aspect('auto')
            ax1.grid(True)
            ax1.set_title(self.fname+'\n')
            ax1.set_xlabel('Full Sequential Length of Source Data (num)')
            ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        elif Mode == 'Hour':
            fig1.suptitle('Statistics of Hours-Exponent Comparison from\n%s'%self.fname, fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
            ax1.set_aspect('auto')
            ax1.grid(True)
            ax1.set_title(self.fname+'\n')
            ax1.set_xlabel('Approximated Time of Source Data (Hours)')
            ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        
        #繪製數據點，點與線雙重疊圖
        if Mode == 'Seq':
            xCount = self.x_count
        elif Mode == 'Hour':
            xCount = self.xhr_count
        for i in range(0, len(xCount)):
            ax1.annotate(xCount[i], (xd[i], yd[i]) , (xd[i], yd[i]), xycoords = 'data')
        ax1.errorbar(xd, yd, yerr = yErr, uplims=True, lolims=True, fmt = 'none', mfc = 'green')
        if Connect_Line == True:
            ax1.plot( xd, yd, 'r', linewidth = 1.3)
        ax1.scatter( xd, yd, s = 8)
        
        if Mode == 'Seq':
            if SaveFig == 1:
                fig1.savefig('Length-Exponent %s Graph.png'%self.fname[:-4], dpi = fig1.dpi, bbox_inches='tight')
                print('From DrawTableStatistics, Graph was saved.\n')
        elif Mode == 'Hour':
            if SaveFig == 1:
                fig1.savefig('Hours-Exponent %s Graph.png'%self.fname[:-4], dpi = fig1.dpi, bbox_inches='tight')
                print('From DrawTableStatistics, Graph was saved.\n')
            
        if ShowFig ==0:
            plt.close()
        return 0
    
    
        
    
    def RunInitiate(self, Mode = 'Hour', SaveFig = 0, ShowFig = 1):
#        self.DrawTable()
#        self.DrawTableStatistics()
        #self.DrawTableStatistics(Xd= self.xhr_coord, Yd= self.yhr_avg, YErr= self.yhr_std, Mode= Mode, SaveFig = SaveFig, ShowFig = ShowFig)
        self.DrawTableStatistics(Mode= Mode, SaveFig = SaveFig, ShowFig = ShowFig)
        return [[self.x_coord, self.y_avg, self.y_std, self.x_count],[self.xhr_coord, self.yhr_avg, self.yhr_std, self.xhr_count]]
    
    
    def RunInitiate_refresh(self, Mode = 'Hour', SaveFig = 0, ShowFig = 1, Xd = '', Xhr = '', Yd = ''):
        self.x_data_FullLength = Xd
        self.x_data_hours = Xhr
        self.y_data_Slope = Yd
        if np.size(self.x_data_FullLength) <2:
            print('This Table only contains 1 dataset, please be aware.')
        #print('Organizing along Seq')
        self.x_data_FullLength_sorted, self.y_data_Slope_sorted = self.Organize()
        #print('Organizing along Hour')
        self.xhr_data_sorted, self.yhr_data_Slope_sorted = self.Organize(X = self.x_data_hours, Y = self.y_data_Slope)
        
        [A,B,C] = self.Statistics()
        self.x_coord, self.y_avg = A
        self.y_std = B[1]
        self.x_count = C
        
        [A,B,C]= self.Statistics(self.xhr_data_sorted, self.yhr_data_Slope_sorted)
        self.xhr_coord, self.yhr_avg = A
        self.yhr_std = B[1]
        self.xhr_count = C
        self.DrawTableStatistics(Mode= Mode, SaveFig = SaveFig, ShowFig = ShowFig)
        return [[self.x_coord, self.y_avg, self.y_std, self.x_count],[self.xhr_coord, self.yhr_avg, self.yhr_std, self.xhr_count]]