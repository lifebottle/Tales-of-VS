@echo off
setlocal

set "command=TextER -e [file] -gim"

for %%F in (*.*) do (
		TextER -e %%F -gim
)

endlocal

pause



