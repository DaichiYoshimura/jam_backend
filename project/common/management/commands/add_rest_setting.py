import sys,os
from django.core.management.base import BaseCommand,CommandError
import re

class Command(BaseCommand):
    help='add files and settings for django_rest_framework'

    def add_arguments(self, parser):
        parser.add_argument('app_name', nargs='+', type=str)

    def handle(self,*args,**options):
        if not options['app_name']:
            print("引数に追加したapp名を入力してください。")
            sys.exit(1) 
        
        for app_name in options['app_name']:
            
            ps_app_name = self.__ps(app_name)

            if os.path.exists(app_name+'/serializer.py'):
                print("すでにserializer.pyが存在しています。")
                sys.exit(1)   
            with open(app_name+'/serializer.py','w') as f:
                s = "from rest_framework import serializers\n"\
                +"from .models import "+ps_app_name+"\n\n\n"\
                +"class "+ps_app_name+"Serializer(serializers.ModelSerializer):\n\n\n"\
                +"  class Meta:\n"\
                +"      model = "+ps_app_name+"\n"\
                +"      ##please add fields = () here after define models."
                f.write(s)

            if os.path.exists(app_name+'/urls.py'):
                print("すでにurls.pyが存在しています。")
                sys.exit(1)   
            with open(app_name+'/urls.py','w') as f:
                s = "from rest_framework import routers\n"\
                +"from .views import "+ps_app_name+"ViewSet"+"\n\n\n"\
                +"router = routers.DefaultRouter()"+"\n"\
                +"router.register(r'"+app_name+"', "+ps_app_name+"ViewSet)"+"\n"
                f.write(s)

    def __ps(self,arg):
        return re.sub("_(.)",lambda x:x.group(1).upper(),arg).capitalize()