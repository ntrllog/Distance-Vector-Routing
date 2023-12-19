# Project Overview

This Python project implements a robust routing protocol over a network of servers acting as routers. It's designed to adapt dynamically to changes in the network topology and link costs.

## Dependencies

- **Python Version:** At least Python 3.11.x

## How to Install Dependencies

- **Windows/Mac:**
  - Download and install Python 3.11 from [Python Downloads](https://www.python.org/downloads/).
- **Linux:**
  - Use the command `sudo [apt] install python3.11`. Replace `[apt]` with the package manager for your Linux variant.

## Getting Started

### Creating Topology Files

Before running the program, create a topology file for each server. This file should only include the link cost to the server's immediate neighbors. The program determines its own host ID and IP port by scanning through the neighbors' link cost list.

### Topology File Example

![Topology File Example](https://i.imgur.com/efbem4Q.png)

## Running the Program

1. **Run the Script:** Execute `distance_vector_routing.py` in your terminal.
2. **Start the Server:** Use the command `server -t <topology-file-name> -i <routing-update-interval>`.
   - Example: `server -t topology-1.txt -i 3`
3. **Further Instructions:** Additional launch instructions are provided during run-time.

## Available Commands

Type `help` in the terminal to see all available commands. These commands allow you to manage the network effectively.

- `update <server-ID1> <server-ID2> <Link Cost>`: Update the link cost between two servers.
  - Example: `update 1 2 inf` sets the link between servers 1 and 2 to infinity.
  - Example: `update 1 2 8` changes the link cost between servers 1 and 2 to 8.
- `step`: Send a routing update to neighbors immediately.
- `packets`: Display the number of distance vector packets the server has received since the last check.
- `display`: Show the current routing table in a sorted order. The format for each line is `<destination-server-ID> <next-hop-server-ID> <cost-of-path>`.
- `disable <server-ID>`: Disable the link to a specific server.
- `crash`: Simulate a server crash by closing all connections, setting the link cost to infinity.

## More Information

<<<<<<< HEAD
For detailed project information, setup guidelines, and advanced features, please refer to the accompanying [Assignment.pdf](https://github.com/ntrllog/Distance-Vector-Routing/blob/main/Assignment.pdf).
=======
For detailed project information, setup guidelines, and advanced features, please refer to the accompanying [Project Detail PDF](Link to PDF).

## Contact

For queries, please contact [Project Maintainer or Team Contact](Contact Link or Email).
>>>>>>> 3f54e8999c70ec39b2e25e85d6634f5bfffd9bc2
