import ctypes


# Constants for different message box types
MB_OK = 0x0
MB_OKCANCEL = 0x1
MB_YESNO = 0x4

# Constants for different icon styles
ICON_EXLAIM = 0x30
ICON_INFO = 0x40
ICON_ERROR = 0x10
ICON_QUESTION = 0x20

def pop_up_erro(erro):
    ctypes.windll.user32.MessageBoxW(0, f"{erro}", "ERRO:", MB_OK | ICON_ERROR)

def pop_up_check(check):
    ctypes.windll.user32.MessageBoxW(0, f"{check}", "INFO:", MB_OK | ICON_INFO)