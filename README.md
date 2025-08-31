# Start project locally

- docker-compose up

Manually change
- for development:
  - in docker-compose.yml change:
    - frontend service:
      - the dockerfile to Dockerfiledev

- for production-ready:
  - in docker-compose.yml change:
    - frontend service:
      - the dockerfile to Dockerfile
     
Add secrets folder in the root and populate with the passwords/keys.
