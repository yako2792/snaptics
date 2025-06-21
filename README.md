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
(.env) $ flet run --port 8000 --web -a resources/assets -m src.main
```

## 2. Project Structure

```text
snaptics
├── README.md
├── requirements.txt
└── src
    ├── camera_controller.py
    ├── main.py
    ├── motor_controller.py
    ├── resources
    │   ├── assets
    │   │   ├── camera_values.json
    │   │   ├── icons
    │   │   │   ├── favicon.png
    │   │   │   └── loading-animation.gif
    │   │   ├── images
    │   │   │   ├── captures
    │   │   │   │   ├── camera_1
    │   │   │   │   ├── camera_2
    │   │   │   │   └── camera_3
    │   │   │   ├── example_01.png
    │   │   │   ├── filtered_images
    │   │   │   ├── gifs
    │   │   │   │   └── loading.gif
    │   │   │   └── view_test
    │   │   ├── presets
    │   │   │   └── presets.json
    │   │   └── routines
    │   │       └── routines.json
    │   ├── controls
    │   │   ├── custom
    │   │   │   ├── header_control.py
    │   │   │   ├── image_viewer_control.py
    │   │   │   ├── loading_dialog.py
    │   │   │   ├── options_control.py
    │   │   │   ├── preset_control.py
    │   │   │   ├── progress_bar.py
    │   │   │   ├── stages
    │   │   │   │   ├── stage_filter.py
    │   │   │   │   ├── stage_save.py
    │   │   │   │   └── stage_scan.py
    │   │   │   └── use_control.py
    │   │   ├── explorer_control.py
    │   │   ├── filters
    │   │   │   └── filters.py
    │   │   ├── tabs
    │   │   │   ├── preview_tab_control.py
    │   │   │   ├── properties_tab_control.py
    │   │   │   ├── routines_tab_control.py
    │   │   │   └── scan_tab_control.py
    │   │   └── workspace_control.py
    │   ├── properties.py
    │   └── utils
    │       ├── layout.py
    │       ├── __pycache__
    │       │   ├── layout.cpython-311.pyc
    │       │   └── routines_controller.cpython-311.pyc
    │       └── routines_controller.py
    └── storage
        ├── data
        └── temp
```

## 3.3 Enhancements

- [x] Credentials manager using dotenv
- [x] Stage padding
- [x] Code product on scan stage 
- [x] Save card dynamic server options 
- [x] Letter code for different capture degrees
- [x] Save images via lftp logic
- [x] Image listing under cameras
- [x] Image preview in tab tab
- [x] After a Save stage take og images*
- [x] Directory with product id before saving images
- [x] Image crop filter

# Auto Start on Raspberry Pi

1. Create an executable `start.sh` file.

```bash
#!/bin/bash
cd /home/user/Documents/snaptics
source .venv/bin/activate
flet run --port 8000 --web -a resources/assets -m src.main
```

2. Make it executable.

```bash
chmod +x start.sh
```

3. Create a systemd serivce.

Command

```bash 
touch /etc/systemd/system/snaptics.service
```

Content

```service
[Unit]
Description=Snaptics App
After=network.target

[Service]
ExecStart=/home/user/Documents/snaptics/start.sh
WorkingDirectory=/home/user/Documents/snaptics
Restart=always
User=user
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

4. Enable and start the service.

```bash
sudo systemctl daemon-reload
sudo systemctl enable snaptics.service
sudo systemctl start snaptics.service
```

5. Check logs.
```
journalctl -u snaptics.service -f
```