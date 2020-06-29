import os
import torch
from torch.utils.data import DataLoader
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import torchvision.utils as vutils
# visualizing data
import matplotlib.pyplot as plt
import numpy as np
import warnings
from config import batch_size,workers
from torch.utils.data import DataLoader

from torch import nn
import torch.functional as F




def get_data_loader(image_type, image_dir='content/summer2winter_yosemite',
                    image_size=128, batch_size=16, num_workers=0):
    """Returns training and test data loaders for a given image type, either 'summer' or 'winter'.
       These images will be resized to 128x128x3, by default, converted into Tensors, and normalized.
    """

    # resize and normalize the images
    transform = transforms.Compose([transforms.Resize(image_size),  # resize to 128x128
                                    transforms.ToTensor()])

    # get training and test directories
    image_path = image_dir
    print(os.listdir(image_path+'{}train'.format(image_type)))
    train_path = os.path.join(image_path, '{}train'.format(image_type))
    test_path = os.path.join(image_path, '{}test'.format(image_type))

    # define datasets using ImageFolder
    train_dataset = datasets.ImageFolder(train_path+'/', transform)
    test_dataset = datasets.ImageFolder(test_path, transform)

    # create and return DataLoaders
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, test_loader


def to_data(x):
    """Converts variable to numpy."""
    if torch.cuda.is_available():
        x = x.cpu()
    x = x.data.numpy()
    x = ((x + 1) * 255 / (2)).astype(np.uint8)  # rescale to 0-255
    return x


def save_samples(iteration, fixed_Y, fixed_X, G_YtoX, G_XtoY, batch_size=16, sample_dir='samples_cyclegan'):
    """Saves samples from both generators X->Y and Y->X.
        """
    # move input data to correct device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    fake_X = G_YtoX(fixed_Y.to(device))
    fake_Y = G_XtoY(fixed_X.to(device))

    X, fake_X = to_data(fixed_X), to_data(fake_X)
    Y, fake_Y = to_data(fixed_Y), to_data(fake_Y)

    merged = merge_images(X, fake_Y, batch_size)
    path = os.path.join(sample_dir, 'sample-{:06d}-X-Y.png'.format(iteration))
    imageio.imwrite(path, merged)
    print('Saved {}'.format(path))

    merged = merge_images(Y, fake_X, batch_size)
    path = os.path.join(sample_dir, 'sample-{:06d}-Y-X.png'.format(iteration))
    imageio.imwrite(path, merged)
    print('Saved {}'.format(path))

def scale(x, feature_range=(-1, 1)):
    ''' Scale takes in an image x and returns that image, scaled
       with a feature_range of pixel values from -1 to 1.
       This function assumes that the input x is already scaled from 0-1.'''

    # scale from 0-1 to feature_range
    min, max = feature_range
    x = x * (max - min) + min
    return x





# helper conv function
def conv(in_channels, out_channels, kernel_size, stride=2, padding=1, batch_norm=True, relu=True):
    """Creates a convolutional layer, with optional batch normalization.
    """
    layers = []
    conv_layer = nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                           kernel_size=kernel_size, stride=stride, padding=padding, bias=False)

    layers.append(conv_layer)

    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
    if relu:
        layers.append(nn.ReLU())
    return nn.Sequential(*layers)




class ResidualBlock(nn.Module):
  def __init__(self,conv_dim):
    super(ResidualBlock,self).__init__()
    self.conv1 = conv(conv_dim,conv_dim,3,1,1,relu=False)
    self.conv2 = conv(conv_dim,conv_dim,3,1,1,relu = False)
  def forward(self,x):
    out = self.conv1(x)
    out2 = self.conv2(out) + x
    return out2
def deconv(in_channels,out_channels,kernel_size,stride = 2,padding = 1,batch_norm = True):
  layers = []
  layers.append(nn.ConvTranspose2d(in_channels,out_channels,kernel_size,stride,padding,bias = False))
  layers.append
  if batch_norm:
    layers.append(nn.BatchNorm2d(out_channels))
  return nn.Sequential(*layers)





class CycleGenerator(nn.Module):
    def __init__(self, conv_d, num_res_blocks=6):
        super(CycleGenerator, self).__init__()

        self.conv1 = conv(3, conv_d, 4)
        self.conv2 = conv(conv_d, conv_d * 2, 4)
        self.conv3 = conv(conv_d * 2, conv_d * 4, 4)

        layers = []
        for i in range(num_res_blocks):
            layers.append(ResidualBlock(conv_dim=conv_d * 4))
        self.res_blocks = nn.Sequential(*layers)

        self.deconv1 = deconv(conv_d * 4, conv_d * 2, 4)
        self.deconv2 = deconv(conv_d * 2, conv_d, 4)
        self.deconv3 = deconv(conv_d, 3, 4, batch_norm=False)

    def forward(self, x):
        """Given an image x, returns a transformed image."""
        # define feedforward behavior, applying activations as necessary

        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)

        out = self.res_blocks(out)

        out = F.relu(self.deconv1(out))
        out = F.relu(self.deconv2(out))
        out = F.tanh(self.deconv3(out))  # tanh activation in last layer

        return out


def create_model(g_conv_dim=64, d_conv_dim=64, n_res_blocks=6):
    """Builds the generators and discriminators."""

    # Instantiate generators
    G_XtoY = CycleGenerator(conv_d=d_conv_dim, num_res_blocks=n_res_blocks)
    G_YtoX = CycleGenerator(conv_d=d_conv_dim, num_res_blocks=n_res_blocks)
    # Instantiate discriminators

    # move models to GPU, if available
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        G_XtoY.to(device)
        G_YtoX.to(device)

        print('Models moved to GPU.')
    else:
        print('Only CPU available.')

    return G_XtoY, G_YtoX


G_XtoY, G_YtoX = create_model()
G_XtoY.load_state_dict(torch.load('content/веса/G_XtoY(10000).pkl',map_location='cpu'), strict=False)
transform = transforms.Compose([transforms.Resize(256),  # resize to 128x128
                                    transforms.ToTensor()])
test_dataset = datasets.ImageFolder('content/summer2winter_yosemite/summerAtest/', transform)



    # create and return DataLoaders
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True, num_workers=2)

test_iter_X = iter(test_loader)


# Get some fixed data from domains X and Y for sampling. These are images that are held
# constant throughout training, that allow us to inspect the model's performance.
fixed_X = test_iter_X.next()[0]
fixed_X = scale(fixed_X) # make sure to scale to a range -1 to 1

G_XtoY.eval()
G_XtoY(fixed_X)