@ECHO OFF

CD /D %~dp0
ECHO %~dp0

ECHO List of videos in "all videos.txt"
FOR /F "usebackq" %%u IN ("all videos.txt") DO ECHO %%u

ECHO.
ECHO To start press the any key...
PAUSE >nul

FOR /F "usebackq delims=/ tokens=4" %%v IN ("all videos.txt") DO CALL :GetAll %%v

ECHO Done.
PAUSE
GOTO :End

:GetAll
ECHO.
ECHO Downloading chats for VOD %1...

ECHO Downloading raw JSON
app.py -f raw -v %1
ECHO.

ECHO Downloading timestamped text
app.py -f timestamp -v %1
IF %ERRORLEVEL% EQU 0 MOVE "chats\v%1.txt" "chats\v%1timestamp.txt" >NUL
ECHO.

ECHO Downloading relative timecoded text
app.py -f relative -v %1
IF %ERRORLEVEL% EQU 0 MOVE "chats\v%1.txt" "chats\v%1relative.txt" >NUL
ECHO.

ECHO Downloading SRT subtitle
app.py -f srt -v %1
ECHO.

ECHO Downloading SSA subtitle
app.py -f ssa -v %1
ECHO.

EXIT /B

:End
