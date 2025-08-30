import os
from pathlib import Path
from typing import List, Tuple

import cairosvg
from PIL import Image


WORKSPACE = Path('/workspace')
SVG_DIR = WORKSPACE / 'assets' / 'logo'
OUT_DIR = SVG_DIR / 'raster'


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def flatten_to_jpeg(png_path: Path, jpg_path: Path, quality: int = 92, background_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
    image = Image.open(png_path).convert('RGBA')
    background = Image.new('RGB', image.size, background_color)
    background.paste(image, mask=image.split()[3])
    background.save(jpg_path, 'JPEG', quality=quality, optimize=True, progressive=True)


def export_png(svg_path: Path, outputs: List[Tuple[int, int, str]]) -> List[Path]:
    generated_pngs: List[Path] = []
    for width, height, suffix in outputs:
        out_png = OUT_DIR / f"{svg_path.stem}-{suffix}.png"
        cairosvg.svg2png(url=str(svg_path), write_to=str(out_png), output_width=width if width else None, output_height=height if height else None)
        generated_pngs.append(out_png)
    return generated_pngs


def main() -> None:
    ensure_dirs()

    # Define export targets: (width, height, suffix)
    horizontal_svg = SVG_DIR / 'gameswam-logo-horizontal.svg'
    stacked_svg = SVG_DIR / 'gameswam-logo-stacked.svg'
    icon_svg = SVG_DIR / 'gameswam-logo-icon.svg'

    # Horizontal exports (width-driven)
    horiz_targets = [
        (2048, 0, 'horizontal-2048w'),
        (1024, 0, 'horizontal-1024w'),
        (512, 0, 'horizontal-512w'),
    ]

    # Stacked exports (square-ish; width-driven)
    stacked_targets = [
        (2048, 0, 'stacked-2048'),
        (1024, 0, 'stacked-1024'),
        (512, 0, 'stacked-512'),
    ]

    # Icon exports
    icon_targets = [
        (1024, 0, 'icon-1024'),
        (512, 0, 'icon-512'),
        (256, 0, 'icon-256'),
    ]

    generated: List[Path] = []
    generated += export_png(horizontal_svg, horiz_targets)
    generated += export_png(stacked_svg, stacked_targets)
    generated += export_png(icon_svg, icon_targets)

    # Convert to JPG with white background
    for png_path in generated:
        jpg_path = png_path.with_suffix('.jpg')
        flatten_to_jpeg(png_path, jpg_path)

    print('Export complete. Files in:', OUT_DIR)


if __name__ == '__main__':
    main()

