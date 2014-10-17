# README #

ceca_pass is an standalone app that keeps passwords centralized, encrypted in a database that you provide.
At the same time gives tools to dump the passwords in files that can be accessed by different apps.

The steps to use it are:
 - Install the app
 - Load the required passwords via admin
 - Dump the passwords in a file
 - Use the passwords with your apps.



### Installation ###
```#!bash
pip install -e git+https://rodrigocarreras@bitbucket.org/rodrigocarreras/ceca_pass.git#egg=ceca_pass
```

ceca_pass provides an admin interface (thanks to django) that allows you to load your passwords very easily.

After you installed ceca_pass create a django app:
```#!bash
django-admin startproject ceca_pass_app
```

Edit the file **settings.py** and add **'ceca_pass'** into the installed apps.
Then run:
```#!bash
python manage.py migrate
python manage.py runserver localhost:8000
```

If you access to http://localhost:8000 you can see the admin that allows you to load the passwords.


### Accessing to passwords ###
If you need to consume the passwords that you had load there are two ways to do it.

####1) Via ceca_pass api
You can dump all your passwords into an encrypted file and later access via ceca_pass.

Run:
```#!bash
export DJANGO_SETTINGS_MODULE=ceca_pass_app.settings; ceca_pass_dump_to_json
```

In your python app:
```#!python
>> from ceca_pass.helpers import get_password
>> print get_password('project_name', 'password_name')
>> 'my password'
```

####2) Access via enviroment variable:
This is accomplished by to steps:
 - Creating a bash file with all the passwords.
 - Importing this new file into your local **.bashrc**

```#!bash
# Create your new bash file
export DJANGO_SETTINGS_MODULE=ceca_pass_app.settings; ceca_pass_dump_to_bash

# Link the two bash files
export DJANGO_SETTINGS_MODULE=ceca_pass_app.settings; ceca_pass_patch_bash
```

After that you can access to the passwords doing:

**In Bash**
```#!bash
echo $PROJECT_NAME_VAR_NAME
```
**In python**
```#!python
>> import os
>> os.environ['PROJECT_NAME_VAR_NAME']
```



### Setting Variables ###
```#!python
"A secret string that is used to encrypt the passwords. It has to have a length of 32."
CECA_PASS_SECRET_STRING = '123456789012345678901234567890'

"The path where we want to save our password file (in case we use access via api).
By default its $HOME/.ceca_pass/dump.json"
CECA_PASS_PASSWORD_PATH = ''

"The path where we want to save our bash file with passwords (in case we use access via enviroment variable).
By default its $HOME/.ceca_pass/.bashrc"
CECA_PASS_BASH_PATH = ''

"The path of your bashrc file.
By default its $HOME/.bashrc"
CECA_PASS_SYSTEM_BASH_FILE = os.path.join(BASE_DIR, 'ceca_pass', 'tests',
    'mybash.rc')
```

The software comes without warranty of any kind, so use at your own risk.
