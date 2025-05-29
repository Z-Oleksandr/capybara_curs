import ctypes
import atexit
import signal
import time
import os
import sys

# Win const and api
SPI_SETCURSORS = 0x0057
SPI_GETCURSORS = 0x0057
ARROW = 32512

OCR_SYSTEM_CURSORS = {
    32512: "main_cursor_capybara_cursor.cur",          # OCR_NORMAL (Arrow)
    32513: "type_cursor_capybara.cur",                 # OCR_IBEAM (Text select)
    32514: "load_cursor_capybara.cur",                 # OCR_WAIT (Busy)
    32516: "up_cursor_capybara.cur",                   # OCR_UP
    32642: "diagonal_cursor_capybara.cur",             # OCR_DIAGONAL_LEFT_IS_UP
    32643: "diagonal-right-is-up_cursor_capybara.cur", # OCR_DIAGONAL_RIGHT_IS_UP
    32644: "left-right_cursor_capybara.cur",           # OCR_SIZEWE
    32645: "up-down_cursor_capybara.cur",              # OCR_SIZENS
    32646: "all-directions_cursor_capybara.cur",       # OCR_SIZEALL (move)
    32648: "nono_cursor_capybara.cur",                 # OCR_NO
    32649: "ok-o_cursor_capybara.cur",                 # OCR_HAND
    32651: "question_cursor_help_capybara.cur",        # OCR_HELP
}

if getattr(sys, 'frozen', False):
  base_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
else:
  base_dir = os.path.dirname(os.path.abspath(__file__))

CURSOR_DIR = os.path.join(base_dir, "curs")

SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW
LoadCursorFromFile = ctypes.windll.user32.LoadCursorFromFileW
SetSystemCursor = ctypes.windll.user32.SetSystemCursor
LoadCursor = ctypes.windll.user32.LoadCursorW
CopyIcon = ctypes.windll.user32.CopyIcon

original_cursors = {}

def set_custom_cursor(write_line):
  for cursor_id, filename in OCR_SYSTEM_CURSORS.items():
    path = os.path.join(CURSOR_DIR, filename)
    hcursor = LoadCursorFromFile(path)
    if not hcursor:
      write_line(f"Failed to load: {path}")
      continue
    success = SetSystemCursor(hcursor, cursor_id)
    if not success:
      write_line(f"Failed to set custom cursor: {filename}")
    else:
      write_line(f"Cursor {cursor_id} set to be: {filename}")

  write_line("Custom cursors applied!")

def restore_cursor(write_line):
  for cursor_id, hcursor in original_cursors.items():
    success = SetSystemCursor(hcursor, cursor_id)
    if not success:
      write_line(f"Failed to restore cursor {cursor_id}")
  write_line("Cursors restored!")

def default_cursors(write_line):
    if not SystemParametersInfo(SPI_SETCURSORS, 0, None, 0):
      raise ctypes.WinError()
    write_line("Windows cursors reset to default!")

def capture_original_cursors():
  for cursor_id in OCR_SYSTEM_CURSORS.keys():
    original_cursors[cursor_id] = CopyIcon(LoadCursor(0, cursor_id))

capture_original_cursors()
signal.signal(signal.SIGINT, lambda sig, frame: exit(0)) # Handle Ctrl+C
