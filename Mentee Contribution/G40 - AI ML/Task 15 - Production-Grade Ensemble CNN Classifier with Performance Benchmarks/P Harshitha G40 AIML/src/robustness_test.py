import os
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import numpy as np
import pandas as pd
# pyrefly: ignore [missing-import]
from torchvision import transforms
# pyrefly: ignore [missing-import]
from PIL import Image, ImageFilter
from sklearn.metrics import accuracy_score

from data_loader import get_data_loaders
from preprocessing import get_base_transform
from models.baseline_cnn import BaselineCNN
from models.regularized_cnn import RegularizedCNN
from models.deep_cnn import DeepCNN

def apply_perturbation(img_tensor, perturbation_type):
    """
    Applies real-world perturbations to normalized image tensors.
    """
    # Denormalize to [0, 1] PIL Image
    mean = torch.tensor([0.4914, 0.4822, 0.4465]).view(3, 1, 1)
    std = torch.tensor([0.2470, 0.2435, 0.2616]).view(3, 1, 1)
    
    unnorm = img_tensor * std + mean
    unnorm = unnorm.clamp(0, 1)
    pil_img = transforms.ToPILImage()(unnorm)
    
    if perturbation_type == 'Original':
        modified_pil = pil_img
    elif perturbation_type == 'Rotated (+30°)':
        modified_pil = pil_img.rotate(30)
    elif perturbation_type == 'Blurred (Gaussian)':
        modified_pil = pil_img.filter(ImageFilter.GaussianBlur(radius=1.5))
    elif perturbation_type == 'Darkened (0.5x)':
        t = transforms.ToTensor()(pil_img) * 0.5
        return transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2470, 0.2435, 0.2616])(t)
    elif perturbation_type == 'Brightened (1.5x)':
        t = (transforms.ToTensor()(pil_img) * 1.5).clamp(0, 1)
        return transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2470, 0.2435, 0.2616])(t)
    elif perturbation_type == 'Noisy (Gaussian)':
        t = transforms.ToTensor()(pil_img)
        noise = torch.randn_like(t) * 0.1
        t = (t + noise).clamp(0, 1)
        return transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2470, 0.2435, 0.2616])(t)
    elif perturbation_type == 'Cropped & Resized':
        w, h = pil_img.size
        crop_box = (w * 0.15, h * 0.15, w * 0.85, h * 0.85)
        modified_pil = pil_img.crop(crop_box).resize((32, 32))
    else:
        modified_pil = pil_img
        
    t = transforms.ToTensor()(modified_pil)
    return transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2470, 0.2435, 0.2616])(t)

def run_robustness_tests(sample_limit=1000):
    eval_transform = get_base_transform()
    _, _, test_loader, classes = get_data_loaders(batch_size=64, eval_transform=eval_transform)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    cnn1 = BaselineCNN().to(device)
    cnn2 = RegularizedCNN().to(device)
    cnn3 = DeepCNN().to(device)
    
    cnn1.load_state_dict(torch.load("./models/cnn_baseline.keras"))
    cnn2.load_state_dict(torch.load("./models/cnn_regularized.keras"))
    cnn3.load_state_dict(torch.load("./models/cnn_deep.keras"))
    
    cnn1.eval()
    cnn2.eval()
    cnn3.eval()
    
    perturbations = [
        'Original',
        'Rotated (+30°)',
        'Blurred (Gaussian)',
        'Noisy (Gaussian)',
        'Darkened (0.5x)',
        'Brightened (1.5x)',
        'Cropped & Resized'
    ]
    
    results = []
    
    for pert in perturbations:
        targets = []
        preds1, preds2, preds3, preds_ens = [], [], [], []
        
        count = 0
        with torch.no_grad():
            for images, labels in test_loader:
                if count >= sample_limit:
                    break
                
                # Apply perturbation image by image
                pert_imgs = torch.stack([apply_perturbation(img, pert) for img in images]).to(device)
                labels = labels.to(device)
                
                out1 = cnn1(pert_imgs)
                out2 = cnn2(pert_imgs)
                out3 = cnn3(pert_imgs)
                
                p1 = torch.softmax(out1, dim=1)
                p2 = torch.softmax(out2, dim=1)
                p3 = torch.softmax(out3, dim=1)
                
                p_ens = (p1 + p2 + p3) / 3.0
                
                preds1.extend(torch.argmax(p1, dim=1).cpu().numpy())
                preds2.extend(torch.argmax(p2, dim=1).cpu().numpy())
                preds3.extend(torch.argmax(p3, dim=1).cpu().numpy())
                preds_ens.extend(torch.argmax(p_ens, dim=1).cpu().numpy())
                targets.extend(labels.cpu().numpy())
                
                count += len(images)
                
        acc1 = accuracy_score(targets, preds1)
        acc2 = accuracy_score(targets, preds2)
        acc3 = accuracy_score(targets, preds3)
        acc_ens = accuracy_score(targets, preds_ens)
        
        results.append({
            'Perturbation': pert,
            'CNN 1 Acc': f"{acc1*100:.2f}%",
            'CNN 2 Acc': f"{acc2*100:.2f}%",
            'CNN 3 Acc': f"{acc3*100:.2f}%",
            'Ensemble Acc': f"{acc_ens*100:.2f}%",
            'Ensemble Gain': f"+{(acc_ens - max(acc1, acc2, acc3))*100:.2f}%"
        })
        
    df = pd.DataFrame(results)
    os.makedirs("./results", exist_ok=True)
    csv_path = "./results/robustness_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved robustness results to {csv_path}\n")
    print(df.to_string(index=False))
    
    return df

if __name__ == "__main__":
    run_robustness_tests()
