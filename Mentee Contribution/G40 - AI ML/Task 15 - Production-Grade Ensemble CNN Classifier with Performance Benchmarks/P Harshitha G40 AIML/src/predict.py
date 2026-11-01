import os
import time
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from PIL import Image
# pyrefly: ignore [missing-import]
from torchvision import transforms

from preprocessing import get_base_transform
from models.baseline_cnn import BaselineCNN
from models.regularized_cnn import RegularizedCNN
from models.deep_cnn import DeepCNN
from data_loader import CIFAR10_CLASSES

class EnsemblePredictor:
    """
    Production-Grade Inference Pipeline with Confidence Thresholding.
    """
    def __init__(self, confidence_threshold=0.80):
        self.confidence_threshold = confidence_threshold
        self.classes = CIFAR10_CLASSES
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transform = get_base_transform()
        
        self.cnn1 = BaselineCNN().to(self.device)
        self.cnn2 = RegularizedCNN().to(self.device)
        self.cnn3 = DeepCNN().to(self.device)
        
        self.cnn1.load_state_dict(torch.load("./models/cnn_baseline.keras"))
        self.cnn2.load_state_dict(torch.load("./models/cnn_regularized.keras"))
        self.cnn3.load_state_dict(torch.load("./models/cnn_deep.keras"))
        
        self.cnn1.eval()
        self.cnn2.eval()
        self.cnn3.eval()

    def predict_image(self, image_input):
        """
        Processes a PIL Image or Image Filepath and returns production JSON payload.
        """
        start_time = time.time()
        
        if isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"Image not found at path {image_input}")
            img = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, Image.Image):
            img = image_input.convert('RGB')
        else:
            raise ValueError("Input must be a valid image path or PIL Image object.")

        # Resize if necessary
        if img.size != (32, 32):
            img = img.resize((32, 32))
            
        tensor_img = self.transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            out1 = self.cnn1(tensor_img)
            out2 = self.cnn2(tensor_img)
            out3 = self.cnn3(tensor_img)
            
            p1 = torch.softmax(out1, dim=1).cpu().numpy()[0]
            p2 = torch.softmax(out2, dim=1).cpu().numpy()[0]
            p3 = torch.softmax(out3, dim=1).cpu().numpy()[0]
            
            ens_probs = (p1 + p2 + p3) / 3.0
            
            pred_class_idx = np.argmax(ens_probs)
            predicted_class = self.classes[pred_class_idx]
            confidence = float(ens_probs[pred_class_idx])
            
            c1_pred = self.classes[np.argmax(p1)]
            c2_pred = self.classes[np.argmax(p2)]
            c3_pred = self.classes[np.argmax(p3)]

        inference_time_ms = (time.time() - start_time) * 1000.0
        
        decision = "Accepted" if confidence >= self.confidence_threshold else "Manual Review Required (Low Confidence)"
        
        response = {
            "predictedClass": predicted_class,
            "confidence": round(confidence, 4),
            "decision": decision,
            "inferenceTimeMs": round(inference_time_ms, 2),
            "modelPredictions": {
                "cnn1_baseline": c1_pred,
                "cnn2_regularized": c2_pred,
                "cnn3_deep": c3_pred
            },
            "individualProbabilities": {
                "cnn1": float(round(p1[pred_class_idx], 4)),
                "cnn2": float(round(p2[pred_class_idx], 4)),
                "cnn3": float(round(p3[pred_class_idx], 4))
            }
        }
        
        return response

if __name__ == "__main__":
    predictor = EnsemblePredictor(confidence_threshold=0.75)
    # Test with dummy image
    dummy_img = Image.fromarray((np.random.rand(32, 32, 3) * 255).astype('uint8'))
    result = predictor.predict_image(dummy_img)
    import json
    print(json.dumps(result, indent=2))
