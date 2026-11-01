import os
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
from torch.utils.data import DataLoader, Subset
# pyrefly: ignore [missing-import]
from torchvision import datasets, transforms
# pyrefly: ignore [missing-import]
import numpy as np

# CIFAR-10 Class labels
CIFAR10_CLASSES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

def get_data_loaders(data_dir='./data', batch_size=32, train_transform=None, eval_transform=None, seed=42):
    """
    Loads CIFAR-10 dataset and creates deterministic Train (70%), Validation (15%), Test (15%) loaders.
    Ensures all models use the exact same splits for fair evaluation.
    """
    os.makedirs(data_dir, exist_ok=True)
    
    if train_transform is None:
        train_transform = transforms.ToTensor()
    if eval_transform is None:
        eval_transform = transforms.ToTensor()

    # Load complete CIFAR-10 train and test sets to construct combined pool
    full_train = datasets.CIFAR10(root=data_dir, train=True, download=True, transform=train_transform)
    full_test = datasets.CIFAR10(root=data_dir, train=False, download=True, transform=eval_transform)
    
    # We will also create eval dataset version for validation/test without augmentation
    full_train_eval = datasets.CIFAR10(root=data_dir, train=True, download=False, transform=eval_transform)

    # Total samples across train+test = 60,000
    # 70% train (42,000), 15% val (9,000), 15% test (9,000)
    np.random.seed(seed)
    total_indices = np.arange(len(full_train) + len(full_test))
    np.random.shuffle(total_indices)
    
    train_end = int(0.70 * len(total_indices))
    val_end = train_end + int(0.15 * len(total_indices))
    
    train_idx = total_indices[:train_end]
    val_idx = total_indices[train_end:val_end]
    test_idx = total_indices[val_end:]
    
    # Map indices: 0..49999 to full_train, 50000..59999 to full_test
    def get_subset(indices, dataset_augmented, dataset_clean):
        train_subset_list = []
        for idx in indices:
            if idx < 50000:
                train_subset_list.append((dataset_augmented[idx] if dataset_augmented else dataset_clean[idx]))
            else:
                train_subset_list.append(dataset_clean[idx - 50000])
        return train_subset_list

    train_data = get_subset(train_idx, full_train, full_train_eval)
    val_data = get_subset(val_idx, None, full_train_eval)
    test_data = get_subset(test_idx, None, full_train_eval)
    
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False, num_workers=0)
    
    return train_loader, val_loader, test_loader, CIFAR10_CLASSES
