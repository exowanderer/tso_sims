from sys import argv
import pynrc
pynrc.setup_logging('WARN', verbose=False)
from pynrc.nrc_utils import S

# # Initialize a NIRCam Grism observation in Stripe mode
# for oneFilt,nGROUP in zip(['F444W','F322W2'],[12,6]):
#     print('Starting Loop Iteration with filter {} & ngroups {}'.format(oneFilt,nGROUP))
#
#     nrcWL = pynrc.NIRCam('F210M', pupil='Weak Lens +8', module='A', nint=2,ngroup=nGROUP,
#                          wind_mode='STRIPE', xpix=2048, ypix=256)
#
#     print('Allocated SW NRC instance for {} & {}'.format(oneFilt,nGROUP))
#
#     nrc = pynrc.NIRCam(oneFilt, pupil='GRISM0', module='A', nint=2,ngroup=nGROUP,
#                        wind_mode='STRIPE', xpix=2048, ypix=256,read_mode='BRIGHT1')
#
#     print('Allocated LW NRC instance for {} & {}'.format(oneFilt,nGROUP))
#
#     # Specify name of output file.
#     # Time stamps will be automatically inserted for unique file names.
#     bpJ = S.ObsBandpass('johnson,j')
#     sp = pynrc.stellar_spectrum('K7V', 9.2, 'vegamag', bpJ)
#     file_out = 'sim_img/grism/NRCALONG_'+oneFilt+'_'
#     file_outWL = 'sim_img/grism/NRCA1_'+oneFilt+'_'
#     res_sp = nrc.gen_exposures(  sp, file_out)
#     res_wl = nrcWL.gen_exposures(sp, file_outWL)

# Initialize a NIRCam Grism observation in Stripe mode 
for oneFilt,nGROUP in zip(['F444W','F322W2'],[12,6]):
    print()
    # oneFilt,nGROUP = list(zip(['F444W','F322W2'],[12,6]))[0]
    
    print('Starting Loop Iteration with filter {} & ngroups {}'.format(oneFilt,nGROUP))
    
    nrcWL = pynrc.NIRCam('F210M', pupil='Weak Lens +8', module='A', nint=2,ngroup=nGROUP,
                         wind_mode='STRIPE', xpix=2048, ypix=256)
    
    print('Allocated SW NRC instance for {} & {}'.format(oneFilt,nGROUP))
    
    nrcGrism = pynrc.NIRCam(oneFilt, pupil='GRISM0', module='A', nint=2,ngroup=nGROUP,
                       wind_mode='STRIPE', xpix=2048, ypix=256,read_mode='BRIGHT1')
    
    print('Allocated LW NRC instance for {} & {}'.format(oneFilt,nGROUP))
    
    # Specify name of output file.
    # Time stamps will be automatically inserted for unique file names.
    bpJ = S.ObsBandpass('johnson,j')
    
    print('Allocated Normalization Bandwidth: J-band')
    
    stellarType = 'K7V'
    Jmag        = 9.2
    sp = pynrc.stellar_spectrum(stellarType, Jmag, 'vegamag', bpJ)
    
    print('Allocated Stellar spectrum with SType: {} and Jmag: {}'.format(stellarType, Jmag))
    
    file_out = 'sim_img/grism/NRCALONG_'+oneFilt+'_'
    file_outWL = 'sim_img/grism/NRCA1_'+oneFilt+'_'
    
    print('Assigned SW file out as {}'.format(file_outWL))
    print('Assigned LW file out as {}'.format(file_out))
    
    print('Generating SW Exposure')
    res_wl = nrcWL.gen_exposures(sp, file_outWL)
    
    print('Generating LW Exposure')
    res_sp = nrcGrism.gen_exposures(  sp, file_out)
    
    print('Completed iteration {} & {}'.format(oneFilt, nGROUP))
