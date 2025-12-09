import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from snap_backup.utils import sanitize_filename, generate_unique_string
from snap_backup.download import decide_extension


# -------------------------
# Utils tests
# -------------------------

def test_sanitize_filename_removes_invalid_chars():
    unsafe = '2025:09:15 17/46*56 UTC'
    safe = sanitize_filename(unsafe)
    # Ensure invalid characters are replaced
    assert ":" not in safe
    assert "/" not in safe
    assert "*" not in safe
    # Should still contain the date text
    assert "2025" in safe

def test_generate_unique_string_length_and_charset():
    s = generate_unique_string(8)
    assert len(s) == 8
    # Only alphanumeric characters
    assert all(c.isalnum() for c in s)

# -------------------------
# Download tests
# -------------------------

def test_decide_extension_with_url_extension():
    # If URL already has extension, use it
    assert decide_extension(".jpg", "image") == ".jpg"
    assert decide_extension(".mp4", "video") == ".mp4"

def test_decide_extension_image_type():
    # No extension, but media type is image
    assert decide_extension("", "image") == ".jpg"

def test_decide_extension_video_type():
    # No extension, but media type is video
    assert decide_extension("", "video") == ".mp4"

def test_decide_extension_default_zip():
    # No extension and no media type
    assert decide_extension("", None) == ".zip"
