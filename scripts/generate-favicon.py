"""Export browser icon sizes from the generated favicon-source.png using Pillow."""

from pathlib import Path
from PIL import Image

public_directory = Path(__file__).resolve().parents[1] / 'public'
image = Image.open(public_directory / 'favicon-source.png').convert('RGB')
image.resize((180, 180), Image.Resampling.LANCZOS).save(public_directory / 'apple-touch-icon.png')
image.resize((192, 192), Image.Resampling.LANCZOS).save(public_directory / 'favicon.png')
image.save(public_directory / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
