"""Download Blue Jays and Dodgers logos"""
import urllib.request
import os
from pathlib import Path

def download_logos():
    """Download team logos"""
    resources_dir = Path(__file__).parent.parent / "resources" / "images"
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Blue Jays logo URLs to try
    blue_jays_urls = [
        "https://logos-world.net/wp-content/uploads/2021/09/Toronto-Blue-Jays-Logo.png",
        "https://content.sportslogos.net/logos/54/53/full/2228_toronto_blue_jays-primary-2015.png"
    ]
    
    # Dodgers logo URLs to try
    dodgers_urls = [
        "https://logos-world.net/wp-content/uploads/2020/05/Los-Angeles-Dodgers-Logo.png",
        "https://content.sportslogos.net/logos/54/55/full/2997_los_angeles_dodgers-primary-2020.png"
    ]
    
    # Try to download Blue Jays logo
    blue_jays_path = resources_dir / "blue_jays_logo.png"
    if not blue_jays_path.exists():
        print("Attempting to download Blue Jays logo...")
        for url in blue_jays_urls:
            try:
                urllib.request.urlretrieve(url, blue_jays_path)
                print(f"✓ Downloaded Blue Jays logo from {url}")
                break
            except Exception as e:
                print(f"  Failed: {e}")
                continue
        if not blue_jays_path.exists():
            print("⚠️  Could not download Blue Jays logo automatically.")
            print(f"   Please manually add blue_jays_logo.png to {blue_jays_path}")
    
    # Try to download Dodgers logo
    dodgers_path = resources_dir / "dodgers_logo.png"
    if not dodgers_path.exists():
        print("Attempting to download Dodgers logo...")
        for url in dodgers_urls:
            try:
                urllib.request.urlretrieve(url, dodgers_path)
                print(f"✓ Downloaded Dodgers logo from {url}")
                break
            except Exception as e:
                print(f"  Failed: {e}")
                continue
        if not dodgers_path.exists():
            print("⚠️  Could not download Dodgers logo automatically.")
            print(f"   Please manually add dodgers_logo.png to {dodgers_path}")
    
    print("\nLogo download complete!")

if __name__ == "__main__":
    download_logos()

