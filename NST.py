
import os


import torch
import torch.nn as nn
import torch.optim as optim

import matplotlib.pyplot as plt


import torchvision.transforms as transforms
from config import device,setting


from StyleLoss import StyleLossByParts,StyleLossAll
from ContentLoss import ContentLoss
from Normalization import Normalization


unloader = transforms.ToPILImage() # тензор в кратинку  


def imshow(tensor, title=None):
    image = tensor.cpu().clone()   
    image = image.squeeze(0)      # функция для отрисовки изображения
    image = unloader(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(0.001) 


class NST:
  def __init__(self,setting):
    self.name = setting['name']
    self.model = None
    self.style_losses = None
    self.content_losses = None
    self.optimizer = None
    self.cnn = setting['cnn']
    self.content_losses = []
    self.style_losses = []
    self.normalization_mean = setting['cnn_normalization_mean']
    self.normalization_std = setting['cnn_normalization_std']
    self.content_layers = setting['content_layers']
    self.style_layers = setting['style_layers']
    self.content_img=setting['content_img']
    self.style_imgs = setting['style_imgs']
    self.input_img=setting['content_img'].clone()
    self.epoches = setting['epoches']
    self.step=0
    self.mode  = setting['mode']
    self.content_weights = setting['content_weights']
    self.style_weights = setting['style_weights']

  def get_input_optimizer(self):
      # this line to show that input is a parameter that requires a gradient
      # добоваляет содержимое тензора катринки в список изменяемых оптимизатором параметров
      self.optimizer = optim.LBFGS([self.input_img.requires_grad_()])


  def get_style_model_and_losses(self):
        
        if self.mode =='All':
          Style = StyleLossAll
        if self.mode =='by_parts':
          Style = StyleLossByParts
        # normalization module
        self.normalization = Normalization(self.normalization_mean, self.normalization_std).to(device)

        # just in order to have an iterable access to or list of content/syle
        # losses
        

        # assuming that cnn is a nn.Sequential, so we make a new nn.Sequential
        # to put in modules that are supposed to be activated sequentially
        self.model = nn.Sequential(self.normalization)

        i = 0  # increment every time we see a conv
        for layer in self.cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                # The in-place version doesn't play very nicely with the ContentLoss
                # and StyleLoss we insert below. So we replace with out-of-place
                # ones here.
                #Переопределим relu уровень
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
            elif isinstance(layer, nn.BatchNorm2d):
                name = 'bn_{}'.format(i)
            else:
                raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

            self.model.add_module(name, layer)

            if name in self.content_layers:
                print(name, name in self.content_layers)
                target = self.model(self.content_img).detach()
                content_loss = ContentLoss(target)
                self.model.add_module("content_loss_{}".format(i), content_loss)
                self.content_losses.append(content_loss)

            if name in self.style_layers:

                target_feature =[ self.model(style_img).detach() for style_img in self.style_imgs]
                style_loss = Style(target_feature, self.style_weights)
                self.model.add_module("style_loss_{}".format(i), style_loss)
                self.style_losses.append(style_loss)

        # now we trim off the layers after the last content and style losses
        #выбрасываем все уровни после последенего styel loss или content loss
        for i in range(len(self.model) - 1, -1, -1):
            if isinstance(self.model[i], ContentLoss) or isinstance(self.model[i], Style):
                break

        self.model = self.model[:(i + 1)]
  def run_style_transfer(self):
        """Run the style transfer."""
        print('Building the style transfer model..')
        self.get_style_model_and_losses()
        self.input_img = self.input_img
        self.get_input_optimizer()
        self.images = []
        print('Optimizing..')
        self.step = 0
        
        while self.step <= self.epoches:

            def closure():
                # correct the values 
                # это для того, чтобы значения тензора картинки не выходили за пределы [0;1]
                self.input_img.data.clamp_(0, 1)

                self.optimizer.zero_grad()

                self.model(self.input_img)

                style_score = 0
                content_score = 0

                for sl in self.style_losses:
                    style_score += sl.loss
                for cl in self.content_losses:
                    content_score += cl.loss
                
                #взвешивание ощибки

                content_score *= self.content_weights[0]

                loss = style_score + content_score
                loss.backward()

                
                if self.step % 1 == 0:
                    print("step {}:".format(self.step))
                    print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                        style_score.item(), content_score.item()))
                    #plt.imsave('samples{}/{}_step{}.jpg'.format(self.name,"NST", str(self.step)),unloader(self.input_img.cpu().clone().squeeze(0)))
         
                    self.images.append(unloader(self.input_img.cpu().clone().squeeze(0)  ).copy())
                    torch.cuda.empty_cache()
                self.step += 1
                return style_score + content_score

            self.optimizer.step(closure)


        self.input_img.data.clamp_(0, 1)


  def create_my_samples(self):
    if not os.path.exists('samples{}'.format(self.name)):
      os.makedirs('samples{}'.format(self.name))


def imshow1(image, title=None, name='ll',figsize=(10,10)):

    fig,axes = plt.subplots(figsize=figsize)
    axes.axis("off")
    axes.imshow(image)
    plt.ioff()
    fig.savefig(name)

