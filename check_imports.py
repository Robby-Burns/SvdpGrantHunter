import sys
import os

print(f"Current Directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import svdpgrantagent
    print("SUCCESS: imported svdpgrantagent (lowercase)")
except ImportError as e:
    print(f"FAILURE: could not import svdpgrantagent (lowercase): {e}")

try:
    import SvdpGrantAgent
    print("SUCCESS: imported SvdpGrantAgent (caps)")
except ImportError as e:
    print(f"FAILURE: could not import SvdpGrantAgent (caps): {e}")

try:
    import exporter
    print("SUCCESS: imported exporter directly")
except ImportError as e:
    print(f"FAILURE: could not import exporter directly: {e}")
