#!/usr/bin/env python3
"""
Process app assets (splash screen and icon) for iOS and Android.

This script:
1. Checks for assets/splash.png and assets/icon.png
2. Generates iOS LaunchScreen with centered image on background color
3. Generates Android splash drawable and theme
4. Copies/resizes icon for Tauri icon generation
"""

import json
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_DIR = PROJECT_ROOT / "config"
SRC_TAURI_DIR = PROJECT_ROOT / "src-tauri"


def load_config() -> dict:
    with open(CONFIG_DIR / "app.json", "r") as f:
        return json.load(f)


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def hex_to_ios_rgb(hex_color: str) -> dict:
    """Convert hex to iOS color components (0-1 range)."""
    r, g, b = hex_to_rgb(hex_color)
    return {"red": r / 255.0, "green": g / 255.0, "blue": b / 255.0}


def process_splash_ios(splash_path: Path, bg_color: str):
    """Generate iOS LaunchScreen.storyboard with centered splash image."""
    print("Processing splash for iOS...")

    # Copy splash image to iOS assets
    ios_assets_dir = SRC_TAURI_DIR / "gen" / "apple" / "Assets.xcassets" / "SplashImage.imageset"
    ios_assets_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(splash_path, ios_assets_dir / "splash.png")

    # Create Contents.json for the image set
    contents = {
        "images": [
            {"filename": "splash.png", "idiom": "universal", "scale": "1x"},
            {"idiom": "universal", "scale": "2x"},
            {"idiom": "universal", "scale": "3x"}
        ],
        "info": {"author": "xcode", "version": 1}
    }
    with open(ios_assets_dir / "Contents.json", "w") as f:
        json.dump(contents, f, indent=2)

    # Generate LaunchScreen.storyboard with image view centered
    rgb = hex_to_ios_rgb(bg_color)
    storyboard = '''<?xml version="1.0" encoding="UTF-8"?>
<document type="com.apple.InterfaceBuilder3.CocoaTouch.Storyboard.XIB" version="3.0" toolsVersion="17150" targetRuntime="iOS.CocoaTouch" propertyAccessControl="none" useAutolayout="YES" useTraitCollections="YES" useSafeAreas="YES" colorMatched="YES" initialViewController="Y6W-OH-hqX">
    <dependencies>
        <plugIn identifier="com.apple.InterfaceBuilder.IBCocoaTouchPlugin" version="17122"/>
        <capability name="Safe area layout guides" minToolsVersion="9.0"/>
        <capability name="documents saved in the Xcode 8 format" minToolsVersion="8.0"/>
    </dependencies>
    <scenes>
        <scene sceneID="s0d-6b-0kx">
            <objects>
                <viewController id="Y6W-OH-hqX" sceneMemberID="viewController">
                    <view key="view" contentMode="scaleToFill" id="5EZ-qb-Rvc">
                        <rect key="frame" x="0.0" y="0.0" width="414" height="896"/>
                        <autoresizingMask key="autoresizingMask" widthSizable="YES" heightSizable="YES"/>
                        <subviews>
                            <imageView clipsSubviews="YES" userInteractionEnabled="NO" contentMode="scaleAspectFit" image="splash" translatesAutoresizingMaskIntoConstraints="NO" id="img-splash">
                                <rect key="frame" x="107" y="348" width="200" height="200"/>
                                <constraints>
                                    <constraint firstAttribute="width" constant="200" id="w-splash"/>
                                    <constraint firstAttribute="height" constant="200" id="h-splash"/>
                                </constraints>
                            </imageView>
                        </subviews>
                        <viewLayoutGuide key="safeArea" id="vDu-zF-Fre"/>
                        <color key="backgroundColor" red="{r}" green="{g}" blue="{b}" alpha="1" colorSpace="custom" customColorSpace="sRGB"/>
                        <constraints>
                            <constraint firstItem="img-splash" firstAttribute="centerX" secondItem="5EZ-qb-Rvc" secondAttribute="centerX" id="cx-splash"/>
                            <constraint firstItem="img-splash" firstAttribute="centerY" secondItem="5EZ-qb-Rvc" secondAttribute="centerY" id="cy-splash"/>
                        </constraints>
                    </view>
                </viewController>
                <placeholder placeholderIdentifier="IBFirstResponder" id="Ief-a0-LHa" userLabel="First Responder" customClass="UIResponder" sceneMemberID="firstResponder"/>
            </objects>
        </scene>
    </scenes>
    <resources>
        <image name="splash" width="200" height="200"/>
    </resources>
</document>'''

    storyboard = storyboard.replace("{r}", f"{rgb['red']:.6f}")
    storyboard = storyboard.replace("{g}", f"{rgb['green']:.6f}")
    storyboard = storyboard.replace("{b}", f"{rgb['blue']:.6f}")

    storyboard_path = SRC_TAURI_DIR / "gen" / "apple" / "LaunchScreen.storyboard"
    storyboard_path.parent.mkdir(parents=True, exist_ok=True)
    storyboard_path.write_text(storyboard, encoding="utf-8")
    print(f"  iOS LaunchScreen.storyboard: {storyboard_path}")
    print(f"  iOS SplashImage asset: {ios_assets_dir}")


