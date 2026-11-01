import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def create_casting_image(is_defective: bool, seed: int) -> Image.Image:
    """
    Generates a synthetic casting flange image (224x224x3).
    Non-defective ('ok_front'): Clean metallic flange with uniform machining concentric circles.
    Defective ('def_front'): Casting flange with prominent dark cracks, pitting holes, and voids.
    """
    np.random.seed(seed)
    width, height = 224, 224
    
    # Base metallic background
    base_gray = np.random.randint(120, 135)
    img_arr = np.full((height, width, 3), base_gray, dtype=np.uint8)
    
    # Subtle metallic grain texture
    noise = np.random.randint(-8, 8, (height, width, 3), dtype=np.int16)
    img_arr = np.clip(img_arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    img = Image.fromarray(img_arr)
    draw = ImageDraw.Draw(img)
    
    center = (112, 112)
    outer_radius = 95
    inner_radius = 35
    
    # Outer casting rim
    draw.ellipse(
        [center[0] - outer_radius, center[1] - outer_radius, center[0] + outer_radius, center[1] + outer_radius],
        outline=(190, 190, 195), width=5
    )
    # Inner shaft hole
    draw.ellipse(
        [center[0] - inner_radius, center[1] - inner_radius, center[0] + inner_radius, center[1] + inner_radius],
        fill=(30, 30, 35), outline=(170, 170, 175), width=4
    )
    
    # Concentric machining grooves
    for r in range(inner_radius + 12, outer_radius - 8, 12):
        shade = int(145 + 15 * np.sin(r / 4.0))
        draw.ellipse(
            [center[0] - r, center[1] - r, center[0] + r, center[1] + r],
            outline=(shade, shade, shade + 5), width=2
        )
    
    # 4 Bolt hole cutouts
    for angle in [0, 90, 180, 270]:
        rad = np.radians(angle)
        bx = int(center[0] + 65 * np.cos(rad))
        by = int(center[1] + 65 * np.sin(rad))
        draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(45, 45, 50), outline=(180, 180, 185), width=2)
    
    # Defect Injection for defective class ('def_front')
    if is_defective:
        num_defects = np.random.randint(3, 6)
        for _ in range(num_defects):
            angle = np.random.uniform(0, 2 * np.pi)
            dist = np.random.uniform(inner_radius + 12, outer_radius - 15)
            dx = int(center[0] + dist * np.cos(angle))
            dy = int(center[1] + dist * np.sin(angle))
            
            defect_type = np.random.choice(["crack", "pit", "void"])
            
            if defect_type == "crack":
                # Prominent dark jagged crack line
                points = [(dx, dy)]
                cx, cy = dx, dy
                for _ in range(np.random.randint(4, 9)):
                    cx += np.random.randint(-12, 13)
                    cy += np.random.randint(-12, 13)
                    points.append((cx, cy))
                draw.line(points, fill=(5, 5, 5), width=4)
                
            elif defect_type == "pit":
                # Deep pitting crater hole
                pr = np.random.randint(6, 12)
                draw.ellipse([dx - pr, dy - pr, dx + pr, dy + pr], fill=(5, 5, 5), outline=(120, 30, 20), width=3)
                
            elif defect_type == "void":
                # Porosity cluster of dark voids
                for _ in range(12):
                    vx = dx + np.random.randint(-12, 13)
                    vy = dy + np.random.randint(-12, 13)
                    draw.ellipse([vx - 3, vy - 3, vx + 3, vy + 3], fill=(0, 0, 0))

    img = img.filter(ImageFilter.SMOOTH)
    return img

def generate_full_dataset(base_dir: str = "data"):
    splits = {
        "train": {"ok_front": 50, "def_front": 50},
        "val": {"ok_front": 10, "def_front": 10},
        "test": {"ok_front": 10, "def_front": 10},
        "unseen": {"ok_front": 3, "def_front": 3}
    }
    
    seed = 42
    for split, counts in splits.items():
        for cls_name, count in counts.items():
            if split == "unseen":
                target_dir = os.path.join(base_dir, "unseen")
            else:
                target_dir = os.path.join(base_dir, split, cls_name)
            os.makedirs(target_dir, exist_ok=True)
            
            is_defective = (cls_name == "def_front")
            for i in range(count):
                seed += 1
                img = create_casting_image(is_defective, seed)
                if split == "unseen":
                    filename = f"unseen_sample_{i+1}_{cls_name}.png"
                else:
                    filename = f"{cls_name}_{i+1:04d}.png"
                img.save(os.path.join(target_dir, filename))
                
    print("Dataset generation complete!")

if __name__ == "__main__":
    generate_full_dataset()
