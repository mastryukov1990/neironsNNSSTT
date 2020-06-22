

import torch
import torch.nn as nn
import torch.nn.functional as F


def gram_matrix(input):
        batch_size , h, w, f_map_num = input.size()  # batch size(=1)
        # b=number of feature maps
        # (h,w)=dimensions of a feature map (N=h*w)
        features = torch.div(input,2).view(batch_size * h, w * f_map_num)  # resise F_XL into \hat F_XL

        G = torch.mm(features, features.t())  # compute the gram product

        # we 'normalize' the values of the gram matrix
        # by dividing by the number of element in each feature maps.
        return G.div(batch_size * h * w * f_map_num)


class StyleLossAll(nn.Module):

    def __init__(self, target_feature,style_weights):
        super(StyleLossAll, self).__init__()
        self.targets = [gram_matrix(i) for i in target_feature]
        self.loss = F.mse_loss(self.targets[0], self.targets[0])  # to initialize with something
        self.style_weights = style_weights

    def forward(self, input):
        self.loss = 0
        for i,weight in zip(self.targets,self.style_weights):
            G = gram_matrix(input)
            self.loss += F.mse_loss(G, i)*weight

        return input






class StyleLossByParts(nn.Module):
    def __init__(self, target_feature,weights):
        super(StyleLossByParts, self).__init__()
        self.W = target_feature[0].size()[3]
        self.target_feature = target_feature
        self.num_t = len(target_feature)
        self.targets = [gram_matrix(torch.div(target_feature[i][..., i*self.W // len(target_feature):(i+1)*self.W // len(target_feature)], 2)).detach()
                        for i in range(self.num_t)]
        self.loss = F.mse_loss(self.targets[0], self.targets[0])  # to initialize with something
        self.weights = weights
    def forward(self, input):

        Gs = [gram_matrix(input[..., i*self.W // self.num_t:(i+1)*self.W // self.num_t])
                        for i in range(self.num_t)]
        self.loss=0
        for i in range(self.num_t):
            self.loss += F.mse_loss(Gs[i], self.targets[i])*self.weights[i]
        return input




def create_parts(self,input):
        parts = []

        for i in range(self.num_p):
            t = int(self.size/self.num_p)

            parts.append(input[...,t*i:t*(i+1)])
        return parts
def create_parts_style(self,input):
        parts = []

        for i in range(self.num_p):
            t = int(self.size/self.num_p)

            parts.append(input[0][...,t*i:t*(i+1)].clone())
        return parts
