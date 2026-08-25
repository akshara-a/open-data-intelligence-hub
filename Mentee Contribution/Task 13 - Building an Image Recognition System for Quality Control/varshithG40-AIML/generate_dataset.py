"""
Synthetic Dataset Generator for Industrial Casting Defect Inspection
Creates realistic 224x224 grayscale/metallic casting product images (impellers).
- ok_front: Non-defective metal casting product (label 0)
- def_front: Defective metal casting product with cracks, porosity, blowholes (label 1)

Configured with lightweight image count (100 total train images, 40 total test images).
"""

import os
import shutil
import random
import numpy as np
import cv2

def draw_base_casting(img_size=224):
    """Draw a realistic metallic pump impeller / casting disk."""
    # Base dark gray background
    img = np.full((img_size, img_size, 3), fill_value=40, dtype=np.uint8)
    
    # Metallic texture noise
    noise = np.random.normal(0, 10, (img_size, img_size, 3)).astype(np.float32)
    img_float = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    center = (img_size // 2, img_size // 2)
    outer_radius = int(img_size * 0.42)
    inner_radius = int(img_size * 0.12)
    
    # Outer rim
    cv2.circle(img_float, center, outer_radius, (180, 185, 190), -1)
    
    # Concentric machining rings
    for r in range(inner_radius + 10, outer_radius - 10, 15):
        cv2.circle(img_float, center, r, (150, 155, 160), 2)
        
    # Central bore / hub
    cv2.circle(img_float, center, inner_radius, (60, 62, 65), -1)
    cv2.circle(img_float, center, inner_radius, (120, 125, 130), 2)
    
    # Radiating spokes
    num_spokes = 6
    for i in range(num_spokes):
        angle = i * (2 * np.pi / num_spokes)
        x1 = int(center[0] + inner_radius * np.cos(angle))
        y1 = int(center[1] + inner_radius * np.sin(angle))
        x2 = int(center[0] + (outer_radius - 8) * np.cos(angle))
        y2 = int(center[1] + (outer_radius - 8) * np.sin(angle))
        cv2.line(img_float, (x1, y1), (x2, y2), (130, 135, 140), 4)
        
    img_blur = cv2.GaussianBlur(img_float, (3, 3), 0)
    return img_blur

def add_defects(img):
    """Add realistic casting defects (cracks, blowholes/porosity, chips, scratches)."""
    img_def = img.copy()
    img_size = img.shape[0]
    center = (img_size // 2, img_size // 2)
    
    defect_types = random.sample(['crack', 'porosity', 'chip', 'scratch'], k=random.randint(1, 3))
    
    for defect in defect_types:
        if defect == 'crack':
            angle = random.uniform(0, 2 * np.pi)
            r_start = random.randint(30, 60)
            x_curr = int(center[0] + r_start * np.cos(angle))
            y_curr = int(center[1] + r_start * np.sin(angle))
            
            pts = [(x_curr, y_curr)]
            for _ in range(random.randint(4, 8)):
                x_curr += random.randint(-15, 15)
                y_curr += random.randint(-15, 15)
                pts.append((x_curr, y_curr))
                
            pts = np.array(pts, np.int32).reshape((-1, 1, 2))
            cv2.polylines(img_def, [pts], isClosed=False, color=(20, 20, 22), thickness=random.randint(2, 4))
            
        elif defect == 'porosity':
            cx = center[0] + random.randint(-40, 40)
            cy = center[1] + random.randint(-40, 40)
            for _ in range(random.randint(5, 12)):
                px = cx + random.randint(-15, 15)
                py = cy + random.randint(-15, 15)
                radius = random.randint(2, 5)
                cv2.circle(img_def, (px, py), radius, (15, 15, 18), -1)
                
        elif defect == 'chip':
            cx = center[0] + random.randint(-50, 50)
            cy = center[1] + random.randint(-50, 50)
            axes = (random.randint(8, 18), random.randint(5, 12))
            angle = random.randint(0, 180)
            cv2.ellipse(img_def, (cx, cy), axes, angle, 0, 360, (25, 25, 28), -1)
            
        elif defect == 'scratch':
            x1 = random.randint(50, 170)
            y1 = random.randint(50, 170)
            x2 = x1 + random.randint(-30, 30)
            y2 = y1 + random.randint(-30, 30)
            cv2.line(img_def, (x1, y1), (x2, y2), (30, 30, 32), 2)
            
    return img_def

def clean_directory(dir_path):
    """Remove all files inside a directory safely."""
    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            fp = os.path.join(dir_path, f)
            if os.path.isfile(fp):
                try:
                    os.unlink(fp)
                except Exception:
                    pass

def generate_dataset(base_dir="data", num_train_per_class=50, num_test_per_class=20):
    """Generate lightweight dataset (100 total train images, 40 total test images)."""
    dirs = [
        os.path.join(base_dir, "train", "ok_front"),
        os.path.join(base_dir, "train", "def_front"),
        os.path.join(base_dir, "test", "ok_front"),
        os.path.join(base_dir, "test", "def_front"),
        "sample_images"
    ]
    
    print("Preparing clean directory structure...")
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        clean_directory(d)
        
    print(f"Generating lightweight dataset ({num_train_per_class*2} train images, {num_test_per_class*2} test images)...")
        
    # Training Images
    for i in range(num_train_per_class):
        base_img = draw_base_casting()
        cv2.imwrite(os.path.join(base_dir, "train", "ok_front", f"cast_ok_{i+1:04d}.jpg"), base_img)
        
        def_img = add_defects(base_img)
        cv2.imwrite(os.path.join(base_dir, "train", "def_front", f"cast_def_{i+1:04d}.jpg"), def_img)
        
    # Test Images
    for i in range(num_test_per_class):
        base_img = draw_base_casting()
        cv2.imwrite(os.path.join(base_dir, "test", "ok_front", f"cast_ok_test_{i+1:04d}.jpg"), base_img)
        
        def_img = add_defects(base_img)
        cv2.imwrite(os.path.join(base_dir, "test", "def_front", f"cast_def_test_{i+1:04d}.jpg"), def_img)
        
    # Sample Images
    sample_files = [
        ("sample_images/sample_ok_1.jpg", False),
        ("sample_images/sample_ok_2.jpg", False),
        ("sample_images/sample_def_1.jpg", True),
        ("sample_images/sample_def_2.jpg", True),
        ("sample_images/sample_def_3.jpg", True),
    ]
    for filepath, is_def in sample_files:
        base_img = draw_base_casting()
        img = add_defects(base_img) if is_def else base_img
        cv2.imwrite(filepath, img)
        
    print("Lightweight dataset generated successfully!")
    print(f"Total Train Images: {num_train_per_class * 2} (50 ok_front, 50 def_front)")
    print(f"Total Test Images : {num_test_per_class * 2} (20 ok_front, 20 def_front)")

if __name__ == "__main__":
    generate_dataset()
