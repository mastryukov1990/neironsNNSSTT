from torchvision.transforms import transforms
import os
from torchvision import datasets
from torch.utils.data import DataLoader
if not os.path.exists('content/summer2winter_yosemite/summerAtrain'):
    os.mkdir('content/summer2winter_yosemite/summerAtrain')
if not os.path.exists('content/summer2winter_yosemite/winterBtrain'):

    os.mkdir('content/summer2winter_yosemite/winterBtrain')
if not os.path.exists('content/summer2winter_yosemite/summerAtest'):
    os.mkdir('content/summer2winter_yosemite/summerAtest')
if not os.path.exists('content/summer2winter_yosemite/winterBtest'):
    os.mkdir('content/summer2winter_yosemite/winterBtest')
if os.path.exists("content/summer2winter_yosemite/testA"):
    os.replace("content/summer2winter_yosemite/testA", "content/summer2winter_yosemite/summerAtest/testA")
if os.path.exists('content/summer2winter_yosemite/trainA'):
    os.replace('content/summer2winter_yosemite/trainA',"content/summer2winter_yosemite/summerAtrain/trainA")
if os.path.exists('content/summer2winter_yosemite/testB'):
    os.replace('content/summer2winter_yosemite/testB',"content/summer2winter_yosemite/winterBtest/testB")
if os.path.exists('content/summer2winter_yosemite/trainB'):
    os.replace('content/summer2winter_yosemite/trainB',"content/summer2winter_yosemite/winterBtrain/trainB")
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
    train_dataset = datasets.ImageFolder(train_path+'/, transform)
    test_dataset = datasets.ImageFolder(test_path, transform)

    # create and return DataLoaders
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, test_loader
