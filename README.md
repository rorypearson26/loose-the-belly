# Weight tracking slack app / bot
Slack bot that can take weight measurements, store in a database, and then regurgitate a nice graph using parsed commands.

SocketMode API was undergoing changes when first developed so couldn't use slash commands. The docs seem to support them now so can probably implement better using them as opposed to listening out for certain words.

List of commands:
- add
- readcsv
- deletelast
- plt

All commands are case-insensitive but should should be followed by a single space to ensure proper parsing of arguments.
