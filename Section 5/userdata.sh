#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y python-pip python-dev build-essential
pip install --upgrade pip
sudo pip install django requests boto3 django-bootstrap3 pillow
django-admin.py startproject s3pythonapp
