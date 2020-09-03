REM set /p dashdir=<dashdirectoryname.txt
set dashdir=%1
REM call echo %dashdir%

C:
cd /
cd %dashdir%
call conda activate dashcovid19
python download_source.py %dashdir%
call conda deactivate

REM set tdy=%date:~0, 4%%date:~5, 2%%date:~8, 2%
set tdy=%2
call echo "Today is %tdy%"
git add Data/"CDC_Press List.xlsx"
git add Data/"COVID-19_TW.xlsx"
git commit -m "Update CDC Press and COVID-19 Statistic on %tdy%"
git push -u origin master
