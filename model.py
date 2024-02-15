import numpy as np 
import cv2
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import torch 
import torchvision 
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.transforms import v2
from pathlib import Path
import os 
import random
import torch.nn.functional as F
from sklearn.metrics import (classification_report, confusion_matrix,
                             ConfusionMatrixDisplay)
import PIL
from PIL import Image
torchvision.disable_beta_transforms_warning()

class NepaliCNN(nn.Module):
    def __init__(self, num_classes):
        super(NepaliCNN, self).__init__()

        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.flatten = nn.Flatten()
        
        self.fc1 = nn.Linear(1568, 1000)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(1000,500)
        self.relu4 = nn.ReLU()
        self.fc3 = nn.Linear(500,num_classes)

    def forward(self, x):
        # Convolutional layer 1
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        # Convolutional layer 2
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)

        x = self.flatten(x)
        
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        x = self.relu4(x)
        x = self.fc3(x)
         
        return x
    

index_to_target = {
0: 'अ', 1: 'अं', 2: 'अः', 3: 'आ', 4: 'इ', 5: 'ई', 6: 'उ', 7: 'ऊ', 8: 'ए', 9: 'ऐ', 10: 'ओ', 11: 'औ', 12: 'क', 13: 'क्ष', 14: 'ख', 15: 'ग', 16: 'घ', 17: 'ङ', 18: 'च', 19: 'छ', 20: 'ज', 21: 'ज्ञ', 22: 'झ', 23: 'ञ', 24: 'ट', 25: 'ठ', 26: 'ड', 27: 'ढ', 28: 'ण', 29: 'त', 30: 'त्र', 31: 'थ', 32: 'द', 33: 'ध', 34: 'न', 35: 'प', 36: 'फ', 37: 'ब', 38: 'भ', 39: 'म', 40: 'य', 41: 'र', 42: 'ल', 43: 'व', 44: 'श', 45: 'ष', 46: 'स', 47: 'ह', 48: '०', 49: '१', 50: '२', 51: '३', 52: '४', 53: '५', 54: '६', 55: '७', 56: '८', 57: '९'}
target_to_index = {value:key for key,value in index_to_target.items()}


device = 'cuda:0' if torch.cuda.is_available() else "cpu"

def predict():
    num_classes = 58
    model = NepaliCNN(num_classes).to(device)
    
    model_state_path = "./OwnNepaliCNNstate.pth"
    
    
    model.load_state_dict(torch.load(model_state_path,map_location=device))

