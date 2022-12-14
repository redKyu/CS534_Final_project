import os
import torch
import torch.nn as nn
import torchvision
from model.encoder import Encoder
from model.encoder import CNN_PRESET
from torchvision.transforms import ToPILImage
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt

from dataset.dataset import LargeCAPTCHA

def test_encoder(params):

    _Encoder = torch.load(os.path.join(params['encoder_save_path'], params['model_name']))

    if torch.cuda.is_available():
        USE_CUDA = True
    else:
        USE_CUDA = False


    # transform 
    _transform = [torchvision.transforms.Compose([
                        torchvision.transforms.ToTensor(),
                    ]),
                    torchvision.transforms.Compose([
                        torchvision.transforms.ToTensor(),
                    ]),
                    torchvision.transforms.Compose([
                        torchvision.transforms.ToTensor(),
                    ])]

    # dataset
    _datapath = os.path.join(params['datapath'], params['dataset'])
    _data = LargeCAPTCHA(_datapath, (0.8, 0.1, 0.1), transform=_transform)

    _train_loader = DataLoader(_data.train, batch_size=params['batch_size'])
    
    _img, _label = next(iter(_train_loader))

    if USE_CUDA:
        _img = _img.cuda()
        _Encoder.cuda()

    _pred = _Encoder(_img)

    fig, ax = plt.subplots(params['batch_size'], 2)
    cols = ['Original', 'Encoded']
    for _ax, _col in zip(ax[0], cols):
        _ax.set_title(_col)

    for i in range(params['batch_size']):
        ax[i, 0].imshow(ToPILImage()(_img[i]), cmap='gray', vmin=0, vmax=255)
        ax[i, 1].imshow(ToPILImage()(_pred[i]), cmap='gray', vmin=0, vmax=255)

    fig_save_path = os.path.join(params['encoder_save_path'], params['model_name']+"test_imgs")
    os.makedirs(fig_save_path, exist_ok=True)
    fig.savefig(os.path.join(fig_save_path, "img.png"))

# /home/hongkyu/Documents/projects/CS534_FINAL/model/saved_encoder_processors/CAPTCHA_LARGE/3/1670658565.0962765/model_2750_4.597142804414034.pt

if __name__ == "__main__":
    _params = {
        'epoch': 10,
        'batch_size': 4,
        'layer_config' : [-1, -1, 0, 0, 1, 1],
        'cnn_config' : CNN_PRESET[0],
        'encoder_save_path' : './model/saved_encoder_processors/CAPTCHA_LARGE/3/1670658565.0962765',
        'model_name' : 'model_2750_4.597142804414034.pt',
        'datapath' : './dataset/',
        'dataset' : 'CAPTCHA_LARGE'
    }
    test_encoder(_params)


    