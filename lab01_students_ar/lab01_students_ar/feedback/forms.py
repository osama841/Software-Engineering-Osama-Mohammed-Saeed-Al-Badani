from django import forms

class FeedbackForm(forms.Form):
    student_name = forms.CharField(
        label='اسم الطالب',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    course_name = forms.CharField(
        label='اسم المقرر',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    understanding_level = forms.ChoiceField(
        label='مدى فهمك للمقرر',
        choices=[
            ('excellent', 'ممتاز'),
            ('good', 'جيد'),
            ('average', 'متوسط'),
            ('poor', 'ضعيف')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    positives = forms.CharField(
        label='الإيجابيات',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    negatives = forms.CharField(
        label='السلبيات',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    improvements = forms.CharField(
        label='ما الذي يمكن تحسينه؟',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    comparison = forms.CharField(
        label='مقارنة مع مقررات أخرى',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    
    future_use = forms.CharField(
        label='هل تود استخدام هذه التقنية في مقررات أخرى؟',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )