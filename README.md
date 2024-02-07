# Distributed URL Shortener System using Docker, Cassandra, and Redis

## Overview

This project implements a distributed URL shortener system inspired by <a href="bit.ly">bit.ly</a>. It leverages Docker containers for easy deployment and management, Cassandra for storing URL mappings, and Redis for caching frequently accessed URLs.

## Features

- **URL Shortening:** Users can generate short URLs for long web addresses.
- **Distributed Architecture:** The system is designed to handle high traffic and scalability using distributed technologies.
- **Caching:** Redis is used to cache frequently accessed URLs, improving response times.
- **Dockerized Deployment:** The system is containerized using Docker, enabling easy deployment and scaling across different environments.

## Technologies Used

- **Docker:** Docker containers are used to encapsulate and deploy various components of the system.
- **Cassandra:** Cassandra is used as the distributed database to store URL mappings efficiently.
- **Redis:** Redis acts as a caching layer to optimize the retrieval of URLs.
- **Python/Flask:** The backend server is implemented using Python and Flask, providing an HTTP interface for URL shortening operations.

## Deployment

To deploy the system locally or in a production environment, ensure Docker is installed on your system. Then, follow the deployment instructions provided in the project's documentation.

## Getting Started

To get started with the system, clone the repository and follow the setup instructions in the `README.md` file. Make sure you have Docker, Cassandra, and Redis installed and configured correctly.

## Usage
To use without docker swarm:
```bash
./autostart.sh [IP1] [IP2] [IP3] ...
```
To use with docker swarm:
```bash
./fastautostart.sh [IP1] [IP2] [IP3] ...
```
