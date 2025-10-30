#!/usr/bin/env python3
"""
Selene Download Manager
Downloads all required files for LineageOS installation on Redmi Note 10 2022 (selene)
"""

import os
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

# Download links
DOWNLOADS = {
    'twrp': {
        'name': 'TWRP Recovery',
        'url': 'https://drive.google.com/uc?export=download&id=17ebo3DD077HihnncSpQ6X0beChycxJRu',
        'filename': 'twrp-selene.img'
    },
    'firmware_12': {
        'name': 'Stock Firmware 12.5',
        'url': 'https://bigota.d.miui.com/V12.5.20.0.RKUMIXM/miui_SELENEGlobal_V12.5.20.0.RKUMIXM_37f0d4aaa7_11.0.zip',
        'filename': 'selene_12.5.20.zip'
    },
    'firmware_14': {
        'name': 'Stock Firmware 14',
        'url': 'https://bigota.d.miui.com/V14.0.7.0.TKUMIXM/selene_global_images_V14.0.7.0.TKUMIXM_20240517.0000.00_13.0_global_63a8c6a62f.tgz',
        'filename': 'selene_14.0.7.tgz'
    },
    'mtkclient': {
        'name': 'MTKClient',
        'url': 'https://github.com/bkerler/mtkclient/archive/refs/heads/main.zip',
        'filename': 'mtkclient-main.zip'
    },
    'payload_dumper': {
        'name': 'Payload Dumper',
        'url': 'https://github.com/vm03/payload_dumper/archive/refs/heads/master.zip',
        'filename': 'payload_dumper-master.zip'
    },
    'adb': {
        'name': 'ADB Platform Tools',
        'url': 'https://dl.google.com/android/repository/platform-tools-latest-linux.zip',
        'filename': 'platform-tools-latest-linux.zip'
    },
    'magisk': {
        'name': 'Magisk',
        'url': 'https://github.com/topjohnwu/Magisk/releases/download/v27.0/Magisk-v27.0.apk',
        'filename': 'magisk27.apk'
    },
    'abootloop': {
        'name': 'Anti-Bootloop',
        'url': 'https://github.com/Mishu-bepo/abootloop/releases/download/1.0/abootloop-1.0.zip',
        'filename': 'abootloop.zip'
    }
}

CUSTOM_ROM_SOURCEFORGE = 'https://sourceforge.net/projects/hasan6034-builds/files/selene/'

