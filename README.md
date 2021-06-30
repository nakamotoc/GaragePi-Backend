#GaragePi Backend

Serves as a backend web api for the Raspbery Pi garage door opener webapp.

## Setup

Create virtual environment

    python -m virtualenv venv

Switch to virtual environment

    source venv/bin/activate

Install packages

    pip install gpiozero uwsgi

Modify environment variables

    cp .env_example .env
    vi .env


## GPIO Description

| Pin Name | Pin Type | Pin Description |
|-|-|-|
| OPEN_SWITCH | INPUT | A switch to determine whether the garage is in the full open position |
| CLOSED_SWITCH | INPUT | A switch to determine whether the garage is in the foll closed position |
| OPENER_BUTTON | OUTPUT | Activates a relay to "press" the garage door opener |

