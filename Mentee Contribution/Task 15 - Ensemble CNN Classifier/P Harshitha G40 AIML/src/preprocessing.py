# pyrefly: ignore [missing-import]
from torchvision import transforms

def get_base_transform():
    """
    Standard evaluation transform:
    Normalizes images to range [0, 1] using standard CIFAR-10 mean and std.
    """
    return transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2470, 0.2435, 0.2616]
        )
    ])

def denormalize_image(tensor):
    """
    Utility to convert normalized tensor back to [0, 1] image array for display.
    """
    mean = [0.4914, 0.4822, 0.4465]
    std = [0.2470, 0.2435, 0.2616]
    
    t = tensor.clone()
    for i in range(3):
        t[i] = t[i] * std[i] + mean[i]
    return t.clamp(0, 1)
