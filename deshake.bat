@echo off 

for /r %%a in (*.avi) do (
	echo directshowSource^("%%~fa"^) > "%%~na.avs"
)

for /F %%a in ('dir /B/D *.avs') do (
	echo Processing "%%~fa" pass 1... 
	..\vdub64.exe /s deshake1.vcf /p "%%~fa" "%%~fa.deshaken.avi" /r /c /x 
	echo Processing "%%~fa" pass 2... 
	..\vdub64.exe /s deshake2.vcf /p "%%~fa" "%%~fa.deshaken.avi" /r /c /x
)

del *.avs