# Countdown Widget

A minimal Linux desktop countdown widget built for my purpose of **personal accountability**.

## Why I made it

I wanted a lightweight countdown that always stayed visible while I worked. Existing timer applications had more features than I needed, so I built a simple widget that fit my workflow.

## Notes

* Built with assistance from ChatGPT.
* Created a desktop launcher/shortcut so the widget can be started with a single click.
   
* Added:

  * Always-on-top transparent widget
  * Drag button to reposition
  * Exit button
  * Compact layout with several size adjustments
* Experimented with resizing and simplifying the interface to occupy minimal screen space.

## Current Features

* Transparent frameless window
* Always-on-top
* Countdown timer
* Click to edit remaining time
* Hover controls
* Drag to move
* Desktop notifications on completion
* Progress indicator
* Color changes based on remaining time

## Purpose

This is a small utility project built for daily use rather than as a production-ready application. The focus was solving a personal problem quickly with minimal complexity.



## Requirements

* Python 3.8 or newer
* PyQt5

Install PyQt5:

```bash
pip install PyQt5
```

## Running

```bash
python3 countdown.py
```

---

# Linux

### Install Python

Most Linux distributions already include Python 3.

Verify:

```bash
python3 --version
```

Install PyQt5:

```bash
pip3 install PyQt5
```

Run:

```bash
python3 countdown.py
```

For desktop launching, create a `.desktop` launcher or use your desktop environment's launcher editor.

---

# Windows

Install:

* Python 3
* PyQt5

```powershell
pip install PyQt5
```

Run:

```powershell
python countdown.py
```

To launch with one click:

* Right-click → **Create Shortcut**
* Move the shortcut to the Desktop or Start Menu.

Optional: package into a standalone executable:

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed countdown.py
```

---

# macOS

Install Python (if needed):

```bash
brew install python
```

Install PyQt5:

```bash
pip3 install PyQt5
```

Run:

```bash
python3 countdown.py
```

For quick launching:

* Save the script in a folder.
* Create an Automator Application or use Shortcuts to launch it.
* Pin it to the Dock if desired.

---

Everything is contained in a single `countdown.py` file, making customization straightforward.
