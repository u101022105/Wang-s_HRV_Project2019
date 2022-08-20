# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:59 2019
Reading from the custom table from PeriodCls series of programs.
Version 1.3
@author: Harry
"""
import os as os
import warnings as warnings
import numpy as np
import TableClsV1_3 as TbleC
import TableCls2V1_3 as TbleC2
import TableBridgeV1_3 as TbleBridge
from collections import Counter

proj_folder    = 'project 0802 aftn'
ses_folder     = 'ses0802'
ses_folder_out = 'ses0802'+'_out1'
name_folder    = 'PSD of Catas 0802'
path_general   = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'
path_neutral   = path_general+'\\' + proj_folder
path_in_par    = path_neutral+'\\' + 'Source' +'\\'+ ses_folder
path_in        = path_neutral+'\\' + 'Source' +'\\'+ ses_folder + '\\'+ name_folder
path_res       = path_neutral+'\\' + 'Result'
path_out_par   = path_neutral+'\\' + 'Result' +'\\'+ ses_folder_out 
path_out       = path_neutral+'\\' + 'Result' +'\\'+ ses_folder_out + '\\'+ name_folder 


def func2():
    path = {'Path_in':path_in, 'Path_out':path_out,'Path_neutral':path_neutral}
    #os.chdir(path_in)
    #flst = os.listdir()
    obj1 = TbleC2.TblC2('TableDEP_Can_S1 - test.csv', path = path)
    data_slices = obj1.Run_ini()
    return data_slices

#func2()

def func3():
    #mode = 'Hour'
    #mode = 'Seq'
    showCombinedFig =1
    saveCombinedFig =0
    showFig = 0
    saveFig = 0
    #mode = ['Hour']
    #mode = ['Seq']
    MODE = ['Seq', 'Hour']
    path = {'Path_in':path_in, 'Path_out':path_out,'Path_neutral':path_neutral}
    
    os.chdir(path_res)
    if os.path.exists(path_out_par) == False:
        os.mkdir(ses_folder_out)
        if os.path.exists(path['Path_out']) == False:
            os.chdir(path_out_par)
            os.mkdir(name_folder )
    os.chdir(path_neutral)

    for md in range(0, len(MODE)):
        
        mode = MODE[md]
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            with TbleBridge.HidePrint():
                ObjB = TbleBridge.TblB2(Session_Folder= proj_folder, Path= path)
                print('Things inside this with loop won\'t be printed')
            #Obj_hndl = ObjB.TblBridge2(Mode= mode, ShowFig= showFig, SaveFig = saveFig)
            print('-'*50)
            Flst = os.listdir(path_in)
            for i in range(0, len(Flst)):
                Obj_hndl2 = TbleC2.TblC2(Flst[i], Path = path)
                Data_Slices, xd, xhr, yd, yErr, obj, FileTags = Obj_hndl2.Run_ini(Mode = mode, ShowFig = showFig, SaveFig= saveFig)
                #with TbleBridge.HidePrint():
                #提醒 
                #obj[1] = temp2 = [[self.x_coord, self.y_avg, self.y_std],[self.xhr_coord, self.yhr_avg, self.yhr_std]] for [data1, data2, data3]
                Flst = FileTags
                #Objlst = Obj_hndl[0][1]
#                    if mode == 'Seq':
#                        Obj_temp = np.array(Obj_hndl[1][0])
#                    elif mode == 'Hour':
#                        Obj_temp = np.array(Obj_hndl[1][1])
                xd = list(xd)
                yd =list(yd)
                yErr = list(yErr)
                Xd    = []
                Yd    = []
                YErr  = []
                XCount = []
#                Xd    = xd
#                Yd    = yd
#                YErr  = yErr
#                XCount = []
#                print(xd)
                for j in range(0, len(Flst)):
                    Xd.append(xd)
                    Yd.append(yd)
                    YErr.append(yErr)
                    XCount_temp= Counter(xd).values()
                XCount.append(XCount_temp)
                Obj_hndl2 = ObjB.DrawTableCombinedSource(FileTags, Xd= Xd, Yd= Yd, YErr= YErr, XCount = XCount, ShowCombinedFig = showCombinedFig, SaveCombinedFig=saveCombinedFig, Mode = mode )
        return 0
func3()

def func1():
    #mode = 'Hour'
    #mode = 'Seq'
    showCombinedFig =1
    saveCombinedFig =1
    showFig = 0
    saveFig = 0
    #mode = ['Hour']
    #mode = ['Seq']
    MODE = ['Seq', 'Hour']
    
    for md in range(0, len(MODE)):
        mode = MODE[md]
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            with TbleBridge.HidePrint():
                ObjB = TbleBridge.TblB(Session_Folder= proj_folder)
                print('Things inside this with loop won\'t be printed')
            Obj_hndl = ObjB.TblBridge1(Mode= mode, ShowFig= showFig, SaveFig = saveFig)
            print('-'*50)
            
            with TbleBridge.HidePrint():
                #提醒 
                #obj[1] = temp2 = [[self.x_coord, self.y_avg, self.y_std],[self.xhr_coord, self.yhr_avg, self.yhr_std]] for [data1, data2, data3]
                Flst = Obj_hndl[0][0]
                Objlst = Obj_hndl[0][1]
                if mode == 'Seq':
                    Obj_temp = np.array(Obj_hndl[1][0])
                elif mode == 'Hour':
                    Obj_temp = np.array(Obj_hndl[1][1])
                Xd    = []
                Yd    = []
                YErr  = []
                XCount= []
                for i in range(0, len(Flst)):
                    Xd.append(Obj_temp[i][0])
                    Yd.append(Obj_temp[i][1])
                    YErr.append(Obj_temp[i][2])
                    XCount.append(Obj_temp[i][3])
                Obj_hndl2 = ObjB.DrawTableCombinedSource(Obj_hndl[0][0], Xd= Xd, Yd= Yd, YErr= YErr, XCount = XCount, ShowCombinedFig = showCombinedFig, SaveCombinedFig=saveCombinedFig, Mode = mode )
        return 0

#func1()
print('Reminder: This is the OP of Table OP') 
        #print(Obj_hndl)