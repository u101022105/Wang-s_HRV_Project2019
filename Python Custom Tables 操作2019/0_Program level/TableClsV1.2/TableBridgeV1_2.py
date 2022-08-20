# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:36:04 2019
Table cls series bridge
Version 1.2
@author: Harry
"""

import TableClsV1_2 as TbleCls
import numpy as np
import matplotlib.pyplot as plt
import os as os
import sys as sys

folder ='Period_data_pack folder'
path1 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'+'\\'+folder + '\\Period_data_pack folder'
path2 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'
path = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'

class TblB(object):
    def __init__(self, Session_Folder, SaveFig= 0, ShowFig = 1, SaveCombinedFig =0, ShowCombinedFig= 1, Path1 = path, Path2 = path):
        self.Session_Folder = Session_Folder
        #self.flst = self.TblBridge1()[0][0]
        self.profile = self.TblBridge1()
        self.SaveFig = SaveFig
        self.ShowFig = ShowFig
        self.SaveCombinedFig = SaveCombinedFig
        self.ShowCombinedFig = ShowCombinedFig 
        
    def TblBridge1(self, Session_Folder = '', Mode = 'Hour', Folder = 'Period_data_pack folder', Fname = 'none', SaveFig= 0, ShowFig = 0, Path1 = path, Path2 = path):
        '''
        兩種模式，輸入fname來讀特定檔名
        不輸入模式則自動跑過預設資料夾中的所有檔案
        傳回 numpy陣列 [ [檔名1, TbleC_obj1], [檔名2, TbleC_obj2],... ]
        '''
#        if self.SaveFig != SaveFig:
#            SaveFig = self.SaveFig
#        if self.ShowFig != ShowFig:
#            ShowFig = self.ShowFig
        
        if Session_Folder =='none':
            print('Please direct the program with the session folder\'s name')
            
        Path1 = path+ '\\'+ self.Session_Folder+ '\\'+ Folder
        Path2 = path + '\\'+ self.Session_Folder
        if Fname != 'none':
            os.chdir(Path1)
            obj = TbleCls(Fname)
            temp2 = [obj.RunInitiate(Mode = Mode, SaveFig = SaveFig, ShowFig = ShowFig)]
            temp = np.array([Fname, obj])
            os.chdir(Path2)
        else:
            os.chdir(Path1)
            flst = os.listdir()
            os.chdir(Path2)
            obj_lst = []
            temp2 = []
            temp2hr = []
            x_clst =[]
            xhr_clst =[]
            for i in range(0, len(flst)):
                os.chdir(Path1)
                obj = TbleCls.TblC(flst[i])
                os.chdir(Path2)
                t2_hdl = obj.RunInitiate(Mode = Mode, SaveFig = SaveFig, ShowFig = ShowFig)
                temp2.append( t2_hdl[0])
                temp2hr.append( t2_hdl[1])
                obj_lst.append(obj)
                x_clst.append(obj.x_count)
                xhr_clst.append(obj.xhr_count)
            temp = np.array((flst, obj_lst))
#        self.x_c, self.y_a, self.y_std = np.array(temp2)
#        self.xhr_c, self.yhr_a, self.yhr_std = np.array(temp2hr).T
        self.x_count = x_clst
        self.xhr_count = xhr_clst
        #print('files: ', flst)
        return [temp, [temp2, temp2hr]]
    
    
    
    def DrawTableCombinedSource(self, Flst, Xd = 'none', Yd = 'none', YErr= 'none', XCount = 'none',SaveFig = 0, SaveCombinedFig = 0, ShowCombinedFig= 1, ShowFig = 1, Connect_Line = 1, Mode = 'Seq'):
        '''
        繪圖器function本體
        預設為
            不跳過第一點 (=0)
            顯示完整擬合後的結果 (=1)
            不存圖       (=0)
        '''
        xd, yd = Xd, Yd
        yErr = YErr
        xCount = XCount
        fig1 = plt.figure()
        fig1.set_size_inches([20*1.2,10*1.2])
        fname_4tilte = ''
        if len(Flst)<=4:
            for i in Flst:
                fname_4tilte = fname_4tilte + str(i)+'\n'
        else:
            fname_4tilte = 'From multiple Tables in folder %s'%(self.Session_Folder)
        fname_4tilte = fname_4tilte+'\n\n'
        #print(fname_4tilte)
        if Mode == 'Seq':
            subp_ttle = 'Length'
            ttl_txt = 'Length - Exponent Graph\n'
            xlb_txt = 'Full Sequential Length of Source Data (num)'
            ylb_txt = 'Exponent of the Fitting\n of Corresponding Data'
            #xd, yd = self.x_c, self.y_a
            #yErr = self.y_std
            #xcount = self.x_count
            
        elif Mode == 'Hour':
            subp_ttle = 'Time'
            ttl_txt = 'Time(hour) - Exponent Graph\n'
            xlb_txt = 'Approximated Time of Source Data (Hours)'
            ylb_txt = 'Exponent of the Fitting\n of Corresponding Data'
            #xd, yd = self.xhr_c, self.yhr_a
            #yErr = self.yhr_std
            #xhrcount = self.xhr_count
            #xcount = xhrcount
            
            
        fig1.subplots_adjust(right = 1)
        fig1.suptitle('Statistics of {:>7s}-Exponent Comparison \n%s'.format(subp_ttle)%(fname_4tilte), fontsize = 24, fontweight = 'bold', x = 0.6, y = 1.02)
        ax1 = fig1.add_subplot(111)
        ax1.set_title(ttl_txt, fontsize =20 )
        ax1.tick_params(axis='both', which='major', labelsize=14)
        #learned from https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
        ax1.set_xlabel(xlb_txt,fontsize = 18)
        ax1.set_ylabel(ylb_txt,fontsize = 18)
        ax1.set_aspect('auto')
        ax1.grid(True)
        ax_lst = []
        for i in range(0, len(Xd)):
            xd = Xd[i]
            yd = Yd[i]
            yErr = YErr[i]
            xcount = xCount[i]
            ax_lst.append( fig1.add_subplot(111))
            current_line = ax_lst[i].scatter( xd, yd, s = 15, label = str(Flst[i][:-4]))
            cur_color = current_line.get_facecolor()[0]
            if Connect_Line == True:
                ax_lst[i].plot( xd, yd, c = cur_color, linewidth = 1.3)  
            for j in range(0,len(xd)):
                ax1.annotate(xcount[j], (xd[j], yd[j]) , (xd[j], yd[j]), xycoords = 'data', fontsize = 12)
            ax_lst[i].errorbar(xd, yd, yerr = yErr, uplims= True, lolims = True, fmt = 'none', mfc = cur_color)
        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize = 16)
        #learned form https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        #ax1.legend(loc = 'lower right')
        if Mode == 'Seq':
            if SaveCombinedFig == 1:
                fig1.savefig('Length-Exponent Combined Comparison %s Graph.png'%self.Session_Folder, dpi = fig1.dpi, bbox_inches='tight')
                print('From DrawTableCombinedSource, Graph was saved.\n')
        elif Mode == 'Hour':
            if SaveCombinedFig == 1:
                fig1.savefig('Hours-Exponent Combined Comparison %s Graph.png'%self.Session_Folder, dpi = fig1.dpi, bbox_inches='tight')
                print('From DrawTableCombinedSource, Graph was saved.\n')    
        
        if ShowCombinedFig ==0:
            plt.close()
        return 0
    
    
    
class HidePrint:
    '''
    to suppress specific print in parts of the code.
    learned from:
    https://stackoverflow.com/
    questions/8391411/suppress-calls-to-print-python
    '''
    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = open( os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self.original_stdout
    