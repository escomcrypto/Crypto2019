REM echo off
SetLocal EnableDelayedExpansion
set RUNNING_VM=false
set ISE_LOGGED=false
set VBOXPATH=%1
set APP=%2
set APPROOT=ISE
if "%APP%"=="xsdk" set APPROOT=EDK
if "%APP%"=="xps" set APPROOT=EDK
set COMMAND="/opt/Xilinx/14.7/ISE_DS/%APPROOT%/bin/lin64/%APP%"
if "%APP%"=="xsdk" set COMMAND="/opt/Xilinx/14.7/ISE_DS/%APPROOT%/bin/lin64/xsdk" -- xsdk -vmargs -Dorg.eclipse.swt.internal.gtk.cairoGraphics=false"
if "%APP%"=="ise" set COMMAND="/opt/Xilinx/14.7/ISE_DS/common/app_launcher.sh" -- app_launcher.sh %APP%

pushd %VBOXPATH%
for /f %%i in ('vboxmanage.exe list runningvms') do ^
if %%i=="ISE_14.7_VIRTUAL_APPLIANCE" set RUNNING_VM=true
for /f "tokens=2" %%i in ('VBoxManage.exe guestproperty get "ISE_14.7_VIRTUAL_APPLIANCE" "/VirtualBox/GuestInfo/OS/LoggedInUsersList"') do ^
if "%%i"=="ise" set ISE_LOGGED=true
popd

pushd %VBOXPATH%
if "%RUNNING_VM%"=="false" (
VBoxManage.exe startvm ISE_14.7_VIRTUAL_APPLIANCE
VBoxManage.exe guestproperty wait "ISE_14.7_VIRTUAL_APPLIANCE" "/VirtualBox/GuestInfo/OS/LoggedInUsersList"
VBoxManage.exe guestcontrol "ISE_14.7_VIRTUAL_APPLIANCE" --verbose start --username ise --password xilinx --putenv "DISPLAY=:0" --putenv "XILINX=/opt/Xilinx/14.7/ISE_DS/ISE" --exe %COMMAND%
) ELSE (
if "%ISE_LOGGED%"=="false" (
VBoxManage.exe guestproperty wait "ISE_14.7_VIRTUAL_APPLIANCE" "/VirtualBox/GuestInfo/OS/LoggedInUsersList"
VBoxManage.exe guestcontrol "ISE_14.7_VIRTUAL_APPLIANCE" --verbose start --username ise --password xilinx --putenv "DISPLAY=:0" --putenv "XILINX=/opt/Xilinx/14.7/ISE_DS/ISE" --exe %COMMAND%
) ELSE (
VBoxManage.exe guestcontrol "ISE_14.7_VIRTUAL_APPLIANCE" --verbose start --username ise --password xilinx --putenv "DISPLAY=:0" --putenv "XILINX=/opt/Xilinx/14.7/ISE_DS/ISE" --exe %COMMAND%
)
)
popd