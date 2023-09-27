# Setting Up and Running the Lokatir Bot


## Installation


### Prerequisites

 Update the package list:

```bash
sudo apt update
```
      
 Clone this repository:

```bash
git clone https://github.com/OleksandrYanchar/Vacancies-Parser-Bot
```
### Set up a virtual environment:

```bash
python3 -m venv venv
```

 Activate the virtual environment:
    
```bash
source venv/bin/activate
```
 Install required Python packages:

```bash
pip3 install -r requirements.txt
```
### Usage 

### Here you have 2 choices:

```bash
python3 main.py
```
for polling bot all time

```bash
celery -A my_schedule  worker --loglevel=info
```
for polling one time per day