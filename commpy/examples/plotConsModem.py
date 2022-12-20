# Authors: CommPy contributors
# License: BSD 3-Clause
import matplotlib

from commpy.modulation import PSKModem, QAMModem
import matplotlib.pyplot as plt
# import matplotlib as mpl
# mpl.use('Qt5Agg')
# # import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Example constellation plot of Modem
# =============================================================================

# # Constellation corresponding to PSKModem for 4 bits per symbols
# psk = PSKModem(16)
# psk.plot_constellation()
#
# # Constellation corresponding to QAMModem for 2 bits per symbols
# qam = QAMModem(64)
# qam.plot_constellation()

# %%
bpsk = PSKModem(2)
bpsk.plot_constellation()



# qpsk = PSKModem(4)
# qpsk.plot_constellation()

# #%%
# bpsk = QAMModem(2)
# bpsk.plot_constellation()
# %%
qpsk = QAMModem(4)
qpsk.plot_constellation()

qam16 = QAMModem(16)
qam16.plot_constellation()

qam64 = QAMModem(64)
qam64.plot_constellation()
