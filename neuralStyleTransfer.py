import matplotlib.pyplot as plt
from NST import NST
from config import setting
def create_and_start(setting):
    Neiron = NST(setting)
    Neiron.create_my_samples()
    Neiron.run_style_transfer()

    def make_image(data, outputname, size=(1, 0.8), dpi=80):
        plt.imshow(data)
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(outputname, bbox_inches='tight',
                    pad_inches=0)
    # data = mpimg.imread(inputname)[:,:,0]

    make_image(Neiron.images[-1], setting['contPicname'])

    return Neiron
