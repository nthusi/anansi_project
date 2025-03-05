# ANANSI WAGTAIL CMS built locally and deployed using Docker.

## A content management system built using wagtail CMS (django backend) and styled using Tailwind CSS (js frontend).

This project depicts a content management system built using django and Tailwind CSS. This project shows you how to:

* Create a custom CMS with django using Wagtail
* Style it using Tailwind CSS
* Containerize it automatically using Docker for local use and for deployment.

LOCAL HOSTING
To get started [backend]:
1. Clone the repository
    `git clone <anansi_project>`
2. Change the directory
    `cd <anansi_project>`
3. Install Python
    `$ brew install python`
4. Install the virtualenv libary using pip
    `$ pip install virtualenv`
5. Create your virtual environment
    `$ virtualenv venv`
6. Enter the virtual environment
    `$ source venv/bin/activate`
7. Install the dependencies and requirements in the current environment
    `$ pip install -r 'requirements.txt'`
8. Use django to set up migrations
    `$ python manage.py makemigrations`
    `$ python manage.py migrate`
9. Create super user using django
    `$ python manage.py createsuperuser`
10. Run the django project locally
    `$ python manage.py run server`

To get started [frontend]:
1. Download and install nvm
    `$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh`
2. Start the shell
    `$ \. "$HOME/.nvm/nvm.sh"`
3. Download and install nvm
    `$ nvm install 22`
4. Verify the Node.js version
    `$ node -v`
    `$ nvm current`
5. Verify the npm version
    `$ npm -v`
6. Run npm to install depencies
    `$ npm install`
7. Start npm on node 9091
    `$ npm run start`
    
