# KU-Polls : Online survey web application
## Description
The web application for conducting surveys and polls executively for authorized people in Kasetsart University. This project has some parts of [Django tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/). This project mainly aims for event organizer to ask about feedbacks from events that hold in the university.

## Documents
* [Project Wiki](../../wiki/Home)
* [Requirements](../../wiki/Requirements)
* [Vision and Scope](../../wiki/Vision-and-Scope)
* [Project Plan](../../wiki/Project-Plan)
* [Installation](../../wiki/Installation)

## Progress
* [Domain Model](../../wiki/Domain_Model)
* [Iteration 1](../../wiki/Iteration_1)
* [Iteration 2](../../wiki/Iteration_2)
* [Iteration 3](../../wiki/Iteration_3)

## Requirements and Installation
## Run these commands respectively
1. Clone github repository
```
git clone https://github.com/Thanawas-Sirilertsathit/ku-polls.git
```
2. Change directory to ku-polls
```
cd ku-polls
```
3. Create Virtual Environment
```
python -m venv env
```
4. Activate Virtual Environment
```
env\Scripts\activate # For Window
```
```
source env/bin/activate # For MacOS and Linux
```
5. Install required modules
```
pip install -r requirements.txt
```
6. Apply config

Create a file called ``.env.production`` then copy format of ``sample.env`` and put information into ``.env``

7. Run the server
```
python manage.py migrate
```
```
python manage.py loaddata data/polls-v3.json
```
```
python manage.py loaddata data/users.json
```
```
python manage.py runserver
```
