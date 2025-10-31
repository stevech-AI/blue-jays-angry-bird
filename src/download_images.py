"""Script to download Blue Jays logo and Dodgers player images"""
import urllib.request
import os
from pathlib import Path

# Player lists
BLUE_JAYS_PLAYERS = [
    "Vladimir Guerrero Jr.",
    "Bo Bichette", 
    "George Springer",
    "Kevin Gausman",
    "Alejandro Kirk",
    "Danny Jansen",
    "Cavan Biggio",
    "Davis Schneider"
]

DODGERS_PLAYERS = [
    "Mookie Betts",
    "Freddie Freeman",
    "Shohei Ohtani",
    "Will Smith",
    "Max Muncy",
    "Teoscar Hernández",
    "Gavin Lux",
    "James Outman"
]

def create_placeholder_image(path, size=(50, 50), color=(100, 150, 200), text=""):
    """Create a simple placeholder image"""
    try:
        import pygame
        pygame.init()
        surface = pygame.Surface(size)
        surface.fill(color)
        if text:
            font = pygame.font.Font(None, 24)
            text_surface = font.render(text[:2], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
            surface.blit(text_surface, text_rect)
        pygame.image.save(surface, path)
        return True
    except Exception as e:
        print(f"Error creating placeholder: {e}")
        return False

def download_images():
    """Download or create placeholder images"""
    resources_dir = Path(__file__).parent.parent / "resources" / "images"
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Blue Jays logo - check if it exists, if not provide instructions
    blue_jays_logo_path = resources_dir / "blue_jays_logo.png"
    if not blue_jays_logo_path.exists():
        print(f"\n⚠️  IMPORTANT: Blue Jays logo not found!")
        print(f"Please add the Blue Jays logo image to: {blue_jays_logo_path}")
        print(f"The game will use the red bird as fallback until the logo is added.\n")
    
    # Create placeholder Dodgers player images
    dodgers_dir = resources_dir / "dodgers_players"
    dodgers_dir.mkdir(exist_ok=True)
    
    for i, player in enumerate(DODGERS_PLAYERS):
        player_file = dodgers_dir / f"dodgers_{i}.png"
        if not player_file.exists():
            # Create a placeholder with player initials
            initials = ''.join([name[0] for name in player.split()[:2]])
            create_placeholder_image(str(player_file), size=(30, 30), 
                                   color=(0, 90, 156), text=initials)
            print(f"Created placeholder for {player}")
    
    print("Image setup complete!")

if __name__ == "__main__":
    download_images()

