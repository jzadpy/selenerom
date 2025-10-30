#!/bin/bash
# Selene Download Manager - Bash version
# Downloads all required files for LineageOS installation

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Default directory
DOWNLOAD_DIR="$HOME/redmi-selene"

# Download links
declare -A DOWNLOADS=(
    ["twrp_name"]="TWRP Recovery"
    ["twrp_url"]="https://drive.google.com/uc?export=download&id=17ebo3DD077HihnncSpQ6X0beChycxJRu"
    ["twrp_file"]="twrp-selene.img"
    
    ["fw12_name"]="Stock Firmware 12.5"
    ["fw12_url"]="https://bigota.d.miui.com/V12.5.20.0.RKUMIXM/miui_SELENEGlobal_V12.5.20.0.RKUMIXM_37f0d4aaa7_11.0.zip"
    ["fw12_file"]="selene_12.5.20.zip"
    
    ["fw14_name"]="Stock Firmware 14"
    ["fw14_url"]="https://bigota.d.miui.com/V14.0.7.0.TKUMIXM/selene_global_images_V14.0.7.0.TKUMIXM_20240517.0000.00_13.0_global_63a8c6a62f.tgz"
    ["fw14_file"]="selene_14.0.7.tgz"
    
    ["mtk_name"]="MTKClient"
    ["mtk_url"]="https://github.com/bkerler/mtkclient/archive/refs/heads/main.zip"
    ["mtk_file"]="mtkclient-main.zip"
    
    ["pd_name"]="Payload Dumper"
    ["pd_url"]="https://github.com/vm03/payload_dumper/archive/refs/heads/master.zip"
    ["pd_file"]="payload_dumper-master.zip"
    
    ["adb_name"]="ADB Platform Tools"
    ["adb_url"]="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
    ["adb_file"]="platform-tools-latest-linux.zip"
    
    ["magisk_name"]="Magisk"
    ["magisk_url"]="https://github.com/topjohnwu/Magisk/releases/download/v27.0/Magisk-v27.0.apk"
    ["magisk_file"]="magisk27.apk"
    
    ["aboot_name"]="Anti-Bootloop"
    ["aboot_url"]="https://github.com/Mishu-bepo/abootloop/releases/download/1.0/abootloop-1.0.zip"
    ["aboot_file"]="abootloop.zip"
)

CUSTOM_ROM_SF="https://sourceforge.net/projects/hasan6034-builds/files/selene/"

print_header() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║          SELENE DOWNLOAD MANAGER                 ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_menu() {
    echo -e "${BLUE}Current directory: ${DOWNLOAD_DIR}${NC}"
    echo ""
    echo "────────────────────────────────────────────────────"
    echo "       Choose download:"
    echo "────────────────────────────────────────────────────"
    echo " 1. TWRP Recovery"
    echo " 2. Stock Firmware 12.5"
    echo " 3. Stock Firmware 14"
    echo " 4. Custom ROMs (external link)"
    echo " 5. MTKClient"
    echo " 6. Payload Dumper"
    echo " 7. ADB Platform Tools"
    echo " 8. Magisk and Anti-Bootloop"
    echo " 9. :::ALL::: (except Custom ROM)"
    echo ""
    echo "00. Change directory"
    echo " 0. Exit"
    echo "────────────────────────────────────────────────────"
}

download_file() {
    local url="$1"
    local filename="$2"
    local filepath="${DOWNLOAD_DIR}/${filename}"
    
    echo ""
    echo -e "${YELLOW}Downloading ${filename}...${NC}"
    echo -e "${BLUE}Destination: ${filepath}${NC}"
    
    mkdir -p "$DOWNLOAD_DIR"
    
    if wget --show-progress -O "$filepath" "$url" 2>&1; then
        echo -e "${GREEN}✓ ${filename} downloaded successfully!${NC}"
        return 0
    else
        echo -e "${RED}✗ Error downloading ${filename}${NC}"
        return 1
    fi
}

download_item() {
    local key="$1"
    local name_key="${key}_name"
    local url_key="${key}_url"
    local file_key="${key}_file"
    
    echo ""
    echo -e "${YELLOW}${DOWNLOADS[$name_key]} will be downloaded to ${DOWNLOAD_DIR}${NC}"
    read -p "Is this okay? (y/n): " confirm
    
    if [[ "$confirm" == "y" ]]; then
        download_file "${DOWNLOADS[$url_key]}" "${DOWNLOADS[$file_key]}"
    fi
}

