from cgi import test
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .forms import TestCreationForm, QuestionCreationForm, AnswerCreationForm
from .models import *
from classes.models import Class
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



class ViewCreateTest(LoginRequiredMixin, View):
    def get(self, request):
        form = TestCreationForm()
        return render(request, 'tests/test_create.html', context={'form':form})
    
    def post(self, request):
        main_data = {'name':request.POST['name'], 'description':request.POST['description'], 'creator':request.user}
        questions_data = [
            {'question':request.POST[question], 
            'answers': [request.POST[answer] for answer in [s for s in request.POST if any(xs in s for xs in [f'answer_{question[question.rfind("_")+1:]}'])]],
            'correct':[int(i) for i in request.POST[f'answers_{question[question.rfind("_")+1:]}'].split(',') if i]
            }
            for question in [s for s in request.POST if any(xs in s for xs in ['question'])]
        ]
    
        form = TestCreationForm(main_data)     
        if form.is_valid():
            test = form.save()
            for question in questions_data:
                qf = QuestionCreationForm({'name':question['question'], 'test':test})
                if qf.is_valid():
                    que = qf.save()
                    for answer_index in range(len(question['answers'])):
                        af = AnswerCreationForm({'value':question['answers'][answer_index], 'right': answer_index+1 in question['correct'],  'question':que})
                        if af.is_valid():
                            af.save()
                            
        return redirect('home')

class ViewTest(LoginRequiredMixin, View):
    def get(self, request, id):
        test = get_object_or_404(Test, id=id, creator__id=request.user.id)
        questions = test.Questions_objs()
        return render(request, 'tests/test_view.html', context={'test':test, 'questions':questions})
    
class AddToCLass(LoginRequiredMixin, View):
    def get(self, request, id):
        test = get_object_or_404(Test, id=id, creator__id=request.user.id)
        classes = request.user.Classes()
        return render(request, 'tests/add_to_class.html', context={'test': test, "classes": classes})
    
    def post(self, request, id):
        class_ = get_object_or_404(Class, id=request.POST['class'], creator__id=request.user.id)
        test =  get_object_or_404(Test, id=id, creator__id=request.user.id)
        if not test.ExistsInTestForClass():
            test_for_class = TestForClass(current_class=class_, test=test)
            test_for_class.save()  
        return redirect('class', id=class_.id)
    
class DeleteTest(LoginRequiredMixin, View):
    def get(self, request, id):
        test = get_object_or_404(Test, id=id, creator__id=request.user.id)
        test.delete()
        return redirect('home')
    
class ViewTestForClass(LoginRequiredMixin, View):
    def get(self, request, tfc_id):
        test_for_class = get_object_or_404(TestForClass, id=tfc_id)
        passed_tests = test_for_class.Passed_Tests()
        return render(request, 'tests/test_info.html', context={'passed_tests':passed_tests})
class ViewPassedTest(LoginRequiredMixin, View):
    def get(self, request, pt_id):
        passed_test = get_object_or_404(PassedTest, id=pt_id)
        test = passed_test.test_for_class.test
        questions = passed_test.Questions_objs()
        isAnswers = passed_test.test_for_class.test.creator.id == request.user.id
        
        return render(request, 'tests/passed_test.html', context={'test':test, 'questions':questions, 'isAnswers':isAnswers})
    
class PassTestForClasses(LoginRequiredMixin, View):
    def get(self, request, tfc_id):
        test_for_class = get_object_or_404(TestForClass, id=tfc_id)
        member = test_for_class.current_class.UserExistsInMembers(request.user.id)
        if member:
            test = test_for_class.test
            questions = test.Questions_objs()
            return render(request, 'tests/test_pass.html', context={'test':test, 'questions':questions})
        return HttpResponseNotFound()
    
    
    def post(self, request, tfc_id):
        test_for_class = get_object_or_404(TestForClass, id=tfc_id)
        question_ids = [(int(s.split('_')[-1]), request.POST[s]) for s in request.POST if any(xs in s for xs in ['answer'])]
        pt = PassedTest(user=request.user, test_for_class=test_for_class)
        pt.save()
        for id, value in question_ids:
            question = get_object_or_404(Question, id=id, test__id=test_for_class.test.id)
            answ = get_object_or_404(Answer, value=value, question__id=question.id)  
            pq = PassedQuestion(question=question, answer=answ, passed_test=pt)
            pq.save()
        return redirect('home')