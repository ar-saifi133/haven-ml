# Python Version Requirements

## Recommended: Python 3.13

This project was developed and tested with **Python 3.13.7** and all dependencies are confirmed working.

## Supported Versions

- ✅ **Python 3.13** (Recommended - fully tested)
- ✅ **Python 3.12** (Should work)
- ✅ **Python 3.11** (Should work)
- ⚠️ **Python 3.10** (May work, some packages might need older versions)
- ❌ **Python 3.9 or older** (Not recommended - missing features)

## Why Python 3.13?

The latest versions of key dependencies work great with Python 3.13:
- PyTorch 2.10.0 ✅
- TensorFlow 2.20.0 ✅
- Transformers 5.1.0 ✅
- DeepFace 0.0.98 ✅
- Whisper (latest) ✅
- pyttsx3 2.99 ✅

## Installation Issues?

If someone has errors installing, they should:

1. **Check Python version**:
   ```bash
   python --version
   ```
   Should show 3.11, 3.12, or 3.13

2. **Use virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Upgrade pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

## Common Installation Errors

### Error: "No matching distribution found"
**Solution**: Upgrade Python to 3.11+ or use compatible package versions

### Error: "Microsoft Visual C++ required"
**Solution (Windows)**: Install Visual C++ Build Tools
- Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Error: "Failed building wheel for X"
**Solution**: Install package individually to see specific error:
```bash
pip install package-name
```

## System Requirements

- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.11, 3.12, or 3.13
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 5GB free space
- **Optional**: NVIDIA GPU with CUDA for faster processing