def process_splash_android(splash_path: Path, bg_color: str):
    """Generate Android splash theme and drawable."""
    print("Processing splash for Android...")

    res_dir = SRC_TAURI_DIR / "gen" / "android" / "app" / "src" / "main" / "res"

    # Copy splash image to drawable
    drawable_dir = res_dir / "drawable"
    drawable_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(splash_path, drawable_dir / "splash.png")

    # If Pillow available, create different density versions
    if Image:
        densities = {
            "drawable-mdpi": 128,
            "drawable-hdpi": 192,
            "drawable-xhdpi": 256,
            "drawable-xxhdpi": 384,
            "drawable-xxxhdpi": 512,
        }
        img = Image.open(splash_path)
        for folder, size in densities.items():
            density_dir = res_dir / folder
            density_dir.mkdir(parents=True, exist_ok=True)
            resized = img.resize((size, size), Image.LANCZOS)
            resized.save(density_dir / "splash.png")

    # Create values directory
    values_dir = res_dir / "values"
    values_dir.mkdir(parents=True, exist_ok=True)

    # Update themes.xml with splash background
    themes_content = '''<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.webview_wrapper_tauri" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="android:windowBackground">@drawable/splash_background</item>
    </style>
</resources>
'''
    (values_dir / "themes.xml").write_text(themes_content, encoding="utf-8")

    # Create splash_background drawable XML (centered image on color)
    splash_bg = '''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/splash_background_color"/>
    <item android:gravity="center" android:width="200dp" android:height="200dp">
        <bitmap android:src="@drawable/splash" android:gravity="center"/>
    </item>
</layer-list>
'''
    (drawable_dir / "splash_background.xml").write_text(splash_bg, encoding="utf-8")

    # Add color resource
    colors_content = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="splash_background_color">{bg_color}</color>
</resources>
'''
    (values_dir / "colors.xml").write_text(colors_content, encoding="utf-8")

    print(f"  Android splash drawable: {drawable_dir / 'splash.png'}")
    print(f"  Android splash_background.xml: {drawable_dir / 'splash_background.xml'}")
    print(f"  Android themes.xml updated")


def process_icon(icon_path: Path):
    """Copy icon to src-tauri/icons/ for Tauri's icon generation."""
    print("Processing app icon...")

    icons_dir = SRC_TAURI_DIR / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)

    # Copy as the source icon
    shutil.copy2(icon_path, icons_dir / "icon.png")

    # If Pillow is available, generate required sizes
    if Image:
        img = Image.open(icon_path)

        sizes = {
            "32x32.png": 32,
            "128x128.png": 128,
            "128x128@2x.png": 256,
        }

        for name, size in sizes.items():
            resized = img.resize((size, size), Image.LANCZOS)
            resized.save(icons_dir / name)

        # Generate .ico (Windows - not needed for mobile but keeps Tauri happy)
        ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        ico_images = [img.resize(s, Image.LANCZOS) for s in ico_sizes]
        ico_images[0].save(icons_dir / "icon.ico", format="ICO", sizes=ico_sizes)

        # Generate .icns placeholder (macOS - just copy largest)
        img.resize((512, 512), Image.LANCZOS).save(icons_dir / "icon.icns", format="PNG")

        print(f"  Generated icon sizes in {icons_dir}")
    else:
        print("  WARNING: Pillow not installed, icon resizing skipped")
        print("  Install with: pip install Pillow")

    print(f"  Icon source: {icons_dir / 'icon.png'}")


def main():
    config = load_config()
    splash_bg = config.get("splashBackgroundColor", "#ffffff")

    splash_path = ASSETS_DIR / "splash.png"
    icon_path = ASSETS_DIR / "icon.png"

    if splash_path.exists():
        process_splash_ios(splash_path, splash_bg)
        process_splash_android(splash_path, splash_bg)
    else:
        print(f"No splash image found at {splash_path}, skipping splash generation")

    if icon_path.exists():
        process_icon(icon_path)
    else:
        print(f"No icon found at {icon_path}, skipping icon generation")

    if not splash_path.exists() and not icon_path.exists():
        print("No assets to process. Place images in assets/ folder.")


if __name__ == "__main__":
    main()
