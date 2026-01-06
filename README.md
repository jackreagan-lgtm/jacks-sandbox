# Prep for Burn-In Script

## Overview

`prep_for_burn_in.py` is an automated X-ray source detection and configuration script designed for Lumafield's Seah CT scanning system. It automatically identifies the connected X-ray source type (VJX or Hamamatsu) and configures the system settings accordingly.

## Features

- **Automatic Source Detection**: Identifies VJX and Hamamatsu X-ray sources via serial communication
- **Dynamic Driver Switching**: Automatically configures the correct driver (VJX or Hamamatsu) in system settings
- **Seamless Source Swapping**: Switch between different source types without manual configuration
- **System Preparation**: Prepares the system for burn-in testing by resetting warming history
- **Colored Output**: Provides clear, color-coded feedback during operation

## Recent Changes (January 2026)

### Added Dynamic Driver Configuration
- **Problem Solved**: Previously, switching from VJX to Hamamatsu sources (or vice versa) required manual settings file editing
- **Solution**: Script now automatically updates `/etc/seah/settings.json` with the correct source driver and model
- **Benefits**: 
  - No more manual driver configuration
  - Seamless source type switching
  - Eliminates configuration errors when swapping sources

### Technical Implementation
- Added `write_source_settings()` function to modify system configuration
- Direct JSON manipulation of `/etc/seah/settings.json`
- Preserves all existing system settings while updating only source-specific configuration

## Usage

```bash
sudo python3 prep_for_burn_in.py [serial_port]
```

**Parameters:**
- `serial_port` (optional): Serial port path (defaults to `/dev/ttyUSBXRAY`)

**Example:**
```bash
sudo python3 prep_for_burn_in.py
sudo python3 prep_for_burn_in.py /dev/ttyUSB0
```

## What the Script Does

### 1. VJX Source Detection
- Connects to X-ray source via serial communication
- Sends `SNUM` command to identify source
- Matches serial identifier against known VJX sources:
  - 120 kV sources: 673, 649, 112, 796
  - 120 kV DC source: 755
  - 160 kV DC source: 747
  - 190 kV sources: 401, 643
  - 320 kV source: 662

### 2. Hamamatsu Source Detection
- If no VJX found, attempts Hamamatsu detection
- Uses 38400 baud rate communication
- Sends `SHS` command to identify Hamamatsu source
- Recognizes L9181 and L12161 series sources

### 3. System Configuration
- Updates `/etc/seah/settings.json` with detected source information
- Sets appropriate driver: `"vjx"` or `"hamamatsu"`
- Sets correct model identifier for the detected source
- Preserves all other system settings

### 4. System Preparation
- Terminates any running Seah processes
- Resets VJX usage history (`/var/seah/vjx_usage_history.json`)
- Prepares system for clean burn-in testing

## Output Files

### 1. Settings Configuration
- **File**: `/etc/seah/settings.json`
- **Content**: Updated with detected source driver and model
- **Example for VJX**:
  ```json
  {
    "source": {
      "driver": "vjx",
      "model": "IXS120BP036P112"
    }
  }
  ```
- **Example for Hamamatsu**:
  ```json
  {
    "source": {
      "driver": "hamamatsu", 
      "model": "L9181-02"
    }
  }
  ```

### 2. Model Output File
- **File**: `model_output_file.txt`
- **Content**: Model identifier for backward compatibility
- **Examples**: `IXS120BP036P112`, `L9181-02`

## Supported X-Ray Sources

### VJX Sources
| Serial ID | Model | kV Range | uA Range | Type |
|-----------|--------|----------|----------|------|
| 673 | IXS120BP036P112 | 40-120 | 50-300 | 120kV VJX |
| 649 | IXS120BP036P112 | 40-120 | 50-300 | 120kV VJX |
| 112 | IXS120BP036P112 | 40-120 | 50-300 | 120kV VJX |
| 796 | IXS120BP036P112 | 40-120 | 50-300 | 120kV P673 Luxbright |
| 755 | IXS120BP096P755 | 80-120 | 200-800 | 120kV VJX DC |
| 747 | IXS160BP100P747 | 80-160 | 200-625 | 160kV VJX DC |
| 401 | IXS200BP150P401 | 100-190 | 200-500 | 190kV VJX |
| 643 | IXS200BP150P401 | 100-190 | 200-500 | 190kV VJX |
| 662 | IXS320BP800P662 | 160-320 | 500-2500 | 320kV VJX |

### Hamamatsu Sources
| Model | kV Range | uA Range | Description |
|--------|----------|----------|-------------|
| L9181-02 | 40-130 | 0-300 | 130kV Hamamatsu |

## Prerequisites

- Python 3.x
- `pyserial` library (`pip install pyserial`)
- Root/sudo privileges (required for modifying system settings)
- X-ray source connected via serial port

## Workflow Example

### Switching from VJX to Hamamatsu:
1. Power down system and physically swap X-ray sources
2. Power up with Hamamatsu source connected
3. Run: `sudo python3 prep_for_burn_in.py`
4. Script detects Hamamatsu and updates settings to `"driver": "hamamatsu"`
5. System ready for Hamamatsu operation

### Switching from Hamamatsu back to VJX:
1. Power down and physically swap back to VJX source
2. Power up with VJX source connected  
3. Run: `sudo python3 prep_for_burn_in.py`
4. Script detects VJX (e.g., serial 747) and updates settings to `"driver": "vjx"`
5. System ready for VJX operation

## Error Handling

- **Serial Communication Errors**: Gracefully handled with error messages
- **File Permission Errors**: Requires sudo privileges for system file modification
- **Unknown Sources**: Reports unrecognized source types
- **Missing Dependencies**: Clear error messages for missing libraries

## Troubleshooting

### Common Issues:
1. **"Permission denied"**: Run with `sudo` to modify system settings
2. **"No module named 'serial'"**: Install pyserial: `pip install pyserial`
3. **"Source not detected"**: Check serial cable connections and port permissions
4. **"Settings not updated"**: Verify `/etc/seah/settings.json` exists and is writable

### Debug Steps:
1. Check serial port: `ls -la /dev/ttyUSB*`
2. Test serial communication: `screen /dev/ttyUSBXRAY 9600`
3. Verify file permissions: `ls -la /etc/seah/settings.json`
4. Check script output for colored error messages

## Author

Lumafield Engineering Team

## Last Updated

January 2026 - Added automatic driver switching functionality
