# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:36:04 2019
Table cls series bridge
Version 1.1
@author: Harry
"""

import TableClsV1_1 as TbleCls
import numpy as np
import matplotlib.pyplot as plt
import os as os

folder ='Period_data_pack folder'
path1 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'+'\\'+folder + '\\Period_data_pack folder'
path2 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'
path = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'


def TblBridge1( Session_Folder = 'none', Folder = 'Period_data_pack folder', Fname = 'none', SaveFig= 0, ShowFig = 1, Path1 = path, Path2 = path):
    '''
    兩種模式，輸入fname來讀特定檔名
    不輸入模式則自動跑過預設資料夾中的所有檔案
    傳回 numpy陣列 [ [檔名1, TbleC_obj1], [檔名2, TbleC_obj2],... ]
    '''
    
    if Session_Folder =='none':
        print('Please direct the program with the session folder\'s name')
        
    Path1 = path+ '\\'+ Session_Folder+ '\\'+ Folder
    Path2 = path
    if Fname != 'none':
        os.chdir(Path1)
        obj = TbleCls(Fname)
        temp2 = [obj.RunInitiate(SaveFig = SaveFig, ShowFig = ShowFig)]
        temp = np.array([Fname, obj])
        os.chdir(Path2)
    else:
        os.chdir(Path1)
        flst = os.listdir()
        os.chdir(Path2)
        obj_lst = []
        temp2 = []
        for i in range(0, len(flst)):
            os.chdir(Path1)
            obj = TbleCls.TblC(flst[i])
            os.chdir(Path2)
            temp2.append( obj.RunInitiate(SaveFig = SaveFig, ShowFig = ShowFig))
            obj_lst.append(obj)
        temp = np.array((flst, obj_lst))
    #print('files: ', flst)
    return [temp, temp2]



def DrawTableCombinedSource( Flst, Xd = 'none', Yd = 'none', YErr= 'none',SaveFig = 0, SaveCombinedFig = 0, ShowFig = 1, Connect_Line = 1, Mode = 'Seq'):
    '''
    繪圖器function本體
    預設為
        不跳過第一點 (=0)
        顯示完整擬合後的結果 (=1)
        不存圖       (=0)
    '''
    xd, yd = Xd, Yd
    yErr = YErr
    fig1 = plt.figure()
    fig1.set_size_inches([20,10])
    fname_4tilte = ''
    for i in Flst:
        fname_4tilte = fname_4tilte + str(i)+'\n'
    print(fname_4tilte)
    if Mode == 'Seq':
        fig1.subplots_adjust(right = 1)
        fig1.suptitle('Statistics of Length-Exponent Comparison from\n%s'%(fname_4tilte), fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
        ax1 = fig1.add_subplot(111)
        ax1.set_xlabel('Full Sequential Length of Source Data (num)')
        ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        ax1.set_aspect('auto')
        ax1.grid(True)
        ax_lst = []
        for i in range(0,len(Xd)):
            ax_lst.append( fig1.add_subplot(111))
            ax_lst[i].errorbar(xd[i], yd[i], yerr = yErr[i], uplims= True, lolims = True, fmt = None, mfc = 'green')
            if Connect_Line == True:
                ax_lst[i].plot( xd[i], yd[i], 'r', linewidth = 1.3)
            ax_lst[i].scatter( xd[i], yd[i], s = 8, label = str(Flst[i][:-4]))
        ax1.legend(loc = 'upper right')

    elif Mode == 'Hour':
        fig1.subplots_adjust(right = 1)
        fig1.suptitle('Statistics of Hours-Exponent Comparison from\n%s'%(fname_4tilte), fontsize = 20, fontweight = 'bold', x = 0.7, y = 1.02)
        ax1 = fig1.add_subplot(111)
        ax1.set_xlabel('Approximated Time of Source Data (Hours)')
        ax1.set_ylabel('Exponent of the Fitting\n of Corresponding Data')
        ax1.set_aspect('auto')
        ax1.grid(True)
        ax_lst = []
        for i in range(0, len(Xd)):
            ax_lst.append( fig1.add_subplot(111))
            ax_lst[i].errorbar(xd[i], yd[i], yerr = yErr[i], uplims= True, lolims = True, fmt = None, mfc = 'green')
            if Connect_Line == True:
                ax_lst[i].plot( xd[i], yd[i], 'r', linewidth = 1.3)
            ax_lst[i].scatter( xd[i], yd[i], s = 8, label = str(Flst[i][:-4]))
        ax1.legend(loc = 'upper right')
    
    if SaveCombinedFig == 1:
        fig1.savefig('PSD %s Graph.png'%fname, dpi = fig1.dpi, bbox_inches='tight')
        print('Graph was saved.\n')
    
    if ShowFig ==0:
        plt.close()
    return 0