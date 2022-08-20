# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:59 2019
Reading from the custom table from PeriodCls series of programs.
Version 1.2
@author: Harry
"""
import warnings as warnings
import numpy as np
import TableClsV1_2 as TbleC
import TableBridgeV1_2 as TbleBridge


showCombinedFig =1
saveCombinedFig =1
showFig = 0
saveFig = 0
mode = 'Hour'
#mode = 'Seq'
session_folder = 'session 0726 noon'
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    with TbleBridge.HidePrint():
        ObjB = TbleBridge.TblB(Session_Folder= session_folder)
        print('Things inside this with loop won\'t be printed')
    Obj_hndl = ObjB.TblBridge1(Mode= mode, ShowFig= showFig, SaveFig = saveFig)
    print('-'*50)
    
    #提醒 
    #obj[1] = temp2 = [[self.x_coord, self.y_avg, self.y_std],[self.xhr_coord, self.yhr_avg, self.yhr_std]] for [data1, data2, data3]
    Flst = Obj_hndl[0][0]
    Objlst = Obj_hndl[0][1]
    if mode == 'Seq':
        Obj_temp = np.array(Obj_hndl[1][0])
    elif mode == 'Hour':
        Obj_temp = np.array(Obj_hndl[1][1])
    Xd =[]
    Yd = []
    YErr = []
    for i in range(0, len(Flst)):
        Xd.append(Obj_temp[i][0])
        Yd.append(Obj_temp[i][1])
        YErr.append(Obj_temp[i][2])
    Obj_hndl2 = ObjB.DrawTableCombinedSource(Obj_hndl[0][0], Xd= Xd, Yd= Yd, YErr= YErr, ShowCombinedFig = showCombinedFig, SaveCombinedFig=saveCombinedFig, Mode = mode )
    #print(Obj_hndl)