# whatsapper

Send automatic messages via WhatsApp Web. The first time you run Whatsapper you will need to log in manually but only the first time.

# Installation.

## Ubuntu/Debian
`sudo python3 pip install git+https://github.com/Atlantox/whatsapper`

## Windows
`pip install git+https://github.com/Atlantox/whatsapper`

## After intalation, install the browsers
Whatsapper only uses chromium, firefox and microsoft edge, always using by default chromium

### Install both browsers
`playwright install chromium firefox msedge`



# Getting Started

<pre>
import asyncio
from whatsapper import Whatsapper

# ('contact name', 'message')
messages = [
    ('John Doe', 'My firsts',),
    ('John Doe', 'Messages',),
    ('Jessica Jhonson', 'Using',),
    ('Louis Perez', 'Whatsapper',),
]

wsapper = Whatsapper()
asyncio.run(wsapper.SendMessages(messages)) # Open with chromium
asyncio.run(wsapper.SendMessages(messages), 'firefox') # Open with firefox
asyncio.run(wsapper.SendMessages(messages), 'edge') # Open with edge
</pre>
