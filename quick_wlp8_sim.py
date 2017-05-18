import pynrc
pynrc.setup_logging('WARN', verbose=False)
from pynrc.nrc_utils import S

# Initialize a NIRCam Grism observation in Stripe mode 
nrc = pynrc.NIRCam('F210M', pupil='Weak Lens +8', module='A', nint=2,ngroup=2,
                   wind_mode='STRIPE', xpix=2048, ypix=256)
# Specify name of output file.
# Time stamps will be automatically inserted for unique file names.
bpk = S.ObsBandpass('johnson,k')
sp = pynrc.stellar_spectrum('G2V', 8, 'vegamag', bpk)
file_out = '/Users/everettschlawin/outside_progs/pynrc_notebooks/sim_img/NRCN'
res_sp = nrc.gen_exposures(sp, file_out,targ_name='Example G2V')
