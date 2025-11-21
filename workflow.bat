.\.venv\Scripts\python.exe opencc_s2t.py -i global_chs.ini -o global.ini -m s2twp
.\.venv\Scripts\python.exe term_replace.py -i global.ini -o global.ini -v
powershell -Command "$existing = Get-Content global.ini -Encoding UTF8; $append = Get-Content coded_traditional.ini -Encoding UTF8; ($existing + $append) | Set-Content global.ini -Encoding UTF8"
