
"""
Image utilities for Soldier Unplugged
Expects:
  data/ppdt.pdf  -> 100 PPDT pictures
  data/tat.pdf   -> 100 TAT pictures
"""
import io
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw, ImageFont
import fitz

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def extract_images_from_pdf(pdf_path: Path, min_size: int = 40) -> List[Image.Image]:
    images = []
    try:
        doc = fitz.open(pdf_path)
        seen = set()
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            for img_info in image_list:
                xref = img_info[0]
                if xref in seen:
                    continue
                seen.add(xref)
                try:
                    base = doc.extract_image(xref)
                    img = Image.open(io.BytesIO(base["image"])).convert("RGB")
                    if img.width >= min_size and img.height >= min_size:
                        images.append(img)
                except Exception:
                    continue
            if not image_list:
                try:
                    pix = page.get_pixmap(dpi=110)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    if img.width >= min_size and img.height >= min_size:
                        images.append(img)
                except Exception:
                    continue
        doc.close()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return images

def generate_placeholder(index: int, width=800, height=600, blank=False) -> Image.Image:
    if blank:
        img = Image.new("RGB", (width, height), (245, 245, 240))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
            small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        except Exception:
            font = ImageFont.load_default()
            small = font
        t = "BLANK SLIDE"
        bbox = draw.textbbox((0, 0), t, font=font)
        draw.text(((width - (bbox[2] - bbox[0])) // 2, height // 2 - 30), t, fill=(70, 70, 70), font=font)
        s = "Imagine any positive situation"
        bbox2 = draw.textbbox((0, 0), s, font=small)
        draw.text(((width - (bbox2[2] - bbox2[0])) // 2, height // 2 + 30), s, fill=(110, 110, 110), font=small)
        return img
    import random
    random.seed(index + 99)
    bg = random.choice([(88, 98, 68), (68, 78, 58), (105, 100, 80), (55, 65, 50), (95, 90, 75)])
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    for _ in range(random.randint(3, 7)):
        x = random.randint(40, width - 140)
        y = random.randint(40, height - 180)
        w = random.randint(35, 110)
        h = random.randint(70, 200)
        c = (max(0, min(255, bg[0] + random.randint(-35, 35))),
             max(0, min(255, bg[1] + random.randint(-35, 35))),
             max(0, min(255, bg[2] + random.randint(-35, 35))))
        draw.ellipse([x, y, x + w, y + h // 3], fill=c)
        draw.rectangle([x + w // 4, y + h // 4, x + 3 * w // 4, y + h], fill=c)
    horizon = random.randint(height // 2, int(height * 0.7))
    draw.rectangle([0, horizon, width, height], fill=(bg[0] - 18, bg[1] - 12, bg[2] - 8))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    draw.rectangle([8, 8, 160, 36], fill=(15, 25, 12))
    draw.text((16, 12), f"Practice #{index + 1}", fill=(190, 190, 140), font=font)
    return img

def load_ppdt_images() -> List[Image.Image]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    candidates = (list(DATA_DIR.glob("*ppdt*.pdf")) + list(DATA_DIR.glob("*PPDT*.pdf")) +
                  list(DATA_DIR.glob("ppdt.pdf")) + list(DATA_DIR.glob("PPDT.pdf")))
    images = []
    for pdf in candidates:
        images.extend(extract_images_from_pdf(pdf))
    if not images:
        images = [generate_placeholder(i) for i in range(100)]
    return images

def load_tat_images() -> List[Image.Image]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    candidates = (list(DATA_DIR.glob("*tat*.pdf")) + list(DATA_DIR.glob("*TAT*.pdf")) +
                  list(DATA_DIR.glob("tat.pdf")) + list(DATA_DIR.glob("TAT.pdf")))
    images = []
    for pdf in candidates:
        images.extend(extract_images_from_pdf(pdf))
    if not images:
        images = [generate_placeholder(i + 200) for i in range(100)]
    return images