download_custom_rom() {
    echo ""
    echo -e "${YELLOW}Opening SourceForge in browser...${NC}"
    echo -e "${CYAN}${CUSTOM_ROM_SF}${NC}"
    xdg-open "$CUSTOM_ROM_SF" 2>/dev/null || open "$CUSTOM_ROM_SF" 2>/dev/null
    
    echo ""
    echo "Please copy the download link from SourceForge and paste here:"
    read -p "Download link: " url
    
    if [[ -z "$url" ]]; then
        echo "No link provided. Cancelled."
        return
    fi
    
    read -p "Enter filename (e.g., lineage-20-selene.zip): " filename
    [[ -z "$filename" ]] && filename="custom_rom.zip"
    
    echo ""
    echo -e "${YELLOW}Custom ROM will be downloaded to ${DOWNLOAD_DIR}${NC}"
    read -p "Is this okay? (y/n): " confirm
    
    if [[ "$confirm" == "y" ]]; then
        download_file "$url" "$filename"
    fi
}

download_magisk_group() {
    echo ""
    echo -e "${YELLOW}Downloading Magisk and Anti-Bootloop...${NC}"
    echo -e "${BLUE}Destination: ${DOWNLOAD_DIR}${NC}"
    read -p "Is this okay? (y/n): " confirm
    
    if [[ "$confirm" == "y" ]]; then
        download_file "${DOWNLOADS[magisk_url]}" "${DOWNLOADS[magisk_file]}"
        download_file "${DOWNLOADS[aboot_url]}" "${DOWNLOADS[aboot_file]}"
    fi
}

download_all() {
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "ALL WILL BE DOWNLOADED (EXCEPT CUSTOM ROM)!"
    echo "════════════════════════════════════════════════════"
    echo ""
    echo "This includes:"
    echo "  • TWRP Recovery"
    echo "  • Stock Firmware 12.5"
    echo "  • Stock Firmware 14"
    echo "  • MTKClient"
    echo "  • Payload Dumper"
    echo "  • ADB Platform Tools"
    echo "  • Magisk"
    echo "  • Anti-Bootloop"
    echo ""
    echo -e "${BLUE}Destination: ${DOWNLOAD_DIR}${NC}"
    read -p "Is this okay? (y/n): " confirm
    
    if [[ "$confirm" != "y" ]]; then
        return
    fi
    
    local items=("twrp" "fw12" "fw14" "mtk" "pd" "adb" "magisk" "aboot")
    local total=${#items[@]}
    local current=0
    
    for key in "${items[@]}"; do
        ((current++))
        name_key="${key}_name"
        url_key="${key}_url"
        file_key="${key}_file"
        
        echo ""
        echo -e "${CYAN}[${current}/${total}] Downloading ${DOWNLOADS[$name_key]}...${NC}"
        download_file "${DOWNLOADS[$url_key]}" "${DOWNLOADS[$file_key]}"
    done
    
    echo ""
    echo "════════════════════════════════════════════════════"
    echo -e "${GREEN}ALL DOWNLOADS COMPLETED!${NC}"
    echo "════════════════════════════════════════════════════"
    read -p "Press Enter to continue..."
}

change_directory() {
    echo ""
    echo -e "${BLUE}Current directory: ${DOWNLOAD_DIR}${NC}"
    read -p "Please paste new directory here: " new_dir
    
    if [[ -n "$new_dir" ]]; then
        new_dir="${new_dir/#\~/$HOME}"
        mkdir -p "$new_dir" 2>/dev/null
        
        if [[ -d "$new_dir" ]]; then
            echo -e "${GREEN}Changed directory from '${DOWNLOAD_DIR}' to '${new_dir}'${NC}"
            echo "All files will be downloaded to this folder"
            DOWNLOAD_DIR="$new_dir"
        else
            echo -e "${RED}Error creating directory${NC}"
        fi
    fi
    
    read -p "Press Enter to continue..."
}

main() {
    while true; do
        print_header
        print_menu
        
        echo ""
        read -p "Enter your choice: " choice
        
        case "$choice" in
            0)
                echo ""
                echo "Exiting... Goodbye!"
                exit 0
                ;;
            00)
                change_directory
                ;;
            1)
                download_item "twrp"
                read -p "Press Enter to continue..."
                ;;
            2)
                download_item "fw12"
                read -p "Press Enter to continue..."
                ;;
            3)
                download_item "fw14"
                read -p "Press Enter to continue..."
                ;;
            4)
                download_custom_rom
                read -p "Press Enter to continue..."
                ;;
            5)
                download_item "mtk"
                read -p "Press Enter to continue..."
                ;;
            6)
                download_item "pd"
                read -p "Press Enter to continue..."
                ;;
            7)
                download_item "adb"
                read -p "Press Enter to continue..."
                ;;
            8)
                download_magisk_group
                read -p "Press Enter to continue..."
                ;;
            9)
                download_all
                ;;
            *)
                echo ""
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                sleep 1
                ;;
        esac
    done
}

# Run
main
