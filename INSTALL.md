# Quick Installation Guide: Making Snapshot a Terminal Command

## What You're Doing

You're making `snapshot` work as a terminal command from anywhere on your computer. The script already has a **shebang** line at the top that tells your system to use Python to run it.

## Step 1: Make the Script Executable

Navigate to where your script is located, then run:

```bash
chmod +x snapshot_v0-1-2.py
```

This tells your system: "This file can be executed as a program"

## Step 2: Copy to Your ~/bin Directory

```bash
cp snapshot_v0-1-2.py ~/bin/snapshot
```

This copies the script to ~/bin and renames it to just `snapshot` (without .py).

**Note:** The shebang line at the top (`#!/usr/bin/env python3`) tells the system to use Python even without the .py extension.

## Step 3: Add ~/bin to Your PATH

Open your shell configuration file:

```bash
nano ~/.zshrc
```

Scroll to the bottom and add this line:

```bash
export PATH="$HOME/bin:$PATH"
```

**What this does:** Tells your system to look in ~/bin when you type a command in terminal.

Save the file: `Ctrl+O` → `Enter` → `Ctrl+X`

## Step 4: Reload Your Configuration

```bash
source ~/.zshrc
```

This loads the changes you just made.

## Step 5: Test It!

From anywhere in your terminal, type:

```bash
snapshot
```

Your script should run!

## What is the Shebang?

The first line of your script is:

```python
#!/usr/bin/env python3
```

This is called a **shebang**. It tells your operating system:
- `#!` = "This is a shebang"
- `/usr/bin/env` = Use the environment to find Python
- `python3` = Run this file with Python 3

Without the shebang, you'd have to type `python3 snapshot` every time. With it, you can just type `snapshot`.

## Troubleshooting

**"Command not found: snapshot"**
- Make sure you ran `source ~/.zshrc`
- Check that the file is in ~/bin: `ls ~/bin/snapshot`
- Verify ~/bin is in PATH: `echo $PATH`

**"Permission denied"**
- Make sure you ran `chmod +x snapshot_v0-1-2.py`

**Script runs but asks for path**
- Everything is working correctly! Just follow the prompts.
