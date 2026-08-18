# pyrefly: ignore [missing-import]
from torchvision import transforms

def get_train_augmentation():
    """
    Data augmentation pipeline for training data only.
    Includes:
    - Random Horizontal Flip
    - Random Crop (padding=4, fill=0)
    - Random Rotation (-15 to +15 deg)
    - Brightness & Contrast Adjustment
    - Pixel Normalization
    """
    return transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2470, 0.2435, 0.2616]
        )
    ])
