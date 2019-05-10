from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
import json
import os
from whoosh.filedb.filestore import FileStorage
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser


def indexs(request):
    # user = form.get_user()
    auth_logout(request)
    return redirect('fresh')
    # user = None

def index(request,p=1):
    lunbo = Banner.objects.all()
    lunbo2 = Category.objects.filter(icon='广告图2').all()
    toutu = Category.objects.filter(desc=1).all()
    fentu = Goods.objects.filter(num=2).all()
    logo = Category.objects.get(name='logo')
    try:
        num = request.session['num']
    except Exception:
        num = 0
    imgs = {
        'num':num,
        'lunbo':lunbo,
        'lunbo2':lunbo2,
        'toutu': toutu,
        'fentu':fentu,
        'logo':logo,
        'p':p
        }
    return render(request, 'index.html',imgs)


def logins(request):
    return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user=user)
            user = User.objects.get(username=request.user)
            shop = Shopping.objects.filter(user_id_id=user.id, state=1).all()
            num = 0
            for i in shop:
                num = num + i.number
            request.session['num'] = num
            return redirect(request.POST.get('next','fresh'))
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'next':request.GET.get('next','fresh')
    }
    return render(request, 'login.html',context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        email=request.POST.get('email')
        if form.is_valid():
            user=form.save()
            user_email=User.objects.filter(username=user).update(email=email)
            return redirect('login')
    else:
        form = RegisterForm()
    imgs = Category.objects.get(name='logo')
    context = {
        'form':form,
        'imgs':imgs
    }
    return render(request,'register.html',context)

@login_required
def info(request):
    user = User.objects.get(username=request.user)
    over = Over.objects.filter(user_id_id=user.id).order_by('-id').all()
    try:
        add = Addr.objects.get(user_id=user.id, approve=2)
    except Exception:
        add=None
    logo=Category.objects.get(name='logo')
    context = {
        'logo':logo,
        'add':add,
        'over':over
    }
    return render(request,'user_center_info.html',context)


def order(request):         #区分已买和没有买的货物
    try:
        yigou = request.GET.get('ids')
        yigou = json.loads(yigou)
        shuzi = Shopping.objects.filter(id__in=yigou).update(state=2)
        shuzis = Shopping.objects.filter(id__in=yigou,state=2).order_by('-id')[:int(shuzi)]
        sets = 0
        for i in shuzis:
            sets += i.number
        print(123123123)
        print(sets)
        print(123123123)
        num = request.session['num'] = request.session['num'] - sets
    except Exception as a:
        print(a)
        pass
    user = User.objects.get(username=request.user)
    logo=Category.objects.get(name='logo')
    shop_yi = Shopping.objects.filter(user_id_id=user.id,state=2).order_by('-id').all()
    shop_mei = Shopping.objects.filter(user_id_id=user.id, state=1).all()
    context = {'shopyi':shop_yi,
               'shopmei':shop_mei,
               'logo':logo
               }
    return render(request,'user_center_order.html',context)

def site(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        provin = request.POST.get("address")
        code = request.POST.get("code")
        tel = request.POST.get("tel")
        user = User.objects.get(username=request.user)
        cunt = len(tel)
        if name and provin and code and cunt == 11:
            Addr.objects.create(name=name, provin=provin, code=code,tel=tel,user_id=user.id)
            res = {'name': '添加成功'}
        else:
            res = {'name':'添加失败'}
        return JsonResponse(res)
    else:
        logo = Category.objects.get(name='logo')
        user = User.objects.get(username=request.user)


        default = Addr.objects.filter(user_id=user.id).all()
        context = {'default':default,
                   'logo':logo

                   }
        cunt = len(default)
        return render(request,'user_center_site.html',context)


@login_required
def cart(request):
    logo = Category.objects.get(name="logo")
    user = User.objects.get(username=request.user)
    shop = Shopping.objects.filter(user_id_id=user.id,state=1).all()
    # num = request.session['num']
    context = {
        'shop':shop,
        # 'good':good,
        # 'sum':num,
        'logo':logo
               }
    return render(request, 'cart.html',context)



@login_required
def place_order(request):               #提交订单
    logo = Category.objects.get(name='logo')
    user = User.objects.get(username=request.user)
    # num = request.session['num']
    try:                                #没有地址时
        addr = Addr.objects.filter(user_id=user.id, approve=2).get()
    except:
        addr = None

    # 获取的为商品详情的购买信息
    detail = request.GET.get('one')       #为详情中进行提交的购物数据
    if detail:              #判断是否是详情提交的数据
        good_num = request.GET.get('two')
        good_num = int(json.loads(good_num))
        detail = int(json.loads(detail))
        try:     #看购物车中是否已经添加
            shop = Shopping.objects.get(user_id_id=user.id,goods_id_id=int(detail),state=1)
            set = shop.number
            # num = request.session['num'] =request.session['num'] - set + good_num
            Shopping.objects.filter(user_id_id=user.id, goods_id_id=int(detail),state=1).update(number=good_num)
        except Exception as a:
            #没有添加时的值,可进行新增一
            Shopping.objects.filter(user_id_id=user.id, goods_id_id=int(detail)).create(number=good_num,user_id_id=user.id, goods_id_id=int(detail))
            # num = request.session['num'] = request.session['num'] + good_num

        good = Shopping.objects.filter(user_id_id=user.id,goods_id_id=int(detail),state=1).all()

        for i in good:
            num2 = i.number

    else:
        try:   #看是否是购物车提交的数据
            ids = request.GET.get('ids')
            ids = json.loads(ids)

        # print(type(ids))
            good = Shopping.objects.filter(goods_id_id__in=ids,user_id_id=user.id,state=1).all()

            num2=0
            for i in good:
                num2 += i.number

        except Exception:          #我的订单提交的数据
            # num2 = request.session['num']
            good = Shopping.objects.filter(user_id_id=user.id,state=1).all()

    context = {
        # 'num':num2,
        'addr': addr,
        'good':good,
        'logo':logo
        }
    return render(request, 'place_order.html',context)



def dizhi(request):

    valu = request.POST.get('select')
    print(123)
    print(valu)
    print(456)
    user = User.objects.get(username=request.user)
    Addr.objects.filter(user_id=user.id,approve=2).update(approve=1)
    Addr.objects.filter(pk=int(valu)).update(approve=2)
    res = {'name': '地址确定成功'}
    return JsonResponse(res)

@login_required
def detail(request,detail_id):
    user = User.objects.get(username=request.user)

    try:
        Over.objects.get(user_id_id=user.id,goods_id_id=detail_id)
    except Exception:
        over_num = Over.objects.filter(user_id_id=user.id).count()
        if over_num == 5:       #进行浏览表单数量的控制
            first_over = Over.objects.filter(user_id_id=user.id).first()
            print(first_over)
            Over.objects.filter(id=first_over.id).delete()
            Over.objects.create(user_id_id=user.id, goods_id_id=detail_id)
        else:
            Over.objects.create(user_id_id=user.id,goods_id_id=detail_id)

    logo = Category.objects.get(name='logo')
    good = Goods.objects.filter(pk=detail_id).get()

    forset = Goods.objects.filter(Meta_id_id=good.Meta_id_id).order_by('-id').all()[:2]

    try:
        user = User.objects.get(username=request.user)
        num = request.session['num']
    except Exception:
        num = 0

    barter = {
        'good':good,
        'number':num,
        'logo':logo,
        'forset':forset
    }
    return render(request,'detail.html',barter)



def list(request,list_id,p=1):

    search = request.GET.get('search')

    if list_id == 0:
        storage = FileStorage('./index')
        ix = storage.open_index()
        with ix.searcher() as searcher:
            query = QueryParser('goods_name',ix.schema).parse(search)
            results = searcher.search(query,limit=None)
            lis = []
            for res in results:
                lis.append(int(res.get('goods_id')))

        if not lis:
            p = 2
            return redirect('/fresh/'+ str(p))

        else:
            goods = Goods.objects.filter(id__in=lis).all()
            goods_one = Goods.objects.filter(id__in=lis).first()
            try:
                forset = Goods.objects.filter(Meta_id_id=goods_one.Meta_id_id).order_by('-id').all()[:2]
            except Exception:
                forset = None
            name = Category.objects.get(name='搜索内容')

    else:
        goods = Goods.objects.filter(Meta_id_id=list_id).all()
        forset = Goods.objects.filter(Meta_id_id=list_id).order_by('-id').all()[:2]
        name = Category.objects.get(id=list_id)


    paginator = Paginator(goods, 3)
    page = paginator.get_page(p)
    logo = Category.objects.get(name='logo')
    try:
        user = User.objects.get(username=request.user)
        num = request.session['num']
    except Exception:
        num = 0

    imgs = {'good':page,
            'name':name,
            'num':num,
            'p':p,
            'logo':logo,
            'forset':forset
            }
    return render(request,'list.html',imgs)


@login_required
def shopping(request):            #异步进行详情页面的购物车购买
    valu = request.POST.get('date')
    user = User.objects.get(username=request.user)
    number = len(Shopping.objects.filter(user_id_id=user.id,state=1).all())
    ones = int(request.POST.get('ones'))
    try:         #当里面已经存在时
        nun = Shopping.objects.filter(user_id_id=user.id, goods_id_id=valu,state=1).get()
        set = nun.number + ones
        num = request.session['num'] = request.session['num'] +ones
        Shopping.objects.filter(user_id_id=user.id, goods_id_id=valu,state=1).update(number=set)
        res = {
            'name': number,
            'names':123
               }
        return JsonResponse(res)

    except Exception:           #当里面没存在时，进行创建
        Shopping.objects.create(user_id_id=int(user.id),goods_id_id=valu,number=ones)
        num = request.session['num'] = request.session['num'] + ones
        res = {
            'name': number,
            'names':123
               }
        return JsonResponse(res)


@login_required
def shop(request,p):
    user = User.objects.get(username=request.user)
    meat = Goods.objects.get(id=p)
    try:
        nun = Shopping.objects.filter(user_id_id=user.id, goods_id_id=p).get()
        set = nun.number + 1

        num = request.session['num'] =  num = request.session['num'] +1

        Shopping.objects.filter(user_id_id=user.id, goods_id_id=p).update(number=set)
        return redirect('info')
    except Exception:

        num = request.session['num'] = num = request.session['num'] + 1

        Shopping.objects.create(user_id_id=int(user.id), goods_id_id=p)
        return redirect('info')


@login_required
def shoppings(request,p):
    user = User.objects.get(username=request.user)
    meat = Goods.objects.get(id=p)
    meats = meat.Meta_id_id
    print(meats)
    number = len(Shopping.objects.filter(user_id_id=user.id).all())
    try:
        nun = Shopping.objects.filter(user_id_id=user.id, goods_id_id=p).get()
        set = nun.number + 1

        num = request.session['num'] =  num = request.session['num'] +1

        Shopping.objects.filter(user_id_id=user.id, goods_id_id=p).update(number=set)
        return redirect('/list/'+ str(meats))
    except Exception:

        num = request.session['num'] = num = request.session['num'] + 1

        Shopping.objects.create(user_id_id=int(user.id), goods_id_id=p)
        return redirect('/list/'+str(meats))


def shanchu(request,shop_id):           #删除购物车东西

    nums = Shopping.objects.filter(id=int(shop_id)).get()
    Shopping.objects.filter(id=int(shop_id)).delete()
    num = request.session['num'] = request.session['num'] - nums.number
    return redirect('cart')



def adds(request):    #数据库中的数量加减   post为加，get为减
    if request.method == 'POST':
        print('adsiand')
        nums = request.POST.get('date')
        ids = request.POST.get('ids')
        num = request.session['num'] = request.session['num']+1
    else:
        nums = request.GET.get('date')
        ids = request.GET.get('ids')
        num = request.session['num'] = request.session['num'] -1

    Shopping.objects.filter(id=ids).update(number=nums)

    res = {
        'num': num
    }
    return JsonResponse(res)

#创建全文索引
def about_index(request):
    analyzer = ChineseAnalyzer()
    schema = Schema(
        goods_name=TEXT(stored=True, analyzer=analyzer),
        goods_id=TEXT(stored=True, analyzer=analyzer)
    )
    storage = FileStorage('./index')
    if not os.path.exists('./index'):
        os.mkdir('./index')
        ix = storage.create_index(schema)
    else:
        ix = storage.open_index()

    writer = ix.writer()
    for goods in Goods.objects.all():
        writer.add_document(goods_name=goods.name, goods_id=str(goods.id))
    writer.commit()
    return HttpResponse('创建索引完成')

