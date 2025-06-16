from native.windows.win_clip_api import copy, paste


def clipboard_get():
    clipboard_content = paste()
    return clipboard_content


def clipboard_set(text):
    copy(text)

if __name__ == "__main__":
    # Test the clipboard functions
    test_text = "Hello, this is a test!"
    
    # Test setting clipboard
    print("Setting clipboard content to:", test_text)
    clipboard_set(test_text)
    
    # Test getting clipboard
    result = clipboard_get()
    print("Getting clipboard content:", result)
    
    # Verify if the content matches
    assert result == test_text, "Clipboard content doesn't match!"
    print("Test passed successfully!")