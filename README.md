# ANANSI WAGTAIL CMS built locally and deployed using Docker.

## A content management system built using wagtail CMS (django backend) and styled using Tailwind CSS (js frontend).

This project depicts a content management system built using django and Tailwind CSS. This project shows you how to:

* Create a custom CMS with django using Wagtail
* Style it using Tailwind CSS
* Containerize it automatically using Docker for local use and for deployment.

To get started:
1. Clone the repository
    `git clone <anansi_project>`
2. Change the directory
    `cd <anansi_project>`
3. Install Python
    `$ brew install python`
3. Install Docker
    `$ sudo hdiutil attach Docker .dmg`
    `$ sudo /Volumes/Docker/Docker .app/Contents/MacOS/install`
    `$ sudo hdiutil detach /Volumes/Docker`
4. Install the virtualenv libary using pip
    `$ pip install virtualenv`
5. Create your virtual environment
    `$ virtualenv venv`
6. Enter the virtual environment
    `$ source venv/bin/activate`
7. Install the dependencies and requirements in the current environment
    `$ pip install -r 'requirements.txt'`
8. Use Docker to build your image
    `$ docker-compose up -d --build`
9. Run the docker image
    `$ docker-compose logs -f`
10. Access the cms using your local host
    `https:localhost`