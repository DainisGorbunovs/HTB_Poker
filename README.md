# HTB_Poker
Devpost: [Schnitzel Pokerman](https://devpost.com/software/schnitzel-pokerman)

Hack The Burgh 2019: Poker game Squarepoint.

Created by:
* [Dainis Gorbunovs](https://github.com/DainisGorbunovs) - [LinkedIn](https://www.linkedin.com/in/dainisgorbunovs/)
* [Valentine Dragan](https://github.com/ValntinDragan) - [LinkedIn](https://www.linkedin.com/in/valentinadriandragan/)
* [Ilja Tscharikow](https://github.com/Ilja2307) - [LinkedIn](https://www.linkedin.com/in/ilja-tscharikow/)
* [Minh Tri Pham](https://github.com/MinhTri-Pham)

## Create, and use the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Alternatively in Windows:
```bash
.\venv\Script\activate.bat
```


Set Python (from venv) as the default interpreter:
1. Preferences... / Settings
2. Project Interpreter
3. Add a new Virtual Env environment.
4. Add `htb-poker/venv/bin/python`
 

## Log all the games
Save the games into `games` directory by using `log_game` argument:
```python
TransactionClient(log_game=True)
```