class DownloadProgress:
    """Progress bar for downloads"""
    def __init__(self, filename):
        self.filename = filename
        self.start_time = time.time()
        self.last_update = 0
        
    def __call__(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        
        # Update every 0.5 seconds
        current_time = time.time()
        if current_time - self.last_update < 0.5 and downloaded < total_size:
            return
        self.last_update = current_time
        
        if total_size > 0:
            percent = min(downloaded * 100 / total_size, 100)
            speed = downloaded / (current_time - self.start_time + 0.001) / 1024 / 1024  # MB/s
            
            # Calculate remaining
            if speed > 0:
                remaining = (total_size - downloaded) / (speed * 1024 * 1024)
                mins, secs = divmod(int(remaining), 60)
                time_str = f"{mins:02d}:{secs:02d}"
            else:
                time_str = "??:??"
            
            # Progress bar
            bar_length = 40
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f'\r{self.filename}: [{bar}] {percent:.1f}% | {speed:.2f} MB/s | {time_str} remaining', 
                  end='', flush=True)
        else:
            print(f'\rDownloading {self.filename}...', end='', flush=True)

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Print header"""
    clear_screen()
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 14 + "SELENE DOWNLOAD MANAGER" + " " * 13 + "║")
    print("╚" + "═" * 50 + "╝")
    print()

def print_menu(current_dir):
    """Print download menu"""
    print(f"Current directory: {current_dir}")
    print()
    print("─" * 52)
    print("       Choose download:")
    print("─" * 52)
    print(" 1. TWRP Recovery")
    print(" 2. Stock Firmware 12.5")
    print(" 3. Stock Firmware 14")
    print(" 4. Custom ROMs (external link)")
    print(" 5. MTKClient")
    print(" 6. Payload Dumper")
    print(" 7. ADB Platform Tools")
    print(" 8. Magisk and Anti-Bootloop")
    print(" 9. :::ALL::: (except Custom ROM)")
    print()
    print("00. Change directory")
    print(" 0. Exit")
    print("─" * 52)

def download_file(url, filename, download_dir):
    """Download a file with progress bar"""
    filepath = os.path.join(download_dir, filename)
    
    try:
        print(f"\nDownloading {filename}...")
        print(f"Destination: {filepath}")
        
        # Create directory if doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Download with progress
        urllib.request.urlretrieve(url, filepath, DownloadProgress(filename))
        print(f"\n✓ {filename} downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error downloading {filename}: {e}")
        return False

def download_item(key, download_dir):
    """Download single item"""
    item = DOWNLOADS[key]
    print(f"\n{item['name']} will be downloaded to {download_dir}")
    confirm = input("Is this okay? (y/n): ").lower()
    
    if confirm == 'y':
        return download_file(item['url'], item['filename'], download_dir)
    return False

def download_custom_rom(download_dir):
    """Handle custom ROM download from SourceForge"""
    print(f"\nOpening SourceForge in browser: {CUSTOM_ROM_SOURCEFORGE}")
    webbrowser.open(CUSTOM_ROM_SOURCEFORGE)
    
    print("\nPlease copy the download link from SourceForge and paste here:")
    url = input("Download link: ").strip()
    
    if not url:
        print("No link provided. Cancelled.")
        return False
    
    # Extract filename from URL or ask user
    filename = input("Enter filename (e.g., lineage-20-selene.zip): ").strip()
    if not filename:
        filename = "custom_rom.zip"
    
    print(f"\nCustom ROM will be downloaded to {download_dir}")
    confirm = input("Is this okay? (y/n): ").lower()
    
    if confirm == 'y':
        return download_file(url, filename, download_dir)
    return False

def download_magisk_group(download_dir):
    """Download Magisk and Anti-Bootloop"""
    print("\nDownloading Magisk and Anti-Bootloop...")
    print(f"Destination: {download_dir}")
    confirm = input("Is this okay? (y/n): ").lower()
    
    if confirm != 'y':
        return False
    
    success = True
    success &= download_file(DOWNLOADS['magisk']['url'], 
                             DOWNLOADS['magisk']['filename'], 
                             download_dir)
    success &= download_file(DOWNLOADS['abootloop']['url'], 
                             DOWNLOADS['abootloop']['filename'], 
                             download_dir)
    return success

def download_all(download_dir):
    """Download all files except custom ROM"""
    print("\n" + "="*52)
    print("ALL WILL BE DOWNLOADED (EXCEPT CUSTOM ROM)!")
    print("="*52)
    print("\nThis includes:")
    print("  • TWRP Recovery")
    print("  • Stock Firmware 12.5")
    print("  • Stock Firmware 14")
    print("  • MTKClient")
    print("  • Payload Dumper")
    print("  • ADB Platform Tools")
    print("  • Magisk")
    print("  • Anti-Bootloop")
    print()
    print(f"Destination: {download_dir}")
    confirm = input("\nIs this okay? (y/n): ").lower()
    
    if confirm != 'y':
        return
    
    # Download all items
    items_to_download = ['twrp', 'firmware_12', 'firmware_14', 'mtkclient', 
                        'payload_dumper', 'adb', 'magisk', 'abootloop']
    
    total = len(items_to_download)
    for i, key in enumerate(items_to_download, 1):
        item = DOWNLOADS[key]
        print(f"\n[{i}/{total}] Downloading {item['name']}...")
        download_file(item['url'], item['filename'], download_dir)
    
    print("\n" + "="*52)
    print("ALL DOWNLOADS COMPLETED!")
    print("="*52)
    input("\nPress Enter to continue...")

def change_directory(current_dir):
    """Change download directory"""
    print(f"\nCurrent directory: {current_dir}")
    new_dir = input("Please paste new directory here: ").strip()
    
    if not new_dir:
        return current_dir
    
    # Expand home directory
    new_dir = os.path.expanduser(new_dir)
    
    # Create if doesn't exist
    try:
        os.makedirs(new_dir, exist_ok=True)
        print(f"Changed directory from '{current_dir}' to '{new_dir}'")
        print("All files will be downloaded to this folder")
        input("\nPress Enter to continue...")
        return new_dir
    except Exception as e:
        print(f"Error creating directory: {e}")
        input("\nPress Enter to continue...")
        return current_dir

def main():
    """Main function"""
    # Default directory
    download_dir = os.path.join(str(Path.home()), 'redmi-selene')
    
    while True:
        print_header()
        print_menu(download_dir)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '0':
            print("\nExiting... Goodbye!")
            sys.exit(0)
            
        elif choice == '00':
            download_dir = change_directory(download_dir)
            
        elif choice == '1':
            download_item('twrp', download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            download_item('firmware_12', download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            download_item('firmware_14', download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            download_custom_rom(download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            download_item('mtkclient', download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '6':
            download_item('payload_dumper', download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '7':
            download_item('adb', download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '8':
            download_magisk_group(download_dir)
            input("\nPress Enter to continue...")
            
        elif choice == '9':
            download_all(download_dir)
            
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
