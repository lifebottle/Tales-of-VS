

::use this to reduce to 8bpp the images so that index8 of gimconv work proprely

::tools/pngquant/pngquant.exe --force --verbose 256 title.png

::@echo off
::setlocal enabledelayedexpansion
::set "pngquant= tools\Pngquant\pngquant.exe"
::
::for /r "2_translated/USRDIR/2D/test" %%F in (*.png) do (
::    echo Processing: "%%F"
::    call %pngquant% --force --verbose 256 --ext .png "%%F"
::)

@echo off
set "GimConvDir=tools\GimConv"
set "SourceDir=2_translated\USRDIR\2D\test"

for /r "%SourceDir%" %%F in (*.png) do (
    pushd "%GimConvDir%"
    gimconv "%%F" -o "%%~dpF%%~nF.gim"
    popd
)

::--image_format index8


::::Build command for the gim conversion
::pushd "tools/GimConv/"
::gimconv ../../2_translated/USRDIR/CLIMAX/data/bg/title.png --image_format index8 -o ../../3_patched/USRDIR/CLIMAX/data/bg/title.gim
::popd



Pause