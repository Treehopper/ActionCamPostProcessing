@echo off 

REM requires VirtualDub 64, Avisynth 64 and Deshaker plugin
REM create a folder in your VirtualDub install folder, copy this script + *.vcf files + videos as avi containers over, and run script

deshaker_conf.py --deshaker=1 > deshake1.vcf
deshaker_conf.py --deshaker=2 --acompress --vcompress --smoother > deshake2.vcf

for /r %%a in (*.avi) do (
	echo directshowSource^("%%~fa"^) > "%%~na.avs"
)

for /F %%a in ('dir /B/D *.avs') do (
	echo Processing "%%~fa" pass 1... 
	..\vdub.exe /s deshake1.vcf /p "%%~fa" "%%~fa.deshaken.avi" /r /c /x 
	echo Processing "%%~fa" pass 2... 
	..\vdub.exe /s deshake2.vcf /p "%%~fa" "%%~fa.deshaken.avi" /r /c /x
)

del *.avs
