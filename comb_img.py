from astropy.io import fits
import numpy as np
import glob
import pdb
import os

class combInts():
    """ Object that can combine individual integration files made by pynrc into a single FITS """
    def __init__(self,fileString,outImg='comb_img.fits'):
        self.outImg = outImg
        self.fileString = fileString
        self.fileList = np.sort(glob.glob(fileString))
        if len(self.fileList) >= 1:
            self.firstFile = self.fileList[0]
            self.fileFound = True
            print("Combining "+self.fileString)
        else:
            print("No files found for "+self.fileString)
            self.fileFound = False
            return
        
        HDUList = fits.open(self.firstFile)
        self.firstHeader = HDUList['PRIMARY'].header
        self.nints = self.firstHeader['NINTS']
        self.ngroups = self.firstHeader['NGROUPS']
        self.subsizeX = self.firstHeader['SUBSIZE1']
        self.subsizeY = self.firstHeader['SUBSIZE2']
        self.firstSciHeader = HDUList['SCI'].header
        
        #self.nx = self.
        HDUList.close()
        
    def checkDetector(self):
        """ Checks that the detector keyword is the same in all images """
        checkKeys = ['DETECTOR','NGROUPS','SUBSIZE1','SUBSIZE2']
        for oneFile in self.fileList:
            HDUList = fits.open(oneFile)
            thisHeader = HDUList[0].header
            for oneKey in checkKeys:
                if thisHeader[oneKey] != self.firstHeader[oneKey]:
                    print('Error: More than one '+oneKey+' in FITS list')
                    print(oneFile,' : ',thisHeader[oneKey])
                    print(self.firstFile, ' : ',self.firstHeader[oneKey])
    
    def comb(self):
        """ Combines the files """
        self.checkDetector()
        allCube = np.zeros((self.nints,self.ngroups,self.subsizeY,self.subsizeX),dtype='uint16')
        allZero = np.zeros((self.nints,self.subsizeY,self.subsizeX),dtype='uint16')
        
        for intInd, oneFile in enumerate(self.fileList):
            HDUList = fits.open(oneFile)
            allCube[intInd,:,:,:] = HDUList['SCI'].data
            allZero[intInd,:,:] = HDUList['ZEROFRAME'].data
            HDUList.close()
        
        primHDU = fits.PrimaryHDU(header=self.firstHeader)
        primHDU.name = 'PRIMARY'
        
        cubeHDU = fits.ImageHDU(data=allCube,header=self.firstSciHeader)
        
        zeroHDU = fits.ImageHDU(data=allZero)
        zeroHDU.header.comments['NAXIS1'] = 'length of first data axis (#columns)'
        zeroHDU.header.comments['NAXIS2'] = 'length of second data axis (#rows)'
        if zeroHDU.header['NAXIS'] > 2:
            zeroHDU.header.comments['NAXIS2'] = 'length of second data axis (#integrations)'
        zeroHDU.name = 'ZEROFRAME'
        
        HDUList = fits.HDUList([primHDU,cubeHDU,zeroHDU])
        HDUList.writeto(self.outImg,overwrite=True)
        
def test():
    """ example run of comb_img """
    c = combInts('sim_img/grism/NRCALONG_F444W*.fits','sim_img/grism_comb/NRCALONG_F444W.fits')
    c.comb()

def comb_all():
    """ Combines integrations of all small simulations """
    schNames = ['NRCA1_F322W2',
                'NRCALONG_F322W2',
                'NRCA1_F444W',
                'NRCALONG_F444W',
                'NRCB1','NRCBLONG']
    dirNames = ['grism','grism','grism','grism',
               'direct_imaging','direct_imaging']
    for oneSch,oneDir in zip(schNames,dirNames):
        searchPath = 'sim_img/'+oneDir+'/'+oneSch+'*.fits'
        savePath = 'sim_img/'+oneDir+'_comb/'+oneSch+'.fits'
        c = combInts(searchPath,savePath)
        if c.fileFound == True:
            c.comb()

if __name__ == '__main__':
    """ Run comb_all by default """
    comb_all()
    