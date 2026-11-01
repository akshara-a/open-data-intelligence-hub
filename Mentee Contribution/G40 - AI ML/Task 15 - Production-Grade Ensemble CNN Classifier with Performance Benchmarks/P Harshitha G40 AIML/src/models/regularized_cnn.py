# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import torch.nn as nn
# pyrefly: ignore [missing-import]
import torch.nn.functional as F

class RegularizedCNN(nn.Module):
    """
    CNN Model 2 — Regularized CNN
    Incorporate Batch Normalization and Dropout to reduce overfitting and improve training stability.
    """
    def __init__(self, num_classes=10):
        super(RegularizedCNN, self).__init__()
        # Conv Block 1
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.drop1 = nn.Dropout2d(0.25)
        
        # Conv Block 2
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.drop2 = nn.Dropout2d(0.25)
        
        # Conv Block 3
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.drop3 = nn.Dropout2d(0.30)
        
        # Fully Connected Layers
        self.fc1 = nn.Linear(128 * 8 * 8, 256)
        self.bn_fc1 = nn.BatchNorm1d(256)
        self.drop_fc = nn.Dropout(0.50)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.drop1(self.pool1(F.relu(self.bn1(self.conv1(x)))))
        x = self.drop2(self.pool2(F.relu(self.bn2(self.conv2(x)))))
        x = self.drop3(F.relu(self.bn3(self.conv3(x))))
        x = x.view(x.size(0), -1)
        x = self.drop_fc(F.relu(self.bn_fc1(self.fc1(x))))
        x = self.fc2(x)
        return x
