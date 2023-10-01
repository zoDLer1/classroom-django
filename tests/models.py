from django.db import models



class Test(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True)
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['name', 'creator']
    
    def Questions_objs(self):
        return [{'question': question, 'answers': question.Answers()} for question in self.Questions()]
    
    def Questions(self):
        return Question.objects.filter(test__id=self.id)
    
    def ExistsInTestForClass(self):
        try:
            return TestForClass.objects.get(test__id=self.id)
        except:
            return None 

    
    
class Question(models.Model):
    name = models.CharField(max_length=150)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    def Answers(self):
        return Answer.objects.filter(question__id=self.id)
    
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=150)
    right = models.BooleanField(default=False)
    
class TestForClass(models.Model):
    current_class = models.ForeignKey('classes.Class', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def ExistsInPassedTest(self):
        try:
            return PassedTest.objects.get(test_for_class__id=self.id)
        except:
            return None 
    
    def Passed_Tests(self):
        return PassedTest.objects.filter(test_for_class__id=self.id)  
    
class PassedTest(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    test_for_class = models.ForeignKey(TestForClass, on_delete=models.CASCADE)
    def Questions_objs(self):
        return [{'question': question.question, 'answers': question.question.Answers(), 'answer':question.answer} for question in self.Questions()]
    def Questions(self):
        return PassedQuestion.objects.filter(passed_test__id=self.id)
    def CorrectQuestions(self):
        return PassedQuestion.objects.filter(passed_test__id=self.id, answer__right=True)
    def Persent(self):
        return self.CorrectQuestions().count() / self.Questions().count() * 100
    
    
class PassedQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    passed_test = models.ForeignKey(PassedTest, on_delete=models.CASCADE)
    
    