import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def generate_casting_image(is_defective: bool, seed: int) -> Image.Image:
    np.random.seed(seed)
    width, height = 224, 224
    
    # Base metallic gray image
    img = Image.new("RGB", (width, height), color=(180, 185, 190))
    draw = ImageDraw.Draw(img)
    
    # Outer casting rim (concentric circles)
    draw.ellipse([15, 15, 209, 209], fill=(160, 165, 170), outline=(100, 105, 110), width=4)
    draw.ellipse([35, 35, 189, 189], fill=(195, 200, 205), outline=(130, 135, 140), width=3)
    draw.ellipse([60, 60, 164, 164], fill=(150, 155, 160), outline=(90, 95, 100), width=4)
    draw.ellipse([85, 85, 139, 139], fill=(120, 125, 130), outline=(70, 75, 80), width=3)
    
    # Bolt holes
    bolt_centers = [(45, 45), (179, 45), (45, 179), (179, 179), (112, 28), (112, 196)]
    for cx, cy in bolt_centers:
        r = 9
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 55, 60), outline=(20, 25, 30), width=2)
    
    # Add subtle metallic texture noise
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 5, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)
    
    if is_defective:
        # Add high-contrast casting defects (Cracks, Pinhole porosity, Deep gouges)
        defect_type = seed % 3
        if defect_type == 0:
            # Prominent Jagged Crack Defect
            num_points = np.random.randint(5, 9)
            start_x, start_y = np.random.randint(60, 160), np.random.randint(60, 160)
            points = [(start_x, start_y)]
            for _ in range(num_points):
                nx = points[-1][0] + np.random.randint(-20, 20)
                ny = points[-1][1] + np.random.randint(-20, 20)
                points.append((nx, ny))
            draw.line(points, fill=(10, 10, 10), width=5)
            draw.line([(p[0]+1, p[1]+1) for p in points], fill=(40, 40, 40), width=3)
        elif defect_type == 1:
            # Pinhole Cluster / Porosity Defect
            center_x, center_y = np.random.randint(70, 150), np.random.randint(70, 150)
            for _ in range(np.random.randint(12, 25)):
                px = center_x + np.random.randint(-30, 30)
                py = center_y + np.random.randint(-30, 30)
                pr = np.random.randint(3, 7)
                draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(0, 0, 0), outline=(30, 30, 30))
        else:
            # Deep Scratch / Surface Gouge Defect
            sx, sy = np.random.randint(50, 170), np.random.randint(50, 170)
            ex, ey = sx + np.random.randint(-50, 50), sy + np.random.randint(-50, 50)
            draw.line([(sx, sy), (ex, ey)], fill=(5, 5, 5), width=6)
            draw.ellipse([sx-6, sy-6, sx+6, sy+6], fill=(0, 0, 0))
            draw.ellipse([ex-6, ey-6, ex+6, ey+6], fill=(0, 0, 0))
            
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    return img

def setup_dataset(base_dir: str = "data"):
    splits = {
        "train": {"ok_front": 150, "def_front": 150},
        "validation": {"ok_front": 50, "def_front": 50},
        "test": {"ok_front": 50, "def_front": 50}
    }
    
    seed_counter = 100
    for split, counts in splits.items():
        for category, count in counts.items():
            dir_path = os.path.join(base_dir, split, category)
            os.makedirs(dir_path, exist_ok=True)
            is_def = (category == "def_front")
            for i in range(count):
                img_name = f"{category}_{i+1:04d}.jpeg"
                img_path = os.path.join(dir_path, img_name)
                img = generate_casting_image(is_defective=is_def, seed=seed_counter)
                img.save(img_path, format="JPEG")
                seed_counter += 1
                
    print("Enhanced casting dataset generated successfully.")

if __name__ == "__main__":
    setup_dataset()
