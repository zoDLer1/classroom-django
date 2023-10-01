from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
# from django.contrib.auth.decorators import login_required
# from classes.models import Class, Member
# from tests.models import PassedTest, Test, TestForClass
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request,'main/index.html')


class Home(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        self.roles = [
            {'id':1, 'func':self.is_Teacher},
            {'id':2, 'func':self.is_Student}
        ]
        super().__init__(**kwargs)
        
    def get(self, request):
        if request.user.is_authenticated:
            for role in self.roles:
                if role['id'] == request.user.role.id:
                    return role['func'](request)
        return redirect('login')
    
    def is_Student(self, request):
        memb = request.user.Members()
        
        tests = []
        passed_tests = []
        for test_arr in [m.current_class.Tests() for m in memb]:
            for test in test_arr:
                passed_test = test.ExistsInPassedTest()
                if not passed_test:
                    tests.append(test)
                else:
                    passed_tests.append(passed_test)
                    
        return render(request, 'main/student_home.html', context={'tests':tests, 'passed_tests':passed_tests, "members":memb})
    
    def is_Teacher(self, request):
        classes = request.user.Classes()
        tests = request.user.Tests()
        
        return render(request, 'main/home.html', context={'classes':classes, 'tests':tests})
