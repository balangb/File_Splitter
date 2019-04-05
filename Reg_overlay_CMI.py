
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:11:07 2013

@author: abainbri
"""


import sys
import os as os
import numpy as np
#import dicom as dcm
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QPushButton, QLabel, QListWidget
from PyQt5.QtWidgets import QAbstractItemView, QTextBrowser, QLabel, QFileDialog, QListWidgetItem          
from PyQt5 import QtGui
#from PyQt4 import QtCore
#import pyqtgraph as pg
import dicom as dcm
import dicom.UID
#from dicom.filereader import open_dicom
from dicom.filereader import read_partial
from shutil import copyfile


def partial_dicom(tag, VR, length):
    return tag == (0x0028, 0x0011)
    

class Maingui(QMainWindow):
    #--------Class Construction--------------------
    def __init__(self):
        super(Maingui, self).__init__()
        self.imageoblist = []        #Hold list of spec objects
        self.curobject = 0
        self.rois = []
        self.initUI()


        
    def initUI(self):  
        #---------Add menubar----------------- 
        menubar = self.menuBar()
        
        #Create menubar items ++++++++++++++++++++++
        #Items in 'File' menu
        #Get Filename 
        outDir = QAction(QtGui.QIcon('C:\\Users\\nifty-user\\Documents\\python_code\\Pre_registration_code\\saveas.png'), 
                                 'Output Dir', self)
        outDir.setShortcut('Ctrl+O')
        outDir.triggered.connect(self.getoutdir)

        #Get Directory Name
        openDir = QAction(QtGui.QIcon('C:\\Users\\nifty-user\\Documents\\python_code\\Pre_registration_code\\open.png'),
                                'Open Dir', self)
        openDir.setShortcut('Ctrl+D')
        openDir.triggered.connect(self.getdir)
        
        #Items in 'Tools' menu


        #Add the created items to menubar
        #Note - this part must come after item creation (above)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openDir)
        fileMenu.addAction(outDir)
        
        

        
        #--------Add buttons------------------
        #btnup = QtGui.QPushButton('Im up', self)  
        btnpreview = QPushButton('Preview', self)
        #btnaddroi = QtGui.QPushButton('Add Roi', self)
        #btndelroi = QtGui.QPushButton('Del Roi', self)
        btnwrite = QPushButton('write', self)
        btnlistselect = QPushButton('Select ->', self)
        
        #Set button attributes
        #btnup.resize(btnup.sizeHint())
        #btnup.move(100,570)  
        #btnup.clicked.connect(self.imup)
        
        btnpreview.resize(btnpreview.sizeHint())
        btnpreview.move(70,210)  
        btnpreview.clicked.connect(self.preview)
        
        #btnaddroi.resize(btnaddroi.sizeHint())
        #btnaddroi.move(180,570)  
        #btnaddroi.clicked.connect(self.addroi)        
        
        #btndelroi.resize(btndelroi.sizeHint())
        #btndelroi.move(260,570)  
        #btndelroi.clicked.connect(self.delroi) 

        btnwrite.resize(btnwrite.sizeHint())
        btnwrite.move(500,210)  
        btnwrite.clicked.connect(self.writeout) 
        
        btnlistselect.resize(btnlistselect.sizeHint())
        btnlistselect.move(260,120)  
        btnlistselect.clicked.connect(self.getselected) 
        
        #---------- Add List Boxes -------------------------
        listlabel = QLabel("&List of Series")
        self.listwidget = QListWidget(self)
        self.listwidget.setGeometry(10,80,240,120) 
        self.listwidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        
        self.selectedlistwidget = QListWidget(self)
        self.selectedlistwidget.setGeometry(350,80,240,120)
        
        
        
        
        
        #--------Add Message Box---------------
        #Note this opens a separate windpw with a message
        #self.mssg = QtGui.QMessageBox()
        #self.mssg.setGeometry(310, 240, 280,280)
        #self.mssg.show()
        
        #-------Add line edit------------------
        #self.le = QtGui.QLineEdit(self)
        #self.le.move(310, 240)
        #self.le.setFixedWidth(280)
        #self.le.setGeometry(310, 240, 280,280)
        #self.le.textChanged[str].connect(self.onChanged)
        
         #-------Add Text Browser------------------
        self.dcmheadwin = QTextBrowser(self)
        self.dcmheadwin.setGeometry(10, 240, 580,140)
        self.dcmheadwin.clear()
        self.dcmheadwin.append('Preview brief study information in this window')
        
        self.messages = QTextBrowser(self)
        self.messages.setGeometry(10, 390, 580, 140)
        self.messages.clear()
        self.messages.append('Messages will appear in this window')
        
        #self.le.textChanged[str].connect(self.onChanged)
                
        #-------Add text labels-----------------------
        self.lblin = QLabel(self)
        self.lblin.move(10,30)
        self.lblin.setText('Input Directry:')
        self.lblin.adjustSize()     
        
        self.lblout = QLabel(self)
        self.lblout.move(10,45)   
        self.lblout.setText('Output Directry:')
        self.lblout.adjustSize() 
        
        self.lblserin = QLabel(self)
        self.lblserin.move(10,65)
        self.lblserin.setText('Series in Input Directory:')
        self.lblserin.adjustSize() 
        
        self.lblselser = QLabel(self)
        self.lblselser.move(350,65)
        self.lblselser.setText('Selected Series for Registration:')
        self.lblselser.adjustSize() 
        
        
        
        #------- Add pyqtgraph objects ---------------------
        ## Switch to using white background and black foreground
        #pg.setConfigOption('background', 'w')
        #pg.setConfigOption('foreground', 'k')
        
        #--------Add simple image view widget ---------------
        #a = np.array([[1,2,3,4],[2,3,4,5],[4,3,2,1],[2,1,5,3]])
        #self.win = pg.GraphicsLayoutWidget(self)
        #self.win.setGeometry(10, 240, 280, 280)
        #self.vb = self.win.addViewBox()
        #self.vb.setAspectLocked()
        #grad = pg.GradientEditorItem(orientation='right')
        #win.addItem(grad, 0, 1)
        #img = pg.ImageItem(a)
        #self.vb.addItem(img)
        #self.win.show()
    
        
        #self.imagewidget.setImage(a)
        
        
        #self.imagewidget = pg.ImageView(self)
        #self.imagewidget.setGeometry(QtCore.QRect(20, 40, 560, 500))
        #self.imagewidget.show()
        
        #self.roiwidget = pg.ImageView()
        #self.roiwidget.setGeometry(900,200,300,300)
        #self.roiwidget.setWindowTitle('Roi Viewer')
        #self.roiwidget.show()
        
        #self.maskwidget = pg.ImageView()
        #self.maskwidget.setGeometry(900,600,300,300)
        #self.maskwidget.setWindowTitle('Roi Mask Viewer')
        #self.maskwidget.show()

        ## Open a DICOM image
       # self.dcmob = dcm.read_file('K:\\Alan_projects\\ingenia\\Dicom_scale_test\\IM_1770')
        
        ## Display the data and assign each frame a time value from 1.0 to 3.0
        #self.imagewidget.setImage(data, xvals=np.linspace(1., 3., data.shape[0]))        
       # self.imagewidget.setImage(self.dcmob.pixel_array)
        

        #rois.append(pg.RectROI([20, 20], [20, 20], pen=(0,9)))
        #rois[-1].addRotateHandle([1,0], [0.5, 0.5])
        #rois.append(pg.LineROI([0, 60], [20, 80], width=5, pen=(1,9)))
        #rois.append(pg.MultiRectROI([[20, 90], [50, 60], [60, 90]], width=5, pen=(2,9)))
        
        #rois.append(pg.LineSegmentROI([[110, 50], [20, 20]], pen=(5,9)))
        #rois.append(pg.PolyLineROI([[110, 60], [20, 30], [50, 10]], pen=(6,9)))
        
                   
        #for roi in self.rois:
            #roi.sigRegionChanged.connect(self.update)
            #self.imagewidget.addItem(roi)

        #self.update(rois[-1])        
        
        
        #------Main Window Geometry-----------
        #This should come at the end once all GUI item are created
        self.setGeometry(200, 200, 600, 540)
        self.setWindowTitle('File Splitter')
        self.setWindowIcon(QtGui.QIcon('C:\\Users\\nifty-user\\Documents\\python_code\\Pre_registration_code\\advanced.png'))
        self.show()
        
        
        
    #--------Class Methods-----------------------------------    
    def getoutdir(self):
        self.outdirname = str(QFileDialog.getExistingDirectory(self,
                'Ouput Directory', 'D:/Google Drive/cancer_centre/DCE_code'))
        textout = 'Output Directory: ' + self.outdirname
        self.lblout.setText(textout)
        self.lblout.adjustSize()        
        
    def getdir(self):
        self.dirname = str(QFileDialog.getExistingDirectory(self,
                'Open Directory', 'D:/Google Drive/cancer_centre/DCE_code'))
        textout = 'Input Directory: ' + self.dirname
        self.lblin.setText(textout)
        self.lblin.adjustSize()
        self.getseries()
        self.populatelist()      
        
    def imup(self):
        dummy = 1
        
    def imdown(self):
        dummy = 1
        
    def addroi(self):
        #print 'in addroi'
        self.rois.append(pg.CircleROI([60, 10], [30, 20], pen=(3,9)))
        size_rois = np.size(self.rois)
        self.imagewidget.addItem(self.rois[size_rois-1])     
        
    def delroi(self):
        size_rois = np.size(self.rois)
        self.imagewidget.removeItem(self.rois[size_rois-1]) 
        del self.rois[-1]
        
    def writeout(self):
        self.messages.append('Writing series')
        for entry in self.SelSerList:
            entry.write_dicom_easy(self.outdirname)        
        self.messages.append('Writing Finished')    
        #print 'Number of series ' + str(SeriesOb.NumSeries)
        
    def makeROImask(self):
        #Compare Roi bounds with self.roiarr shape and make sure they are the same size
        
        self.ROImask = np.zeros([self.x, self.y])
        for cnt1 in range(0,self.x):
            for cnt2 in range(0, self.y):
                if cnt1 > self.bounds[0] and cnt1 < self.bounds[1]:
                    if cnt2 > self.bounds[2] and cnt2 < self.bounds[3]:
                        if self.roiarr[cnt1-self.bounds[0], cnt2-self.bounds[2]] > 0:
                            self.ROImask[cnt1, cnt2] = 1
      
    def populatelist(self):
        self.listwidget.clear()
        for item in self.SerList:
            seriesname = str(item.obnumber) + ': ' + item.study + '_series_' + str(item.series)
            qitem = QListWidgetItem(seriesname)            
            self.listwidget.addItem(qitem)
        
        
        
    def preview(self):
        item = self.listwidget.selectedItems()[0]
        qitem = QListWidgetItem(item)            
        serobnumindex = str(item.text()).index(':')
        serobnum = int(str(item.text())[:serobnumindex])
        self.dcmheadwin.clear()
        fp = open(self.SerList[serobnum].pathlist[0], 'rb')
        data = read_partial(fp, stop_when=partial_dicom)
        message = 'Patient name: ' + str(data.PatientName)
        self.dcmheadwin.append(message)
        message = 'Protocol name: ' + str(data.ProtocolName)
        self.dcmheadwin.append(message)
        message = 'Study ID: ' + str(data.StudyID)
        self.dcmheadwin.append(message)
        message = 'Series Number: ' + str(data.SeriesNumber)
        self.dcmheadwin.append(message)
        fp.close()
        
    
    def getselected(self):
        self.SelSerList = []
        self.selectedlistwidget.clear()
        for item in self.listwidget.selectedItems():
            qitem = QListWidgetItem(item)            
            self.selectedlistwidget.addItem(qitem)
            serobnumindex = str(item.text()).index(':')
            serobnum = int(str(item.text())[:serobnumindex])
            self.SelSerList.append(self.SerList[serobnum])

    def addmessage(self, message):    
        self.messages.append(message)
        

        
    def getseries(self):
        SeriesOb.NumSeries = 0
        start_dir = self.dirname
       
        self.SerList = []
        
        os.chdir(start_dir)
        #get list of files in chosen directory
        filelist = os.listdir(start_dir)
        #print filelist
        dirlist = []
        dirlist.append(start_dir)
        for entry in filelist:
            if os.path.isdir(entry):
                dirname = start_dir + '/' + entry
                dirlist.append(dirname)
                
                
        for directory in dirlist:
            os.chdir(directory)
            filelist = os.listdir(directory)
        
            for entry in filelist:
                dummy = 0
                try:
                    fp = open(entry, 'rb')
                    read_partial(fp, stop_when=partial_dicom)
                    fp.close()
                    
                except:
                    dummy = 1
                    #print 'excepted'
                    
                if dummy == 0:
                    #print entry
                    fp = open(entry, 'rb')
                    data = read_partial(fp, stop_when=partial_dicom)
                    study = data.StudyID
                    series = data.SeriesNumber
                    fp.close()    
                
                gotseries = 0
                for Ser in self.SerList:
                    if Ser.study == study:
                        if Ser.series == series:
                            gotseries = 1
                            filename = directory + '/' + entry
                            Ser.pathlist.append(filename)
                            
                if gotseries == 0:
                    if dummy == 0:
                        filename = directory + '/' + entry
                        self.SerList.append(SeriesOb(filename))
                    
                        
        #for entry in SerList:
            #entry.write_dicom(outpath)        
            
        #print 'Number of series ' + str(SeriesOb.NumSeries)





class SeriesOb(object):
    NumSeries = 0   #Keep track of number of series objects
    
    def __init__(self, pathtofile):
        self.obnumber = SeriesOb.NumSeries
        self.pathlist = []
        self.pathlist.append(pathtofile)
        SeriesOb.NumSeries += 1

        self.series = 0
        self.study = 'no name stored'
        self.frames = 1
        self.curframe = 0
        
        
        fp = open(pathtofile, 'rb')
        data = read_partial(fp, stop_when=partial_dicom)
        self.study = data.StudyID
        self.series = data.SeriesNumber
        try:
            self.protocolname = data.ProtocolName
        except:
            self.protocolname = 'unknown'   
        try:
            self.frames = data_element.value
        except:
            dummy = 1
        fp.close()            
    
    
    def num_frames(self):
        self.frames = 0
        for dcmfile in self.pathlist:
            dcmob = dcm.read_file(dcmfile, stop_before_pixels = True)
            try:
                dummy_frames = dcmob.NumberOfFrames
            except:
                dummy_frames = 1
            self.frames = self.frames + dummy_frames   
        #return self.frames
     
    def inc_frame(self):
        self.curframe = self.curframe + 1
        if self.curframe > self.frames:
            self.curframe = self.frames

    def dec_frame(self):
        self.curframe = self.curframe - 1
        if self.curframe <0:
            self.curframe = 0
            
    def get_frame(self):
        self.num_frames()
        # determine if multi frame or multi file
        if np.size(self.pathlist) == 1:
            dcmob = dcm.read_file(self.pathlist[0])
            if self.frames < 1000:
                imsize = dcmob.Rows * dcmob.Columns * 2
                fm = np.round(self.frames/2)
                imstart = fm * imsize
                dummyim = dcmob[0x7fe0, 0x0010][imstart:(imstart + imsize)]
                dcmob[0x7fe0, 0x0010].value = dummyim
                dcmob.NumberOfFrames = 1
                imout = dcmob.pixel_array
        else:
            a = np.size(self.pathlist)
            fm = int(np.round(a/2))
            dcmob = dcm.read_file(self.pathlist[fm])
            imout = dcmob.pixel_array
        return imout
            
    def write_dicom_easy(self, outfilepath):
        message =  'writing series ' + self.study + '_' + str(self.series)
        #os.chdir(outfilepath)
        outpathdir = outfilepath + '/Series_' +  str(self.series) + '_' + str(self.protocolname)
                                                     
        if os.path.isdir(outpathdir) == False:
            os.mkdir(outpathdir)
                    
        filenum = 0
        for dcmfile in self.pathlist:
            filenum = filenum + 1
            if filenum < 10:
                filstr = '00' + str(filenum)
            elif filenum < 100:
                filstr = '0' + str(filenum)
            else:
                filstr = str(filenum)
            fileout  = outpathdir + '/' + '_Image_' + filstr + '.dcm'
            copyfile(dcmfile, fileout)
            
            
            
    def write_dicom(self, outfilepath):
        """
        INPUTS:
        pixel_array: 2D numpy ndarray.  If pixel_array is larger than 2D, errors.
        filename: string name for the output file.
        """
        message =  'writing series ' + self.study + '_' + str(self.series)
        ImPosList = [] 
        VolList = []
        curslices = 0
        ds = dcm.read_file('C:\\Users\\nifty-user\\Documents\\python_code\\Pre_registration_code\\dicom_header') 
        filenum = 0
        framenumber = 0
        for dcmfile in self.pathlist:
            filenum = filenum + 1
            dcmob = dicom.read_file(dcmfile)
            #pixel_array3D = dcmob.pixel_array
            try:
                frames = dcmob.NumberOfFrames
            except:
                frames = 1   
        
            
            code_list = ['ds.add_new([0x0018, 0x9082], \'DS\', dcmob[0x5200, 0x9230][20][0x0018, 0x9114][0][0x0018, 0x9082].value)',
                         'ds.SpecificCharacterSet = dcmob.SpecificCharacterSet',
                         'ds.ImageType = dcmob.ImageType',
                         'ds.ContentDate = dcmob.ContentDate',
                         'ds.ContentTime = dcmob.ContentTime',
                         'ds.StudyInstanceUID =  dcmob.StudyInstanceUID',
                         'ds.SeriesInstanceUID = dcmob.SeriesInstanceUID',
                         'ds.SOPInstanceUID =  dcmob.SOPInstanceUID',  
                         'ds.SOPClassUID = \'Secondary Split Dicom\'',
                         'ds.SecondaryCaptureDeviceManufacturer = \'Python 2.7.3\'',
                         'ds.SamplesPerPixel = dcmob.SamplesPerPixel',
                         'ds.PhotometricInterpretation = dcmob.PhotometricInterpretation',
                         'ds.PixelRepresentation = dcmob.PixelRepresentation',
                         'ds.HighBit = dcmob.HighBit',
                         'ds.BitsStored = dcmob.BitsStored',
                         'ds.BitsAllocated = dcmob.BitsAllocated',
                         'ds.Columns = dcmob.Columns',
                         'ds.Rows = dcmob.Rows',
                         'ds.LowRRValue = dcmob.LowRRValue',
                         'ds.HighRRValue = dcmob.HighRRValue',
                         'ds.IntervalsAcquired = dcmob.IntervalsAcquired',
                         'ds.IntervalsRejected = dcmob.IntervalsRejected',
                         'ds.HeartRate = dcmob.HeartRate',
                         'ds.PixelSpacing = dcmob.PixelSpacing',
                         'ds.WindowCenter = dcmob.WindowCenter',
                         'ds.WindowWidth = dcmob.WindowWidth',
                         'ds.DiffusionBValue = dcmob.DiffusionBValue',
                         'ds.DiffusionGradientOrientation = dcmob.DiffusionGradientOrientation',
                         'ds.InstanceCreationDate = dcmob.InstanceCreationDate',
                         'ds.InstanceCreationTime = dcmob.InstanceCreationTime',
                         'ds.InstanceCreatorUID = dcmob.InstanceCreatorUID',
                         'ds.StudyDate = dcmob.StudyDate',
                         'ds.SeriesDate = dcmob.SeriesDate',
                         'ds.StudyTime = dcmob.StudyTime',
                         'ds.SeriesTime = dcmob.SeriesTime',
                         'ds.AcquisitionDate = dcmob.AcquisitionDate',
                         'ds.AcquisitionDate = dcmob.AcquisitionDateTime[:8]',
                         'ds.AcquisitionTime = dcmob.AcquisitionTime',
                         'ds.AcquisitionTime = dcmob.AcquisitionDateTime[8:]',
                         'ds.AccessionNumber = dcmob.AccessionNumber',
                         'ds.PatientName = dcmob.PatientName',
                         'ds.PatientBirthDate = dcmob.PatientBirthDate',
                         'ds.PatientSex = dcmob.PatientSex',
                         'ds.PatientID = dcmob.PatientID',
                         'ds.PatientPosition = dcmob.PatientPosition',
                         'ds.PatientWeight = dcmob.PatientWeight',
                         'ds.BodyPartExamined = dcmob.BodyPartExamined',
                         'ds.MRAcquisitionType = dcmob.MRAcquisitionType',
                         'ds.SliceThickness = dcmob.SliceThickness',
                         'ds.RepetitionTime = dcmob.RepetitionTime',
                         'ds.EchoTime = dcmob.EchoTime',
                         'ds.NumberOfAverages = dcmob.NumberOfAverages',
                         'ds.ImagingFrequency = dcmob.ImagingFrequency',
                         'ds.ImagedNucleus = dcmob.ImagedNucleus',
                         'ds.EchoNumbers = dcmob.EchoNumbers',
                         'ds.MagneticFieldStrength = dcmob.MagneticFieldStrength',
                         'ds.SpacingBetweenSlices = dcmob.SpacingBetweenSlices',
                         'ds.NumberOfPhaseEncodingSteps = dcmob.NumberOfPhaseEncodingSteps',
                         'ds.EchoTrainLength = dcmob.EchoTrainLength',
                         'ds.PercentSampling = dcmob.PercentSampling',
                         'ds.PercentPhaseFieldOfView = dcmob.PercentPhaseFieldOfView',
                         'ds.PixelBandwidth = dcmob.PixelBandwidth',
                         'ds.SoftwareVersions = dcmob.SoftwareVersions',
                         'ds.ProtocolName = dcmob.ProtocolName',
                         'ds.ReceiveCoilName = dcmob.ReceiveCoilName',
                         'ds.TransmitCoilName = dcmob.TransmitCoilName',
                         'ds.AcquisitionMatrix = dcmob.AcquisitionMatrix',
                         'ds.InPlanePhaseEncodingDirection = dcmob.InPlanePhaseEncodingDirection',
                         'ds.FlipAngle = dcmob.FlipAngle',
                         'ds.AcquisitionDuration = dcmob.AcquisitionDuration',
                         'ds.StudyID = dcmob.StudyID',
                         'ds.SeriesNumber = dcmob.SeriesNumber',
                         'ds.AcquisitionNumber = dcmob.AcquisitionNumber',
                         'ds.InstanceNumber = dcmob.InstanceNumber',
                         'ds.SliceLocation = dcmob.SliceLocation',
                         'ds.ImagePositionPatient = dcmob.ImagePositionPatient',
                         'ds.ImageOrientationPatient = dcmob.ImageOrientationPatient',
                         'ds.TemporalPositionIdentifier = dcmob.TemporalPositionIdentifier',
                         'ds.NumberOfTemporalPositions = dcmob.NumberOfTemporalPositions',
                         'ds.RescaleIntercept = dcmob.RescaleIntercept',
                         'ds.RescaleSlope = dcmob.RescaleSlope',
                         'ds.RescaleType = dcmob.RescaleType',
                         'ds[0x2005, 0x100d].value = dcmob[0x2005, 0x100d].value',
                         'ds[0x2005, 0x100e].value = dcmob[0x2005, 0x100e].value',
                         'ds[0x2001, 0x1023].value = dcmob[0x2001, 0x1023].value',
                         'ds[0x2005, 0x1030].value = dcmob[0x2005, 0x1030].value',
                         'ds.add_new([0x0018, 0x9082], \'FD\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9114][0][0x0018, 0x9082].value)',
                         'ds.add_new([0x0008, 0x9007], \'CS\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9226][0][0x0008, 0x9007].value)',
                         'ds.add_new([0x0008, 0x9205], \'CS\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9226][0][0x0008, 0x9205].value)',
                         'ds.add_new([0x0008, 0x9206], \'CS\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9226][0][0x0008, 0x9206].value)',
                         'ds.add_new([0x0008, 0x9207], \'CS\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9226][0][0x0008, 0x9207].value)',
                         'ds.add_new([0x0008, 0x9208], \'CS\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9226][0][0x0008, 0x9208].value)',
                         'ds.add_new([0x0008, 0x9209], \'CS\', dcmob[0x5200, 0x9230][fm][0x0018, 0x9226][0][0x0008, 0x9209].value)',
                         'ds.add_new([0x0018, 0x9074], \'DT\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0018, 0x9074].value)',
                         'ds.add_new([0x0018, 0x9151], \'DT\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0018, 0x9151].value)',
                         'ds.add_new([0x0018, 0x9220], \'FD\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0018, 0x9220].value)',
                         'ds.add_new([0x0020, 0x9056], \'SH\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0020, 0x9056].value)',
                         'ds.add_new([0x0020, 0x9057], \'UL\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0020, 0x9057].value)',
                         'ds.add_new([0x0020, 0x9128], \'UL\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0020, 0x9128].value)',
                         'ds.add_new([0x0020, 0x9157], \'UL\', dcmob[0x5200, 0x9230][fm][0x0020, 0x9111][0][0x0020, 0x9157].value)',
                         'ds[0x0020, 0x0032].value = dcmob[0x5200, 0x9230][fm][0x0020, 0x9113][0][0x0020, 0x0032].value',
                         'ds[0x0020, 0x0037].value = dcmob[0x5200, 0x9230][fm][0x0020, 0x9116][0][0x0020, 0x0037].value',
                         'ds[0x0018, 0x0050].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9110][0][0x0018, 0x0050].value',
                         'ds[0x0028, 0x0030].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9110][0][0x0028, 0x0030].value',
                         'ds[0x0028, 0x1050].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9132][0][0x0028, 0x1050].value',
                         'ds[0x0028, 0x1051].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9132][0][0x0028, 0x1051].value',
                         'ds[0x0028, 0x1052].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9145][0][0x0028, 0x1052].value',
                         'ds[0x0028, 0x1053].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9145][0][0x0028, 0x1053].value',
                         'ds[0x0028, 0x1054].value = dcmob[0x5200, 0x9230][fm][0x0028, 0x9145][0][0x0028, 0x1054].value',
                         'ds[0x0008, 0x0008].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0008, 0x0008].value',
                         'ds[0x0008, 0x0018].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0008, 0x0018].value',
                         'ds[0x0008, 0x0023].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0008, 0x0023].value',
                         'ds[0x0008, 0x0033].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0008, 0x0033].value',
                         'ds[0x0018, 0x0020].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0020].value',
                         'ds[0x0018, 0x0023].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0023].value',
                         'ds[0x0018, 0x0081].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0081].value',
                         'ds.add_new([0x0018, 0x0082], \'DS\', dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0082].value)',
                         'ds[0x0018, 0x0083].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0083].value',
                         'ds[0x0018, 0x0084].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0084].value',
                         'ds[0x0018, 0x0085].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0085].value',
                         'ds[0x0018, 0x0086].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0086].value',
                         'ds[0x0018, 0x0088].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0088].value',
                         'ds[0x0018, 0x0091].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x0091].value',
                         'ds[0x0018, 0x1081].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1081].value',
                         'ds[0x0018, 0x1082].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1082].value',
                         'ds[0x0018, 0x1083].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1083].value',
                         'ds[0x0018, 0x1084].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1084].value',
                         'ds[0x0018, 0x1088].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1088].value',
                         'ds[0x0018, 0x1251].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1251].value',
                         'ds[0x0018, 0x1310].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1310].value',
                         'ds[0x0018, 0x1314].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x1314].value',
                         'ds.add_new([0x0018, 0x9064], \'CS\', dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x9064].value)',
                         'ds.add_new([0x0018, 0x9147], \'CS\', dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0018, 0x9147].value)',
                         'ds[0x0020, 0x0012].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0020, 0x0012].value',
                         'ds[0x0020, 0x0013].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0020, 0x0013].value',
                         'ds[0x0020, 0x0100].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0020, 0x0100].value',
                         'ds[0x0020, 0x0105].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x0020, 0x0105].value',
                         'ds[0x2005, 0x100d].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x2005, 0x100d].value',
                         'ds[0x2005, 0x100e].value = dcmob[0x5200, 0x9230][fm][0x2005, 0x140f][0][0x2005, 0x100e].value']
                          
                          
                          
                          
                          
            for fm in range(0,frames):  
                framenumber = fm + filenum
                
                #get Image Position from header - could be either of two locations:
                try:
                    ImPostemp = dcmob.ImagePositionPatient
                except:
                    ImPostemp = dcmob[0x5200, 0x9230][fm][0x0020, 0x9113][0][0x0020, 0x0032].value
                
                inlist = 0
                for IP in ImPosList:
                    if IP == ImPostemp:
                        inlist = 1
                        
                
                if inlist == 0:
                    ImPosList.append(ImPostemp)
                    Vol = 0
                    curslices = curslices + 1.
                    VolList.append(0)
                    message =  'cs:' + str(curslices) + ' fm:' + str(framenumber) + ' vol:' + str(Vol)
                    
                else:
                    Lind = ImPosList.index(ImPostemp)
                    VolList[Lind] = VolList[Lind] + 1
                    Vol = VolList[Lind]
                    message =  'cs:' + str(curslices) + ' fm:' + str(framenumber) + ' vol:' + str(Vol)
                    
                outparentdir = outfilepath + '/Study_' + self.study.strip(' ') 
                if os.path.isdir(outparentdir) == False:
                    os.mkdir(outparentdir)
                    
                outpathdir = outparentdir + '/Series_' +  str(self.series) + '_Volume_' + str(Vol).zfill(3)
                if os.path.isdir(outpathdir) == False:
                    os.mkdir(outpathdir)
                    
                fileout  = outpathdir + '/' + self.study + '_series_' + str(self.series) + '_frame_' + str(framenumber).zfill(3) + '.dcm'

        
                ds.file_meta = dcmob.file_meta
                ds.file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4' #MRImage Storage - not enhanced
                ds.file_meta.ImplementationClassUID = '1.3.6.1.4.1.9590.100.1.0.100.4.0'
        
                
                for entry in code_list:
                    try:
                        exec(entry)
                    except:
                        dummy = 1
                imsize = dcmob.Rows * dcmob.Columns * 2
                imstart = fm * imsize

                ds[0x7fe0, 0x0010].value = dcmob[0x7fe0, 0x0010][imstart:(imstart + imsize)]
                ds.save_as(fileout)
                             
            
        



                      

def main():
    
    app = QApplication(sys.argv)
    ex = Maingui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()