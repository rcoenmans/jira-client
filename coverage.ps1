$env:PYTHONPATH=".\"

Start-Process coverage -ArgumentList "run", ".\tests\test_jiraclient.py" -NoNewWindow -Wait
Start-Process coverage -ArgumentList "report", "-m" -NoNewWindow -Wait