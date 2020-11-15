# **python環境構築**

## **mac本体に直接設定するもの**
まずはhomebrew（macのパッケージ管理）をインストールします。

homebrewをインストール
```    
home/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
python(3.8以上)をインストール
```    
brew install python
```
pipenv（pythonのライブラリ管理）をインストール
```
brew install pipenv
```
## **仮想環境を作る**
このディレクトリ内で同じ環境が適用されます。
```
mkdir X
cd X
```
仮想環境を作る
```    
pipenv install
```
使うpythonのバージョンを指定
```    
pipenv --python 3.8
```
必要なパッケージをインストール
```
pipenv install {library}
pipenv install --dev {library}
```
(参考)django系
- django:フルスタックフレームワーク
- djangorestframework:restAPIフレームワーク
- django-filter:検索機能
- django-environ:環境操作
- django-cors-headers:CORS対応
- drf-nested-routers:ネストされたURLの構築


(参考)開発補助
- flake8:コーディング規約 
- autopep8:フォーマッタ

(参考)その他有名どころ
- 配列計算等の高速演算：numpy,pandas 
- 機械学習・ディープラーニング：scikit-learn,tensor-flow,pytorch

インストールしたパッケージ環境をアクティベートする
```
pipenv shell
exitで終了
```    
# **プロジェクトの作成**
仮想環境をアクティベート（pipenv shell）した上で
```
django-admin startproject {your_project_name}
cd ./{your_project_name}
```
- {your_project_name}：フレームワークの共通ディレクトリ
- `manage.py`：startapp,migrateのような管理コマンドが入っています。
- `pipenv run [script]`に`manage.py`のコマンドをラップしておくと楽です。(pipfileに記載)

## **共通ディレクトリの作成**
APIをはじめにひとつ作成するとき、rest_frameworkの共通ディレクトリが作成されます。    
まずは先ほど構築したディレクトリで仮想環境をアクティベート  
```
pipenv shell
```

## **startappコマンド**
アプリ追加コマンドを叩きます。

```
python manage.py startapp {your_app_name} 
```
- このリポジトリではappの作成されるディレクトリと作成されるファイルをカスタマイズしています。
- {your_app_name}：API本体を構築していくディレクトリになります。
- 共通ディレクトリがすでに存在している場合は、APPディレクトリのみ作成されます。
- APIを新規に追加する場合はこのコマンドで他のAPIと並列構成になるように追加します。
- はじめはプロジェクトの開発者（スーパーユーザー）を管理するAPPを作成するとスムーズかと思います。

## **スーパーユーザー用のmodel作成**  
テーブル,カラムを定義していきます。

`{your_app_name}/models.py`
```
class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()
```

## **共通ディレクトリの設定にアプリ名を加えておきます**
INSTALLED_APPSの最下行に追加  
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

## **DBのマイグレーションを行います**
これによりテーブルが作成されます。
```
python manage.py makemigrations
python manage.py migrate
```  

## **スーパーユーザーを作成しておきます**
```
python manage.py createsuperuser
```
下記が順に聞かれますのでそのまま入力していきます。
```
Username (leave blank to use 'dev'): dev
Email address:
Password:
Password (again):
Superuser created successfully.
```

## **スーパーユーザーを登録しておきます。**
`{your_app_name}/admin.py`
```
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
```

## **開発サーバーを起動**
```
pipenv run start
```
- vscodeならデバッグスタートの方が楽です。
- ctrl+Cで終了
- localhost:8000:djangoの動作確認
- localhost:8000/admin/:管理画面に入れる

ここまででdjangoのスーパーユーザー設定が完了となります。

# **djangoアプリ(API)の追加手順**

## **startappコマンド**  
アプリ追加コマンドを叩きます。  
```
python manage.py startapp {your_app_name} 
```  
- {your_app_name}：API本体を構築していくディレクトリになります。
- APIを新規に追加する場合はこのコマンドで他のAPIと並列構成になるように追加します。
- 共通ディレクトリがすでに存在しているはずなので、APPディレクトリのみ作成されます。
   
## **settingの編集**  
共通ディレクトリの設定にアプリ名を加えておきます。  
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

## **modelの定義**  
テーブル,カラムを定義を行います。  
`{your_app_name}/models.py`  
```
class User(models.Model):
    name = models.CharField(max_length=32)
    mail = models.EmailField()
```

## **serializerの定義**
・リクエストの加工
・リクエストのバリデーション
・レスポンスの加工
`{your_app_name}/serializer.py`  
```
from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'mail')
```

## **viewsetの定義**
・リクエストの受け取り
・リクエストへのシリアライザ適用
・モデルへのCRUD司令
・レスポンスの返却  
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

## **urlsの定義**  
いわゆるルーティングを書きます。  
共通ディレクトリ側にはAPPディレクトリの`urls.py`を追加します。  
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
APPディレクトリ側にはそれぞれのViewSetのルーティングを追加します。  
`{your_app_name}/urls.py`  
```
from rest_framework import routers
from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
```
- このプロジェクトのrouterはカスタマイズされています。
- `extends`メソッドでappディレクトリで登録されているルーティング情報を引き継ぎます。

## **admin.pyについて**
djangoの管理画面にモデルを表示させるために登録します。
```
from django.contrib import admin
from .models import Partitipant

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass
```

## **動作確認**
```
pipenv run start
```
- roomエントリ：http://localhost:8000/api/rooms/

## (参考)Postgresの使い方
スーパーユーザーでログイン
```
psql -U postgres
```
ユーザーを作成
```
CREATE ROLE admin WITH LOGIN PASSWORD 'jsms';
ALTER ROLE admin WITH option [SUPERUSER];

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA jsms TO admin;
```
ロールとデータベースを指定してログイン
```
psql -U admin -d jsms
```
brewサービス起動
```
brew services start postgresql
```
brewサービス停止
```
brew services stop postgresql
```
ユーザーパスワードを変更
```
ALTER USER jsms with unencrypted password 'jsms';
```
# 残課題
 - dockerは必要かどうか（dockerファイル書いておけば環境構築簡単そうな気がする）
 - デプロイ方法（CIはどうする？）
 - AWSの使い方,EC2（ファイル置き場）,lambda,RDS（DBはEC2に置かないでここにおく）

