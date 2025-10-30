# LineageOS 20 Installation Guide for Redmi Note 10 2022 (selene) - Linux Only

[![Device](https://img.shields.io/badge/Device-Redmi%20Note%2010%202022-orange)](https://www.gsmarena.com/xiaomi_redmi_note_10_2022-11371.php)
[![SoC](https://img.shields.io/badge/SoC-MediaTek%20Helio%20G88-blue)](https://www.mediatek.com/products/smartphones/mediatek-helio-g88)
[![OS](https://img.shields.io/badge/OS-LineageOS%2020-green)](https://lineageos.org/)
[![Linux](https://img.shields.io/badge/Platform-Linux%20Only-red)](https://fedoraproject.org/)
[![Root](https://img.shields.io/badge/Root-Magisk%20v27-purple)](https://github.com/topjohnwu/Magisk)

> Complete guide to install LineageOS 20 with root on Redmi Note 10 2022 (selene) using only Linux.  
> No Windows required. No 7-day waiting period. No hassle.

---

## ⚠️ DISCLAIMER

**READ THIS BEFORE PROCEEDING:**

- **ALL DATA WILL BE LOST** - Make complete backups before starting
- **WARRANTY WILL BE VOIDED** - Unlocking bootloader voids manufacturer warranty
- **RISK OF BRICKING** - Incorrect procedures may render device unusable
- **BATTERY REQUIREMENT** - Keep device charged above 70% throughout process
- **CABLE QUALITY** - Use original or high-quality USB cable (critical for MediaTek devices)
- **LINUX ONLY** - This guide is exclusively for Linux systems (Fedora/Ubuntu/Arch)
- **TERMINAL KNOWLEDGE** - Basic command-line proficiency required

**THE AUTHOR IS NOT RESPONSIBLE FOR:**
- Bricked devices
- Data loss
- Hardware damage
- Missed alarms
- Thermonuclear War
- A rupture of the space–time continuum causing a black hole to form in front of you and hurl an atomic bomb.
- Any other consequences resulting from following this guide

**YOU PROCEED AT YOUR OWN RISK.**

By continuing, you acknowledge that you understand and accept these risks.

---

## 📋 Table of Contents

- [Device Specifications](#-device-specifications)
- [Requirements](#-requirements)
- [Tools Used](#-tools-used)
- [Project Structure](#-project-structure)
- [Part 1: Unlock Bootloader](#-part-1-unlock-bootloader)
- [Part 2: Install Custom Recovery](#-part-2-install-custom-recovery)
- [Part 3: Install LineageOS](#-part-3-install-lineageos)
- [Part 4: Root with Magisk](#-part-4-root-with-magisk)
- [Troubleshooting](#-troubleshooting)
- [Downloads](#-downloads)
- [Credits](#-credits)

---

## 📱 Device Specifications

| Feature | Detail |
|---------|--------|
| **Model** | Redmi Note 10 2022 (2112119XX) |
| **Codename** | selene |
| **SoC** | MediaTek Helio G88 (MT6768) |
| **RAM** | 4GB / 6GB |
| **Storage** | 64GB / 128GB |
| **Architecture** | ARM64, A/B Partitions |
| **Stock Android** | MIUI 12.5 - 14 (Android 11-13) |

---

## 💻 Requirements

### Hardware
- PC running Linux (i used Fedora 42)
- 1GB RAM or more
- 16GB free storage space or more
- Functional USB port

### Software Base
```bash
# Fedora/RHEL
sudo dnf install android-tools git python3 python3-pip unzip wget

# Ubuntu/Debian
sudo apt install android-tools-adb android-tools-fastboot git python3 python3-pip unzip wget

# Arch Linux
sudo pacman -S android-tools git python python-pip unzip wget

# Others
sudo [packageManager] [installCommand] android-tools git python python-pip unzip wget
```

### Python Dependencies
```bash
pip3 install brotli protobuf pyusb pyserial capstone keystone-engine
```

---

## 🛠️ Tools Used

| Tool | Version | Purpose | Link |
|------|---------|---------|------|
| **mtkclient** | Latest | Bootloader unlock + Unbrick | [GitHub](https://github.com/bkerler/mtkclient) |
| **TWRP** | 3.7.x | Custom Recovery | [Google Drive](https://drive.google.com/file/d/17ebo3DD077HihnncSpQ6X0beChycxJRu/view?usp=sharing) |
| **LineageOS** | 20.0 (Android 13) | Custom ROM | [SourceForge](https://sourceforge.net/projects/hasan6034-builds/files/selene/) |
| **Magisk** | v27.0 | Systemless root | [GitHub](https://github.com/topjohnwu/Magisk) |
| **ABootLoop** | Latest | Anti-bootloop fix | [MMRL](https://mmrl.dev/repository/mishubepo/abootloop) |
| **payload_dumper** | Latest | Extract ROM images | [GitHub](https://github.com/vm03/payload_dumper) |
| **ADB/Fastboot** | Latest | Android Debug Bridge | [Android Developers](https://developer.android.com/tools/releases/platform-tools) |

---

## 📦 Project Structure (Recommended)

```
redmi-selene/
├── lineageImages/          # Extracted LineageOS images
│   ├── boot.img           # Kernel + ramdisk
│   ├── dtbo.img           # Device Tree Overlay
│   ├── product.img        # Product partition
│   ├── system.img         # Base system
│   ├── vbmeta*.img        # Boot verification
│   └── vendor.img         # Drivers and binaries
├── recoverys/             # Custom recoveries
│   ├── twrp-selene.img   # TWRP (bootable)
│   └── selene_12_5_20_recovery.zip  # MIUI base recovery
├── root/                  # Root files
│   ├── magisk27.apk      # Magisk Manager
│   ├── magisk.zip        # Magisk flashable
│   └── abootloop.zip     # Bootloop fix (emergency)
├── selene_12.5.20/        # Stock MIUI ROM (unbrick)
│   └── images/           # All stock partitions
├── payload_dumper/        # Extraction tool
├── lineage_selene.zip     # Complete LineageOS ROM
└── *.tgz                  # Compressed stock ROMs
```

---

## 🔓 Part 1: Unlock Bootloader

### Why mtkclient?

Xiaomi's official unlock tool requires a **7-day waiting period** and **Windows only**. mtkclient unlocks instantly on Linux.

### Install mtkclient

```bash
# Clone repository
git clone https://github.com/bkerler/mtkclient.git
cd mtkclient

# Install dependencies
pip3 install -r requirements.txt

# Configure udev rules
sudo cp Setup/Linux/*.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

### Prepare Device

1. **Enable Developer Options:**
   - Settings > About phone
   - Tap "MIUI Version" 7 times

2. **Enable USB Debugging:**
   - Settings > Additional settings > Developer options
   - Enable "USB debugging"
   - Enable "OEM unlocking"

### Unlock Process

```bash
cd mtkclient

# Run GUI (easier)
python3 mtk_gui

# Or CLI
python3 mtk e metadata,userdata,md_udc

# When prompted:
# 1. POWER OFF the phone
# 2. Hold Vol+ and/or Vol- while connecting USB
# 3. mtkclient will detect device
# 4. Click "Unlock Bootloader"
# 5. Wait for "Done"
```

**Verify unlock:**
```bash
adb reboot bootloader
fastboot getvar unlocked
# Should show: unlocked: yes
```

---

## 🔧 Part 2: Install Custom Recovery

### ⚠️ IMPORTANT: A/B Partitions

Redmi Note 10 2022 uses A/B partitions (dual boot):
- `boot` doesn't exist, there's `boot_a` and `boot_b`
- Recovery is integrated into boot
- Must flash to **both slots**

### Flash TWRP

```bash
cd ~/redmi-selene

# Download TWRP (see Downloads section)
# Place in: recoverys/twrp-selene.img

# Flash with mtkclient
cd ~/mtkclient

# POWER OFF phone, disconnect USB
python3 mtk w boot_a ~/redmi-selene/recoverys/twrp-selene.img
# CONNECT USB when prompted

# Repeat for boot_b
python3 mtk w boot_b ~/redmi-selene/recoverys/twrp-selene.img
```

### Boot into TWRP
```bash
# Hold: Vol+ and Power until TWRP appears
```

### Make TWRP Permanent

```bash
# In TWRP:
# Advanced > Flash Current TWRP
# Swipe to confirm
```

---

## 📱 Part 3: Install LineageOS

### Preparation

**Extract images (optional, for backup/Magisk):**

```bash
cd ~/redmi-selene

# Extract payload.bin
unzip lineage_selene.zip payload.bin

# Use payload_dumper
cd payload_dumper
python3 payload_dumper.py ../payload.bin --images boot

# Images in: output/
cp output/*.img ../lineageImages/
```

### Clean Installation

**Step 1: Complete Wipe**

```bash
# Boot into TWRP
adb reboot recovery

# In recovery:
# Wipe > Format Data
# Type: yes

# Wipe > Advanced Wipe
# Select: Dalvik, Cache, System, Data
# Swipe to wipe
```

**Step 2: Flash LineageOS**

```bash
# Method A: ADB Sideload (recommended)
# In TWRP: Advanced > ADB Sideload

adb sideload ~/redmi-selene/lineage_selene.zip

# Method B: Install from storage
adb push ~/redmi-selene/lineage_selene.zip /sdcard/
# TWRP > Install > lineage_selene.zip
```

**Step 3: Clear cache and reboot**

```bash
# In TWRP:
# Wipe > Advanced Wipe > Dalvik + Cache
# Reboot > System

# First boot: 10-20 minutes ☕
```

---

## 🔓 Part 4: Root with Magisk

### ⚠️ CORRECT Method (avoids bootloops)

**DO NOT flash Magisk.zip from recovery** - this causes bootloops on LineageOS.

**Correct method: Patch boot.img**

### Step 1: Extract clean boot.img

```bash
cd ~/redmi-selene/lineageImages

# Should already be extracted in Part 3
# If not:
cd ~/redmi-selene/payload_dumper
python3 payload_dumper.py ../payload.bin --images boot
cp output/boot.img ../lineageImages/
```

### Step 2: Install Magisk APK

```bash
cd ~/redmi-selene/root

# Download if you don't have it
wget https://github.com/topjohnwu/Magisk/releases/download/v27.0/Magisk-v27.0.apk -O magisk27.apk

# Install on phone
adb install magisk27.apk
```

### Step 3: Patch boot.img

```bash
# Copy boot.img to phone
adb push ~/redmi-selene/lineageImages/boot.img /sdcard/Download/

# On the phone:
# 1. Open Magisk app
# 2. Tap "Install" (next to Magisk)
# 3. "Select and Patch a File"
# 4. Navigate to /sdcard/Download/boot.img
# 5. Tap "Let's Go"
# 6. Wait for "All done!"

# Copy patched boot to PC
adb pull /sdcard/Download/magisk_patched_*.img ~/redmi-selene/root/
```

### Step 4: Flash patched boot

**Option A: With fastboot**
```bash
cd ~/redmi-selene/root

adb reboot bootloader

fastboot flash boot_a magisk_patched_*.img
fastboot flash boot_b magisk_patched_*.img
fastboot reboot
```

**Option B: With mtkclient**
```bash
cd ~/mtkclient

# POWER OFF phone
python3 mtk w boot_a ~/redmi-selene/root/magisk_patched_*.img
# Repeat for boot_b
python3 mtk w boot_b ~/redmi-selene/root/magisk_patched_*.img
```

### Step 5: Verify Root

```bash
# After boot:
adb shell su
```

### Optional: Install Anti-Bootloop

```bash
# In case of future bootloop issues
# Flash abootloop.zip from TWRP:
adb push ~/redmi-selene/root/abootloop.zip /sdcard/
# TWRP > Install > abootloop.zip
```

---

## 🆘 Troubleshooting

### Bootloop after flashing Magisk

**Symptom:** Phone constantly reboots or goes to fastboot.

**Solution:**
```bash
# Restore clean boot
cd ~/mtkclient
python3 mtk w boot_a ~/redmi-selene/lineageImages/boot.img
python3 mtk w boot_b ~/redmi-selene/lineageImages/boot.img

# Reboot normally
# Then follow Part 4 correctly (patch boot, don't flash zip)
```

### Error: "partition boot doesn't exist"

**Cause:** A/B device, use `boot_a` and `boot_b`.

**Solution:**
```bash
# Use boot_a and boot_b instead of boot
fastboot flash boot_a file.img
fastboot flash boot_b file.img
```

### TWRP asks for PIN and doesn't accept it

**Symptoms:** Recovery asks for password to decrypt /data.

**Solutions:**
1. Enter lock screen PIN/pattern (1% chance it works)
2. If it fails: `Wipe > Format Data > yes` (erases everything)
3. Dont do anything, just press "cancel".
### LineageOS Recovery instead of TWRP

**Cause:** LineageOS overwrote custom recovery.

**Solution:**
```bash
# Reflash TWRP
cd ~/mtkclient
python3 mtk w boot_a ~/redmi-selene/recoverys/twrp-selene.img
python3 mtk w boot_b ~/redmi-selene/recoverys/twrp-selene.img

# On TWRP:
1. Flash boot.img from lineage os extracted with payload_dumper
2. Select Install TWRP to ramdisk option
3. Reboot System!
```

### Errors "dm-verity" or "unable to unlock"

**Symptoms:** Error messages about dm-1, verification failed.

**Explanation:** /data is encrypted, this is normal.

**Solution:**
- **Ignore:** Doesn't affect flashing from /sdcard/
- **Remove encryption:** `Wipe > Format Data > yes`

### Hard Brick (won't turn on, no fastboot)

**Solution:** Flash complete stock ROM

```bash
cd ~/redmi-selene/selene_12.5.20

# Use mtkclient with stock ROM:
cd ~/mtkclient
python3 mtk wl ~/redmi-selene/selene_12.5.20/images/

# This restores EVERYTHING to stock
```

### Fastboot commands for emergency flash

```bash
# Flash vbmeta (disable verification)
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img

# Flash TWRP temporarily
fastboot flash boot path/to/TWRP.img
fastboot reboot recovery
```

---

## 📥 Downloads

### Required Files

| Item | Link | Notes |
|------|------|-------|
| **TWRP Recovery** | [Google Drive](https://drive.google.com/file/d/17ebo3DD077HihnncSpQ6X0beChycxJRu/view?usp=sharing) | Custom recovery for selene |
| **LineageOS ROMs** | [SourceForge](https://sourceforge.net/projects/hasan6034-builds/files/selene/) | By hasan6034 |
| **Stock Firmware 12.5** | [XM Firmware Updater](https://xmfirmwareupdater.com/miui/selene/stable/V12.5.20.0.RKUMIXM/) | For unbrick/downgrade |
| **Stock Firmware 14** | [XM Firmware Updater](https://xmfirmwareupdater.com/firmware/selene/stable/V14.0.7.0.TKUMIXM/) | Latest stock |
| **mtkclient** | [GitHub](https://github.com/bkerler/mtkclient) | Bootloader unlock tool |
| **payload_dumper** | [GitHub](https://github.com/vm03/payload_dumper) | Extract ROM images |
| **ADB/Fastboot** | [Android Developers](https://developer.android.com/tools/releases/platform-tools) | Platform tools |
| **Magisk** | [GitHub](https://github.com/topjohnwu/Magisk) | Root solution |
| **ABootLoop** | [MMRL](https://mmrl.dev/repository/mishubepo/abootloop) | Anti-bootloop fix |

**Note:** LineageOS includes GApps (Google Apps).

### Support Resources

| Resource | Link |
|----------|------|
| **Telegram Community** | [Redmi 10 Community](https://t.me/Redmi10_Community) |
| **XDA Forums** | [selene tag](https://xdaforums.com/tags/selene/) |
| **Video Tutorial** | [YouTube (Raycast)](https://youtu.be/Yn1A0mGw6Ck?si=dlDEVUk3xiZCS41I) |

---

## 🙏 Credits

### Developers

- **bkerler** - [mtkclient](https://github.com/bkerler/mtkclient) - MediaTek device savior
- **hasan6034** - LineageOS 20 builds for selene - [SourceForge](https://sourceforge.net/projects/hasan6034-builds/)
- **TWRP Team** - Team Win Recovery Project
- **topjohnwu** - [Magisk](https://github.com/topjohnwu/Magisk) - Systemless root
- **vm03** - [payload_dumper](https://github.com/vm03/payload_dumper) - Image extraction tool
- **mishubepo** - [ABootLoop](https://mmrl.dev/repository/mishubepo/abootloop) - Bootloop prevention

### Special Thanks

- **LineageOS Team** - Clean Android experience
- **Open Source Community** - Making this possible

---

## 📄 License

MIT License



---
