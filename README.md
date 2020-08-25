# Chat

The proggram is split into client, server and database.
Server accept clients and allows them to connect with each_other.
All clients see messages from all clients.
Also the server solves data in database.

Client implemented using sockets.
Server implemented using asyncio.
Database is simple text file.

Language of project is Python.

What else can one implement:
  - Client can send messeges to a certain person.
  
What error:
  - Exit with Ctrl + C.
  - Database keeps a bunch of empty messeges if one client exit.
