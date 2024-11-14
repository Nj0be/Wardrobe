FROM python:3.12.4

EXPOSE 8000
WORKDIR /app

# installing node
ARG NODE_MAJOR=22

RUN apt-get update
RUN apt-get install -y ca-certificates curl gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update
RUN apt-get install nodejs -y
RUN rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man
RUN apt-get clean

# installing python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

