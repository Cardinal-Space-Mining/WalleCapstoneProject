# Walle Capstone Project
This is a backup of the walle capstone project code written by Gavin Andres for the club sponsored outreach project. The ME's working on the project didn't have backups anywhere so I am doing this here.

## Setup
1. Clone the repo using git (`git clone https://github.com/Cardinal-Space-Mining/WalleCapstoneProject.git`)

2. Make sure python virtual environment support is installed. (`sudo apt install python3-venv`)

3. Create virtual environment (`python3 -m venv .venv`)

4. Activate virtual environment (`source ./.venv/bin/activate`)

5. Install necessary libraries (`pip3 install -r ./requirements.txt`)

## Running
1. Source venv (`source ./.venv/bin/activate`)

2. Run code `(python3 ./walle/walle.py`)

## Auto-Running
It is meant to be run on a Rasbery PI. An easy way to set that up is to disable RPI signin, and call the main file from `~/.bashrc`

In this case, the code is as follows:
```bash
WalleDir='/home/pi/WalleCapstoneProject'
${WalleDir}/.venv/bin/python3 ${WalleDir}/walle/walle_new.py
```

Just paste it at the end of your `~/.bashrc` changing `WalleDir` to be the absolute path to the cloned repo. Note, the setup instructions must be completed first.