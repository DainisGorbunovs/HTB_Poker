# HTB_Poker
Hack The Burgh 2019: Poker game Squarepoint

## Create, and use the virtual environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set Python (from venv) as the default interpreter:
1. Preferences...
2. Project Interpreter
3. Add `htb-poker/venv/bin/python`
 

## Log all the games
Save the games into `games` directory by using `log_game` argument:
```python
TransactionClient(log_game=True)
```

