# -*- coding: utf-8 -*-
"""xq_native_adapter.py — thin Win32-native adapter for XQ desktop automation.

Scope: deterministic Win32 execution ONLY. No planning, no WorkOrder authority,
no retry authority, no financial decisions, no acceptance.

Backend: pywinauto win32 (BM_CLICK/TB_PRESSBUTTON/WM_SETTEXT/TVM messages).
Pure-message input only — never moves the real cursor, never takes focus.

Selector priority: HWND/process > control_id/class > menu/accelerator > UIA > visual > pixel.

Build binding: every call SHOULD be gated by XQ_BUILD_FINGERPRINT equality (see
FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json). Never assume selector validity across builds.
"""
import ctypes
import ctypes.wintypes as wt

# --- control message constants (Win32) ---
WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
WM_SETTEXT = 0x000C
WM_GETTEXT = 0x000D
TB_PRESSBUTTON = 0x0408
TB_BUTTONCOUNT = 0x0418
TB_ISBUTTONENABLED = 0x041D

user32 = ctypes.windll.user32


def find_main_window(title_sub="XQ全球贏家", pid=None):
    """Locate DAQXQLITEMainWnd via win32 EnumWindows (no UIA)."""
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, t, 256)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(hwnd, cls, 64)
        if cls.value == "DAQXQLITEMainWnd" and title_sub in t.value:
            p = wt.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
            if pid is None or p.value == pid:
                out.append(hwnd)
        return True
    user32.EnumWindows(cb, 0)
    return out[0] if out else None


def find_window_by_title(title_sub, class_name=None):
    """Find a top-level window by title substring (win32 only)."""
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, t, 256)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(hwnd, cls, 64)
        if title_sub in t.value and (class_name is None or cls.value == class_name):
            out.append(hwnd)
        return True
    user32.EnumWindows(cb, 0)
    return out


def enum_children(hwnd):
    """List child controls: hwnd, class, text, control_id."""
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        cid = user32.GetDlgCtrlID(ch)
        out.append({"hwnd": ch, "class": cls.value, "text": t.value[:40], "cid": cid})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


def find_child(hwnd, cid=None, class_name=None, text=None):
    """Find first child matching control_id/class/text."""
    for c in enum_children(hwnd):
        if cid is not None and c["cid"] != cid:
            continue
        if class_name and c["class"] != class_name:
            continue
        if text is not None and text not in c["text"]:
            continue
        return c
    return None


def invoke_button(hwnd, cid=None, class_name="Button", text=None):
    """Invoke a button via BM_CLICK (pure message, no mouse)."""
    c = find_child(hwnd, cid=cid, class_name=class_name, text=text)
    if c is None:
        return False
    user32.PostMessageW(c["hwnd"], BM_CLICK, 0, 0)
    return True


def set_edit_text(hwnd, cid=None, text=None, value=""):
    """Set an Edit control's text via WM_SETTEXT (same-integrity SendMessage)."""
    c = find_child(hwnd, cid=cid, class_name="Edit", text=text)
    if c is None:
        return False
    buf = ctypes.create_unicode_buffer(value)
    user32.SendMessageW(c["hwnd"], WM_SETTEXT, 0, ctypes.cast(buf, ctypes.c_void_p))
    return True


def get_edit_text(hwnd, cid=None):
    """Read an Edit control's text via WM_GETTEXT."""
    c = find_child(hwnd, cid=cid, class_name="Edit")
    if c is None:
        return None
    buf = ctypes.create_unicode_buffer(256)
    user32.SendMessageW(c["hwnd"], WM_GETTEXT, 256, ctypes.cast(buf, ctypes.c_void_p))
    return buf.value


def press_toolbar(toolbar_hwnd, command_id):
    """Press a toolbar button by command id. VERIFIED 2026-08-14 (XQ 3.20.02-260811):
    TB_PRESSBUTTON returns 0 (no-op) on XQ's ToolbarWindow32; the working message path
    (pywinauto ToolbarButton.click equivalent) is WM_LBUTTONDOWN/UP at the button rect.
    Sequence: TB_BUTTONCOUNT -> TB_GETBUTTON (find index by idCommand) -> TB_GETITEMRECT
    -> WM_LBUTTONDOWN/UP. Pure messages, zero mouse.
    """
    TB_BUTTONCOUNT = 0x0418
    TB_GETBUTTON = 0x0417
    TB_GETITEMRECT = 0x0419
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    MK_LBUTTON = 0x0001

    n = user32.SendMessageW(toolbar_hwnd, TB_BUTTONCOUNT, 0, 0)
    if not n:
        return False
    # TBBUTTON struct: iBitmap, idCommand, fsState, fsStyle, dwData, iString (6 fields, 20 bytes x86 / 24 x64)
    SZ = ctypes.sizeof(ctypes.c_int) * 4 + ctypes.sizeof(ctypes.c_void_p) * 2
    for idx in range(n):
        buf = ctypes.create_string_buffer(SZ)
        if not user32.SendMessageW(toolbar_hwnd, TB_GETBUTTON, idx, ctypes.cast(buf, ctypes.c_void_p)):
            continue
        # idCommand is 2nd int (offset 4)
        cid = int.from_bytes(buf.raw[4:8], "little")
        if cid == command_id:
            # get item rect
            rect = (ctypes.c_long * 4)()
            if not user32.SendMessageW(toolbar_hwnd, TB_GETITEMRECT, idx, ctypes.cast(rect, ctypes.c_void_p)):
                return False
            left, top, right, bottom = rect
            cx = (left + right) // 2
            cy = (top + bottom) // 2
            lparam = (cy << 16) | (cx & 0xFFFF)
            user32.SendMessageW(toolbar_hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lparam)
            user32.SendMessageW(toolbar_hwnd, WM_LBUTTONUP, 0, lparam)
            return True
    return False


def toolbar_button_count(toolbar_hwnd):
    return user32.SendMessageW(toolbar_hwnd, TB_BUTTONCOUNT, 0, 0)


def is_button_enabled(hwnd):
    """Check enabled state via win32 (returns None if control gone)."""
    return bool(user32.IsWindowEnabled(hwnd))


def close_window(hwnd):
    """Close a window via WM_CLOSE (message only)."""
    return bool(user32.PostMessageW(hwnd, WM_CLOSE, 0, 0))


if __name__ == "__main__":
    import json
    mw = find_main_window()
    print("main hwnd:", hex(mw) if mw else None)
    if mw:
        kids = enum_children(mw)
        print("children:", len(kids))
