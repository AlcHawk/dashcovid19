set /p dashdir=<dashdirectoryname.txt
set tdy=%date:~0, 4%%date:~5, 2%%date:~8, 2%

set LOG_FILE=%dashdir%/BatchLog/cmdlog_%tdy%.log
call %dashdir%/crawlertask.bat %dashdir% %tdy% >> %LOG_FILE% 2>&1