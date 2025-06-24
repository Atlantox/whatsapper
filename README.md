# whatsapper

Send automatic messages via WhatsApp Web. The first time you run Whatsapper you will need to log in manually but only the first time.

# Installation.

## Ubuntu/Debian
`sudo python3 pip install git+https://github.com/Atlantox/whatsapper`

## Windows
`pip install git+https://github.com/Atlantox/whatsapper`


# Getting Started

<pre>
python
from whatsapper import Whatsapper

# ('contact name', 'message')
messages = [
    ('John Doe', 'My firsts',),
    ('John Doe', 'Messages',),
    ('Jessica Jhonson', 'Using',),
    ('Louis Perez', 'Whatsapper',),
]

wsapper = Whatsapper()

await wsapper.SendMessages(messages)
</pre>
