#SingleInstance force
#NoEnv
确保管理员权限:
if not A_IsAdmin
{
   Run *RunAs "%A_ScriptFullPath%"  ; 需要 v1.0.92.01+
   ExitApp
}
Sendmode Input

ClipBoard =
WinWaitNotActive, ahk_exe explorer.exe
WinGetActiveTitle, DefaultRoomName
InputBox, RoomName, , 房间名称, , 250, 120, , , , , %DefaultRoomName%
BlockInput on
Run "firefox" -new-window imacros://run/?m=live.bilibili`%5CLiveTitleChange.iim
WinMaximize, ahk_exe firefox.exe
WinWaitActive, iMacros ahk_class MozillaDialogClass
Send {ENTER}
WinWaitActive, ahk_exe firefox.exe, , , iMacros ahk_class MozillaDialogClass
Send ^f
Sleep, 0 
Sleep 1000
ClipBoard = ForFindingTheTextInputBox
Send ^v
Sleep, 0 
Sleep 1000
Send {ESC}
Sleep, 0 
Sleep 1000
Send ^a
ClipBoard = %RoomName%
Send ^v
BlockInput off
ExitApp

$esc::ExitApp