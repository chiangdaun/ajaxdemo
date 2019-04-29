import json

from django.core import serializers
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import widgets
from django.shortcuts import render, HttpResponse
from app01.models import Person, UserInfo, City


# Create your views here.
def index(request):
    return render(request, "index.html")


def ajax_add(request):
    i1 = request.GET.get("i1")
    i2 = request.GET.get("i2")

    ret = int(i1) + int(i2)

    # print(i1, i2)
    # print("===" * 80)
    return HttpResponse(ret)


def test(request):
    import time
    time.sleep(5)
    url = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1556467048401&di=b819ef9a4af92c657eceadd08aba03f6&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201610%2F31%2F20161031082030_uBYix.thumb.700_0.jpeg"
    return HttpResponse(url)


def ajax_add3(request):
    i1 = request.POST.get("i1")
    i2 = request.POST.get("i2")

    ret = int(i1) + int(i2)

    # print(i1, i2)
    # print("===" * 80)
    return HttpResponse(ret)


def person(request):
    ret = Person.objects.all()

    # # 自己实现的序列化
    # person_list = []
    # for i in ret:
    #     person_list.append({"name": i.name, "age": i.age})
    # print(person_list)
    # s = json.dumps(person_list)
    # print(s)
    #
    # # 使用django自带序列化方法
    # s2 = serializers.serialize("json", ret)
    # print(s2)

    return render(request, 'sweetalert_demo.html', {"persons": ret})


def delete(request):
    del_id = request.POST.get("id")
    Person.objects.filter(id=del_id).delete()
    return HttpResponse("删除成功!")


def test2(request):
    if request.method == "POST":
        name = request.POST.get("name")
        sb = request.POST.getlist("sb")
        print(name)
        print(sb, type(sb))

        # ret = {
        #     "status": 0,
        #     "data": [
        #         {"name": "alex", "age": 18},
        #         {"name": "xiaohei", "age": 28},
        #     ]
        # }

        ret = {
            "status": 1,
            "error": "用户名已被注册！"
        }
        ret_str = json.dumps(ret)
        return HttpResponse(ret_str)

    return render(request, "test2.html")


def check_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        # 去数据库中查询用户名是否已经被注册
        ret = UserInfo.objects.filter(name=name)
        if ret:
            # 用户名已经存在
            msg = "用户名已被注册！"
        else:
            msg = "用户名可用"

        return HttpResponse(msg)


# 原生表单
def register(request):
    error = {'user': '', 'pwd': ''}
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        if len(pwd) < 6:
            error['pwd'] = "密码不能小于6位"
    return render(request, 'register.html', {"error": error})


class RegForm(forms.Form):
    name = forms.CharField(
        # 校验规则相关
        max_length=16,
        label="用户名",
        error_messages={
            "required": "该字段不能为空",
        },
        # widget控制的是生成html代码相关的
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    pwd = forms.CharField(
        label="密码",
        min_length=6,
        max_length=10,
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位！",
            "max_length": "密码最长10位！",
            "required": "该字段不能为空",
        }
    )
    re_pwd = forms.CharField(
        label="确认密码",
        min_length=6,
        max_length=10,
        widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        error_messages={
            "min_length": "密码不能少于6位！",
            "max_length": "密码最长10位！",
            "required": "该字段不能为空",
        }
    )
    email = forms.EmailField(
        label="邮箱",

        widget=widgets.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "该字段不能为空",
        }
    )
    mobile = forms.CharField(
        label="手机",
        # 自己定制校验规则
        validators=[
            RegexValidator(r'^[0-9]+$', '手机号必须是数字'),
            RegexValidator(r'^1[3-9][0-9]{9}$', '手机格式有误')
        ],
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "该字段不能为空",
        }
    )
    city = forms.ChoiceField(
        choices=City.objects.all().values_list("id", "name"),
        label="城市",
        initial=1,
        widget=forms.widgets.Select
    )

    # 重写父类的init方法
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].widget.choices = City.objects.all().values_list("id", "name")

    def clean_name(self):
        value = self.cleaned_data.get("name")
        if "金瓶梅" in value:
            raise ValidationError("不符合社会主义核心价值观！")
        return value

    # 重写父类的clean方法
    def clean(self):
        # 此时 通过检验的字段的数据都保存在 self.cleaned_data
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd != re_pwd:
            self.add_error("re_pwd", ValidationError("两次密码不一致"))
            raise ValidationError("两次密码不一致")
        return self.cleaned_data


def register2(request):
    form_obj = RegForm()
    if request.method == "POST":
        form_obj = RegForm(request.POST)
        # form帮我们做校验
        if form_obj.is_valid():
            # 校验通过,数据入库
            # 所有通过校验的数据都保存在form.cleaned_data中
            print(form_obj.cleaned_data)
            # 数据库没有re_pwd字段，删除它;或者form_obj.cleaned_data.pop('re_pwd')
            del form_obj.cleaned_data['re_pwd']
            UserInfo.objects.create(**form_obj.cleaned_data)
            return HttpResponse("注册成功!")
    return render(request, 'register2.html', {"form_obj": form_obj})
