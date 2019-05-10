from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    email = forms.EmailField()

class CreateAddr(forms.Form):
    name=forms.CharField(label='姓名',validators=[
        validators.RegexValidator(
            regex=r'^\w{2,20}$',message='姓名输入有误'
        )
    ])

    addr=forms.CharField(label='地址',validators=[
        validators.RegexValidator(
            regex=r'^\w{6,40}$',message='地址输入有误'
        )
    ])

    postcode=forms.CharField(label='邮编',validators=[
        validators.RegexValidator(
            regex=r'\d{6}$',message='邮编输入有误'
        )
    ])

    tel=forms.CharField(label='手机号码',validators=[
        validators.RegexValidator(
            regex=r'^\d{11}$',message='手机号码输入有误'
        )
    ])



# class LoginFrom(forms.Form):
#     username = forms.CharField(label='用户名', validators=
#     [validators.RegexValidator(regex=r'^\w{5,10}$', message='用户名必须是5-10位的数字，字母或下滑线')])
#     pwd=forms.CharField(label='密码',validators=
#     [validators.RegexValidator(regex=r'^\w{5,20}$',message='密码必须是5-20位的数字，字母或下划线')])
