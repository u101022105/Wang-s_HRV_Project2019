# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:59 2019
Reading from the custom table from PeriodCls series of programs.
Version 1.1
@author: Harry
"""
import warnings as warnings
import numpy as np
import TableClsV1_1 as TbleC
import TableBridgeV1_1 as TbleBridge

session_folder = 'session 0725'
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    Obj_hndl = TbleBridge.TblBridge1(Session_Folder= session_folder, ShowFig= 0)
    #提醒 obj[1] = temp2 = [self.xhr_coord, self.yhr_avg, self.yhr_std] for [data1, data2, data3]
    Flst = Obj_hndl[0][0]
    Objlst = Obj_hndl[0][1]
    Obj_temp = np.array(Obj_hndl[1])
    Xd =[]
    Yd = []
    YErr = []
    for i in range(0, len(Flst)):
        Xd.append(Obj_temp[i][0])
        Yd.append(Obj_temp[i][1])
        YErr.append(Obj_temp[i][2])
    Obj_hndl2 = TbleBridge.DrawTableCombinedSource(Obj_hndl[0][0], Xd= Xd, Yd= Yd, YErr= YErr, Mode = 'Hour' )
    #print(Obj_hndl)