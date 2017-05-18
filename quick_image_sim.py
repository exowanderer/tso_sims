import pynrc
pynrc.setup_logging('WARN', verbose=False)
from pynrc.nrc_utils import S

# Initialize a NIRCam Grism observation in Stripe mode 
for oneFilt in ['F210M','F300M']:
    nrc = pynrc.NIRCam(oneFilt, pupil=None, module='B', nint=4,ngroup=3,
                       wind_mode='WINDOW', xpix=64, ypix=64,read_mode='RAPID')

    bpJ = S.ObsBandpass('johnson,j')
    sp = pynrc.stellar_spectrum('F7V', 9.3, 'vegamag', bpJ)
    thisDetector = nrc.Detectors[0]
    file_out = '/Users/everettschlawin/outside_progs/pynrc_notebooks/sim_img/direct_imaging/'+thisDetector.detname
    # Specify name of output file.
    # Time stamps will be automatically inserted for unique file names.
    res_sp = nrc.gen_exposures(sp, file_out,targ_name='WASP-62')

