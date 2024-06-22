# Re1999-Tools

This repository contains tools for the game `Reverse: 1999`. The tools are written in Python and are intended to be used with the game's data files.

## Tools

### global-metadata.py

**Game Version**: v1.6.0  
For decrypting the `global-metadata.dat` file.  
The file is located in the apk with the path `/assets/bin/Data/Managed/Resources/MobileVideo.dll-resources.dat`.

### asset-bundles.py

**Game Version**: v1.6.0  
For decrypting encrypted Unity AssetBundles.

### lua-bundles/extract.py

**Game Version**: v1.6.0  
For extracting Lua scripts from custom Lua bundles.
The Lua bundles are located in `/sdcard/Android/data/com.bluepoch.m.en.reverse1999/files/ResLib/Android/luabytes` on Android devices.

### lua-bundles/decompile.py

For decompiling Lua scripts extracted from custom Lua bundles.  
The script will attempt to map the hashed file names to the original file names, for files that are failed to be mapped, the hashed file names will be used instead.

## Disclaimer

This project is not affiliated with Bluepoch Co.,Ltd. The tools are intended for research purposes only.
