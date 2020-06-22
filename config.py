TOKEN= '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
import torchvision.models as models
import torch
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torch.nn as nn
from StyleLoss import gram_matrix
import torch.nn.functional as F
import copy
imsize = [150,150]

loader = transforms.Compose([
    transforms.Resize(imsize),  # нормируем размер изображения
    transforms.CenterCrop(imsize),
    transforms.ToTensor()])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cnn = models.vgg19(pretrained=True).features.to(device).eval()
cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
Path = "C:/Users/ASUS/Dropbox/image1/"

def image_loader(image_name):
    image = Image.open(image_name)
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)





setting = {'cnn': cnn, 'cnn_normalization_mean': cnn_normalization_mean,
           'cnn_normalization_std': cnn_normalization_std,
           'content_img':image_loader(Path+"замок.jpg"),
           'style_imgs': [ image_loader(Path+"вангог.jpg"),
                           image_loader(Path+"крик.jpg"),
                           image_loader(Path+"цвета1.jpg"),

                          ],
           'input': image_loader(Path+"замок.jpg").clone(),
           'epoches': 100,
           'style_weights': [100000, 100000],

           'style_layers':
               ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5', 'conv_6'],
           'name': 'Nst',
           'content_layers':['conv_1'],
           'content_weights': [1],
           'mode': 1,
           'size':imsize}
unloader = transforms.ToPILImage() # тензор в кратинку

def imshow(tensor, title=None):
    image = tensor.cpu().clone()
    image = image.squeeze(0)      # функция для отрисовки изображения
    image = unloader(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(1)
