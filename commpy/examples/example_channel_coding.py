import numpy as np
import commpy.channelcoding.convcode as cc
import commpy.modulation as modulation

def BER_calc(a, b):
    num_ber = np.sum(np.abs(a - b))
    ber = np.mean(np.abs(a - b))
    return int(num_ber), ber

# N = 100000 #number of symbols per the frame
N = 1000
message_bits = np.random.randint(0, 2, N) # message

M = 4 # modulation order (QPSK)
k = np.log2(M) #number of bit per modulation symbol
modem = modulation.PSKModem(M) # M-PSK modem initialization

generator_matrix = np.array([[5, 7]]) # generator branches
trellis = cc.Trellis(np.array([M]), generator_matrix) # Trellis structure

rate = 1/2 # code rate
L = 7 # constraint length
m = np.array([L-1]) # number of delay elements
tb_depth = 5*(m.sum() + 1) # traceback depth

EbNo = 5  # energy per bit to noise power spectral density ratio (in dB)
snrdB = EbNo + 10 * np.log10(k * rate)  # Signal-to-Noise ratio (in dB)
noiseVar = 10 ** (-snrdB / 10)  # noise variance (power)

N_c = 10  # number of trials

BER_soft = np.zeros(N_c)
BER_hard = np.zeros(N_c)
BER_uncoded = np.zeros(N_c)

for cntr in range(N_c):
    message_bits = np.random.randint(0, 2, N)  # message
    coded_bits = cc.conv_encode(message_bits, trellis)  # encoding

    modulated = modem.modulate(coded_bits)  # modulation
    modulated_uncoded = modem.modulate(message_bits)  # modulation (uncoded case)

    Es = np.mean(np.abs(modulated) ** 2)  # symbol energy
    No = Es / ((10 ** (EbNo / 10)) * np.log2(M))  # noise spectrum density

    noisy = modulated + np.sqrt(No / 2) * \
            (np.random.randn(modulated.shape[0]) + \
             1j * np.random.randn(modulated.shape[0]))  # AWGN

    noisy_uncoded = modulated_uncoded + np.sqrt(No / 2) * \
                    (np.random.randn(modulated_uncoded.shape[0]) + \
                     1j * np.random.randn(modulated_uncoded.shape[0]))  # AWGN (uncoded case)

    demodulated_soft = modem.demodulate(noisy, demod_type='soft', noise_var=noiseVar)  # demodulation (soft output)
    demodulated_hard = modem.demodulate(noisy, demod_type='hard')  # demodulation (hard output)
    demodulated_uncoded = modem.demodulate(noisy_uncoded, demod_type='hard')  # demodulation (uncoded case)

    decoded_soft = cc.viterbi_decode(demodulated_soft, trellis, tb_depth,
                                     decoding_type='unquantized')  # decoding (soft decision)
    decoded_hard = cc.viterbi_decode(demodulated_hard, trellis, tb_depth,
                                     decoding_type='hard')  # decoding (hard decision)

    NumErr, BER_soft[cntr] = BER_calc(message_bits, decoded_soft[:message_bits.size])  # bit-error ratio (soft decision)
    NumErr, BER_hard[cntr] = BER_calc(message_bits, decoded_hard[:message_bits.size])  # bit-error ratio (hard decision)
    NumErr, BER_uncoded[cntr] = BER_calc(message_bits,
                                         demodulated_uncoded[:message_bits.size])  # bit-error ratio (uncoded case)

mean_BER_soft = BER_soft.mean()  # averaged bit-error ratio (soft decision)
mean_BER_hard = BER_hard.mean()  # averaged bit-error ratio (hard decision)
mean_BER_uncoded = BER_uncoded.mean()  # averaged bit-error ratio (uncoded case)

print("Soft decision:\n{}\n".format(mean_BER_soft))
print("Hard decision:\n{}\n".format(mean_BER_hard))
print("Uncoded message:\n{}\n".format(mean_BER_uncoded))