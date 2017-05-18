import pynrc
pynrc.setup_logging('WARN', verbose=False)
from pynrc.nrc_utils import S

# Initialize a NIRCam Grism observation in Stripe mode 
for oneFilt,nGROUP in zip(['F444W','F322W2'],[12,6]):
    nrc = pynrc.NIRCam(oneFilt, pupil='GRISM0', module='A', nint=2,ngroup=nGROUP,
                       wind_mode='STRIPE', xpix=2048, ypix=256,read_mode='BRIGHT1')

    nrcWL = pynrc.NIRCam('F210M', pupil='Weak Lens +8', module='A', nint=2,ngroup=nGROUP,
                         wind_mode='STRIPE', xpix=2048, ypix=256)
    # Specify name of output file.
    # Time stamps will be automatically inserted for unique file names.
    bpJ = S.ObsBandpass('johnson,j')
    sp = pynrc.stellar_spectrum('K7V', 9.2, 'vegamag', bpJ)
    file_out = 'sim_img/grism/NRCALONG_'+oneFilt+'_'
    file_outWL = 'sim_img/grism/NRCA1_'+oneFilt+'_'
    res_sp = nrc.gen_exposures(sp, file_out,targ_name='WASP-80')
    res_wl = nrcWL.gen_exposures(sp, file_outWL,targ_name='WASP-80')
