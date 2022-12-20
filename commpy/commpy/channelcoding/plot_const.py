

def plot_constellation(rxs):
    """ Plot the constellation """
    plt.figure(figsize=(10, 10), dpi=120)
    plt.scatter(rxs.real, rxs.imag)

    # for symb in self.constellation:
    #     plt.text(symb.real + .1, symb.imag, str(self.demodulate(symb, 'hard')[:]))

    plt.title('Constellation')
    plt.grid()
    plt.show()