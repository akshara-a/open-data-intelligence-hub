import os
import time
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import torch.nn as nn
# pyrefly: ignore [missing-import]
import torch.optim as optim
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
# pyrefly: ignore [missing-import]
import numpy as np

from data_loader import get_data_loaders
from augmentation import get_train_augmentation
from preprocessing import get_base_transform
from models.baseline_cnn import BaselineCNN
from models.regularized_cnn import RegularizedCNN
from models.deep_cnn import DeepCNN

def train_model(model, train_loader, val_loader, model_name, save_path, epochs=15, lr=0.001, patience=5):
    """
    Trains a given CNN model with Early Stopping and Checkpointing.
    Saves loss/accuracy curves to results/.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n--- Training {model_name} on device: {device} ---")
    model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    best_val_loss = float('inf')
    best_val_acc = 0.0
    patience_counter = 0
    
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
    for epoch in range(1, epochs + 1):
        start_time = time.time()
        
        # Training Phase
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += torch.sum(preds == labels.data).item()
            total_train += labels.size(0)
            
        epoch_train_loss = running_loss / total_train
        epoch_train_acc = correct_train / total_train
        
        # Validation Phase
        model.eval()
        running_val_loss = 0.0
        correct_val = 0
        total_val = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                running_val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                correct_val += torch.sum(preds == labels.data).item()
                total_val += labels.size(0)
                
        epoch_val_loss = running_val_loss / total_val
        epoch_val_acc = correct_val / total_val
        
        history['train_loss'].append(epoch_train_loss)
        history['train_acc'].append(epoch_train_acc)
        history['val_loss'].append(epoch_val_loss)
        history['val_acc'].append(epoch_val_acc)
        
        elapsed = time.time() - start_time
        print(f"Epoch {epoch:02d}/{epochs:02d} [{elapsed:.1f}s] - "
              f"Train Loss: {epoch_train_loss:.4f}, Train Acc: {epoch_train_acc*100:.2f}% | "
              f"Val Loss: {epoch_val_loss:.4f}, Val Acc: {epoch_val_acc*100:.2f}%")
        
        # Checkpointing
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            best_val_acc = epoch_val_acc
            patience_counter = 0
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            torch.save(model.state_dict(), save_path)
            print(f"   Saved best model checkpoint to {save_path} (Val Loss: {best_val_loss:.4f}, Val Acc: {best_val_acc*100:.2f}%)")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"   Early stopping triggered at epoch {epoch}.")
                break

    # Load best weights
    model.load_state_dict(torch.load(save_path))
    return history, best_val_acc

def plot_history(history, model_name, plot_save_path):
    """
    Plots Loss and Accuracy training curves.
    """
    epochs = range(1, len(history['train_loss']) + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Loss Plot
    ax1.plot(epochs, history['train_loss'], 'b-o', label='Train Loss')
    ax1.plot(epochs, history['val_loss'], 'r-s', label='Val Loss')
    ax1.set_title(f'{model_name} - Loss History')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Accuracy Plot
    ax2.plot(epochs, [a * 100 for a in history['train_acc']], 'b-o', label='Train Acc')
    ax2.plot(epochs, [a * 100 for a in history['val_acc']], 'r-s', label='Val Acc')
    ax2.set_title(f'{model_name} - Accuracy History')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(plot_save_path), exist_ok=True)
    plt.savefig(plot_save_path, dpi=300)
    plt.close()
    print(f"Saved training curves to {plot_save_path}")

def run_training():
    train_transform = get_train_augmentation()
    eval_transform = get_base_transform()
    
    train_loader, val_loader, _, _ = get_data_loaders(
        batch_size=64,
        train_transform=train_transform,
        eval_transform=eval_transform
    )
    
    models_to_train = [
        ("CNN 1 (Baseline CNN)", BaselineCNN(), "./models/cnn_baseline.keras", "./results/training_history_cnn1.png"),
        ("CNN 2 (Regularized CNN)", RegularizedCNN(), "./models/cnn_regularized.keras", "./results/training_history_cnn2.png"),
        ("CNN 3 (Deep CNN)", DeepCNN(), "./models/cnn_deep.keras", "./results/training_history_cnn3.png")
    ]
    
    val_accuracies = {}
    for name, model, save_path, plot_path in models_to_train:
        history, best_acc = train_model(model, train_loader, val_loader, name, save_path, epochs=15, lr=0.001, patience=5)
        plot_history(history, name, plot_path)
        val_accuracies[name] = best_acc
        
    print("\n=== Training Completed Successfully ===")
    for name, acc in val_accuracies.items():
        print(f"{name}: Best Validation Accuracy = {acc*100:.2f}%")

if __name__ == "__main__":
    run_training()
