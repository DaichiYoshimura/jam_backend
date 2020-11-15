# **python environment**

## **setting local machine**

install homebrew

```    
home/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

install python(3.8)
```    
brew install python
```
install pipenv
```
brew install pipenv
```
## **create pipenv**

```
mkdir X
cd X
```
create pipenv
```    
pipenv install
```
select version
```    
pipenv --python 3.8
```
install package
```
pipenv install {library}
pipenv install --dev {library}
```
django
- django:framework
- djangorestframework:customize django for rest  
- django-filter:customize django for searching
- django-cors-headers:CORS
- drf-nested-routers:nested url


dev
- flake8:linter 
- autopep8:formatter

activate pipenv
```
pipenv shell
exit
```    
# **create project**

```
pipenv shell
django-admin startproject {your_project_name}
cd ./{your_project_name}
```
- {your_project_name}：common dir of framework
- `manage.py`：manage commands e.g. startapp,migrate
- write  `pipenv run [script]` about commands in `manage.py` in pipfile

## **startapp**
```
pipenv shell
python manage.py startapp {your_app_name} 
```
- {your_app_name}：app dir
- If common dir exists, create app dir only.
- At first, You create an app to manage super user.
## **create model for managing super user**  

define table and column.

`{your_app_name}/models.py`
```
class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()
```

## **write app name in common dir setting**
add {your_app_name} to INSTALLED_APPS  
`{your_project_name}/settings.py`
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{your_app_name}'
]
```

## **migrate DB**
create table
```
python manage.py makemigrations
python manage.py migrate
```  

## **create super user**
```
python manage.py createsuperuser
```
```
Username (leave blank to use 'dev'): dev
Email address:
Password:
Password (again):
Superuser created successfully.
```

## **register super user**
`{your_app_name}/admin.py`
```
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
```

## **run local server**
```
pipenv run start
```
- `ctrl+C` for exit
- localhost:8000:django's root
- localhost:8000/admin/:management console

this is finish for managing super user app.

# **tutorial for django app**

## **startapp**  
add app
```
python manage.py startapp {your_app_name} 
```  
- {your_app_name}：app dir
- If common dir exists, create app dir only.
   
## **setting**  

`python:rest_common/settings.py`  
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    '{your_app_name}'
]
```  

## **model**  
define table and columns
`{your_app_name}/models.py`  
```
class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()
```

## **serializer**
`{your_app_name}/serializer.py`  
```
from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'mail')
```

## **viewset**
`{your_app_name}/views.py`  
```
from rest_framework import viewsets
#from django.shortcuts import render

from .models import User
from .serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

## **urls**  
define rooting.
add `urls.py` for common dir
`rest_common/urls.py`  
``` 
from django.contrib import admin
from django.conf.urls import url, include
from jsms_api.urls import router as jsms_api_router


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(jsms_api_router.urls)),
]
```  
add each ViewSet rooting for add dir
`{your_app_name}/urls.py`  
```
from rest_framework import routers
from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
```
- In this project, the router is customized.

## **about admin.py**

```
from django.contrib import admin
from .models import Partitipant

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass
```

## **start local server**
```
pipenv run start
```
- room：http://localhost:8000/api/rooms/

## how to use Postgres
login super user
```
psql -U postgres
```
create user
```
CREATE ROLE admin WITH LOGIN PASSWORD 'jsms';
ALTER ROLE admin WITH option [SUPERUSER];

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA jsms TO admin;
```
login selecting role and database
```
psql -U admin -d jsms
```
start via brew
```
brew services start postgresql
```
stop via brew
```
brew services stop postgresql
```
alter user password
```
ALTER USER jsms with unencrypted password 'jsms';
```