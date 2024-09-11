## Steps to install KU-polls
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

5. Install dependencies
```
pip install -r requirements.txt
```

6. Set up environment variables
```
echo "DEBUG=False" >> .env
```
```
echo "SECRET_KEY=your_secret_key_here" >> .env
```
```
echo "TIME_ZONE=Asia/Bangkok" >> .env
```
```
echo "ALLOWED_HOSTS=localhost,127.0.0.1,::1" >> .env
```

7. Apply migration and load data

```
python manage.py migrate
```
```
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

8. Run the test
   
```
python manage.py test tests
```
