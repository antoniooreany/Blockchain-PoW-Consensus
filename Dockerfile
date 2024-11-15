### Use an official Python runtime as a parent image
##FROM python:3.9-slim
##
### Set the working directory in the container
##WORKDIR /app
##
### Copy the current directory contents into the container at /app
##COPY . /app
##
### Set the PYTHONPATH environment variable
##ENV PYTHONPATH=/app
##
### Install any needed packages specified in requirements.txt
##RUN pip install --no-cache-dir -r requirements.txt
##
### Make port 80 available to the world outside this container
##EXPOSE 80
##
### Define environment variable
##ENV NAME World
##
### Run main.py when the container launches
##CMD ["python", "src/main.py"]
#
## Use an official Python runtime as a parent image
#FROM python:3.9-slim
#
## Install tkinter dependencies
#RUN apt-get update && apt-get install -y \
#    python3-tk \
#    libglib2.0-0 \
#    libgl1-mesa-glx \
#    && rm -rf /var/lib/apt/lists/*
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the current directory contents into the container at /app
#COPY . /app
#
## Set the PYTHONPATH environment variable
#ENV PYTHONPATH=/app
#
## Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
#
## Make port 80 available to the world outside this container
#EXPOSE 80
#
## Define environment variable
#ENV NAME World
#
## Run main.py when the container launches
#CMD ["python", "src/main.py"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install tkinter and xvfb dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    libglib2.0-0 \
    libgl1-mesa-glx \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py with xvfb when the container launches
CMD ["xvfb-run", "python", "src/main.py"]



