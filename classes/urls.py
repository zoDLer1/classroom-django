from unicodedata import name
from django.urls import path, include
from .views import *


urlpatterns = [
    path('create/', ClassAdd.as_view(), name='createClass'),
    path('<int:id>', ViewClass.as_view(), name='class'),
    path('invite/<code>', ViewInvite.as_view(), name='invite'),
    path('<int:class_id>/accept/<int:user_id>', ViewJoin.as_view(), name='join'),
    path('<int:class_id>/reject/<int:user_id>', ViewReject.as_view(), name='reject'),
    path('<int:class_id>/delete', DeleteCLass.as_view(),  name='delete_class'),
    path('<int:class_id>/except/<int:user_id>', ExceptMember.as_view(), name='except'),
    path('<int:id>/refresh-invite', RefreshInvite.as_view(), name='refresh-invite'),
    path('<int:id>/leave', ClassLeave.as_view(), name='leave')
]