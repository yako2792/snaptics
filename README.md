# PHOTO SCANNER V2

Next version of the old photo scanner software, but now with several upgrades.

## 1. How to run

1. Create a virtual environment as a hidden folder.

```bash
$ python -m virtualenv .venv
```

2. Once the venv is created, activate it.

```bash
$ source .venv/bin/activate
```

3. Once the venv is activated, install dependencies.

```bash
(.env) $ pip install -r requirements.txt
```

4. Run the project.

```bash
(.env) $ python -m src.main
```

### 1.1 Run As Desktop

```bash
(.env) $ flet run -m src.main
```

### 1.2 Run As Web

```bash
(.env) $ flet run --web -a resources/assets -m src.main
```

## 2. Project Structure

```text
snaptics
├─ requirements.txt
├─ README.md
└─ src
   ├─ main.py
   ├─ resources
   │  ├─ properties.py
   │  ├─ controls
   │  │  ├─ explorer_control.py
   │  │  └─ workspace_control.py
   │  │
   │  └─ utils
   │     └─ layout.py
   └─ storage
      ├─ data
      └─ temp
```
