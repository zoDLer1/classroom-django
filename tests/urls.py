from django.urls import path, include
from .views import *
urlpatterns = [
    path('create/', ViewCreateTest.as_view(), name='create_test'),
    path('template/<int:id>', ViewTest.as_view(), name='view_test'),
    path('template/<int:id>/add', AddToCLass.as_view(), name='add_to_class'),
    path('template/<int:id>/delete', DeleteTest.as_view(), name='delete_test'),
    path('<int:tfc_id>', ViewTestForClass.as_view(), name='test_for_class'),
    path('<int:tfc_id>/pass', PassTestForClasses.as_view(), name='pass_test'),
    path('passed/<int:pt_id>', ViewPassedTest.as_view(), name='passed_test')
]