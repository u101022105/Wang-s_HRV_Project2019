# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:36:04 2019
Table cls series bridge
Version 1
@author: Harry
"""

import TableClsV1 as TbleCls
import numpy as np
import os as os

#def TblCls_Op(Flst, Mode = None):
#    obj_lst = []
#    for i in range(0, len(Flst)):
#        obj = TbleC(Flst[i])
#        obj.RunInitiate()
#        obj_lst.append(obj)
#    temp = np.array([Flst, obj_lst]).T
#    return temp
folder ='Period_data_pack folder'
path1 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'+'\\'+folder + '\\Period_data_pack folder'
path2 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'
path = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'


def TblBridge1( Session_Folder = None, Folder = 'Period_data_pack folder', Fname = None, Savefig= 0, Showfig = 1, Path1 = path, Path2 = path):
    '''
    兩種模式，輸入fname來讀特定檔名
    不輸入模式則自動跑過預設資料夾中的所有檔案
    傳回 numpy陣列 [ [檔名1, TbleC_obj1], [檔名2, TbleC_obj2],... ]
    '''
    
    if Session_Folder ==None:
        print('Please direct the program with the session folder\'s name')
        
    Path1 = path+ '\\'+ Session_Folder+ '\\'+ Folder
    Path2 = path
    if Fname != None:
        os.chdir(Path1)
        obj = TbleCls(Fname)
        temp = np.array([Fname, obj]).T
        os.chdir(Path2)
    else:
        os.chdir(Path1)
        #print(os.getcwd())
        flst = os.listdir()
        os.chdir(Path2)
        #print(os.getcwd())
        obj_lst = []
        for i in range(0, len(flst)):
            os.chdir(Path1)
            #print(os.getcwd())
            obj = TbleCls.TblC(flst[i])
            os.chdir(Path2)
            #print(os.getcwd())
            obj.RunInitiate()
            obj_lst.append(obj)
        temp = np.array([flst, obj_lst]).T
    #print('files: ', flst)
    return temp


#def TblBridge2( Folder = 'Period_data_pack folder', fname = 'Assumed Strictly Serial Files Operation, please don\'t input file names'):
#    '''
#    operation over files. Instead of turning them all into objects then do the operations,
#    excecute the op over each file sequentially, since the later way is faster and can produce the desired graphs and such when running into obstacles
#    when facing a series of files that might took a long time to analyze and need to be interupted during the python console excecution.
#    '''
#    path1 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'+'\\'+Folder
#    path2 = 'C:\\Users\\Harry\\Google 雲端硬碟\\0_2019冠珵-節拍器與心律變異率\\Python Custom Tables 操作2019\\1_Test session Level'
#    os.chdir(path1)
#    flst = os.listdir()
#    obj_lst = []
#    for i in range(0, len(flst)):
#        obj_lst.append(TbleC(flst[i]))
#    temp = np.array([flst, obj_lst]).T