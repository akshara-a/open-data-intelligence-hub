import os
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import torch.nn as nn
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, accuracy_score

from data_loader import get_data_loaders
from preprocessing import get_base_transform
from models.baseline_cnn import BaselineCNN
from models.regularized_cnn import RegularizedCNN
from models.deep_cnn import DeepCNN

def plot_confusion_matrix(cm, classes, model_name, save_path):
    """
    Generates and saves a confusion matrix visualization heatmap.
    """
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=classes, yticklabels=classes)
    plt.title(f'Confusion Matrix - {model_name}', fontsize=14, pad=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved confusion matrix plot to {save_path}")

def evaluate_single_model(model, test_loader, classes, model_name, save_cm_path=None):
    """
    Evaluates a single model on test_loader and computes metrics.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)
            
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
    total_loss /= len(test_loader.dataset)
    acc = accuracy_score(all_targets, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_targets, all_preds, average='macro')
    cm = confusion_matrix(all_targets, all_preds)
    
    if save_cm_path:
        plot_confusion_matrix(cm, classes, model_name, save_cm_path)
        
    metrics = {
        'model_name': model_name,
        'loss': total_loss,
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'all_preds': np.array(all_preds),
        'all_targets': np.array(all_targets),
        'all_probs': np.array(all_probs)
    }
    
    return metrics

def run_evaluation():
    eval_transform = get_base_transform()
    _, _, test_loader, classes = get_data_loaders(
        batch_size=64,
        eval_transform=eval_transform
    )
    
    models_info = [
        ("CNN 1 (Baseline)", BaselineCNN(), "./models/cnn_baseline.keras", "./results/confusion_matrix_cnn1.png"),
        ("CNN 2 (Regularized)", RegularizedCNN(), "./models/cnn_regularized.keras", "./results/confusion_matrix_cnn2.png"),
        ("CNN 3 (Deep)", DeepCNN(), "./models/cnn_deep.keras", "./results/confusion_matrix_cnn3.png")
    ]
    
    results = []
    for name, model, weight_path, cm_path in models_info:
        if os.path.exists(weight_path):
            model.load_state_dict(torch.load(weight_path, weights_only=True if hasattr(torch, 'load') else False))
            metrics = evaluate_single_model(model, test_loader, classes, name, cm_path)
            results.append(metrics)
            print(f"\n--- {name} Results ---")
            print(f"Accuracy:  {metrics['accuracy']*100:.2f}%")
            print(f"Precision: {metrics['precision']*100:.2f}%")
            print(f"Recall:    {metrics['recall']*100:.2f}%")
            print(f"F1-Score:  {metrics['f1_score']*100:.2f}%")
            print(f"Loss:      {metrics['loss']:.4f}")
        else:
            print(f"Warning: Checkpoint {weight_path} not found. Train the model first.")
            
    return results

if __name__ == "__main__":
    run_evaluation()
