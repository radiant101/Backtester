"""
URL configuration for tradingstrategy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backtest.views import index
from backtest.views import strategy
from backtest.views import results
from backtest.views import news
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('strategy/',strategy,name='strategy'),
    path('results/',results, name='results'),
    path('news/',news,name='news'),

]
