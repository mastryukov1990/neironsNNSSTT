import matplotlib.pyplot as plt
from NST import NST
from config import setting
def create_and_start(setting):
    Neiron = NST(setting)
    Neiron.create_my_samples()
    Neiron.run_style_transfer()

    fig,axes = plt.subplots(figsize=(10,13))
    axes.axis('off')
    plt.imshow(Neiron.images[setting['epoches']])
    fig.savefig(setting['contPicname'])
    return Neiron
