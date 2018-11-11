import hashlib
import io
import os
import random
import uuid

from PIL import ImageFont, ImageDraw, Image
from django.conf import settings
from django.http import HttpResponse, response, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.models import Wheel, whiteSpirit, Goods, Users, shoppingCart


#######主页
def home(request):
    token = request.session.get('token')
    if token:
        user = Users.objects.get(token=token)
        account = user.account
    else:
        account = '未登录'

    wheels = Wheel.objects.all()
    whitespirits0 = whiteSpirit.objects.filter(typeid=0)
    whitespirits1 = whiteSpirit.objects.filter(typeid=1)
    whitespirits2 = whiteSpirit.objects.filter(typeid=2)
    whitespirits3 = whiteSpirit.objects.filter(typeid=3)
    whitespirits4 = whiteSpirit.objects.filter(typeid=4)
    whitespirits5 = whiteSpirit.objects.filter(typeid=5)

    data = {
        'wheels': wheels,
        'whitespirits0': whitespirits0,
        'whitespirits1': whitespirits1,
        'whitespirits2': whitespirits2,
        'whitespirits3': whitespirits3,
        'whitespirits4': whitespirits4,
        'whitespirits5': whitespirits5,
        'account': account
    }
    return render(request, 'home.html', context=data)


####以上为主页########


###########验证码########
def verifycode(request):
    # 创建图片
    width = 80
    height = 24
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    image = Image.new('RGB', (width, height), (r, g, b))
    # 随机数
    str = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    rand_str = ''
    for i in range(0, 4):
        temp = random.randrange(0, len(str))
        rand_str += str[temp]
    # session保存验证码
    request.session['rand_str'] = rand_str
    request.session.set_expiry(60 * 3)
    # 创建画笔
    draw = ImageDraw.Draw(image)
    # 导入字体
    font = ImageFont.truetype('static/fonts/Fangsong.ttf', 20)
    # 添加噪点
    for i in range(0, 300):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
        draw.point(xy, fill=fill)
    # 字体颜色
    fontcolor1 = (255, random.randrange(0, 256), random.randrange(0, 256))
    fontcolor2 = (255, random.randrange(0, 256), random.randrange(0, 256))
    fontcolor3 = (255, random.randrange(0, 256), random.randrange(0, 256))
    fontcolor4 = (255, random.randrange(0, 256), random.randrange(0, 256))

    # 绘制操作
    draw.text((5, 2), rand_str[0], fill=fontcolor1, font=font)
    draw.text((20, 2), rand_str[1], fill=fontcolor2, font=font)
    draw.text((40, 2), rand_str[2], fill=fontcolor3, font=font)
    draw.text((60, 2), rand_str[3], fill=fontcolor4, font=font)
    # 释放
    del draw
    # 文件操作
    buff = io.BytesIO()
    image.save(buff, 'png')  # 保存在内存中
    return HttpResponse(buff.getvalue(), 'image/png')


#########以上为验证码########

def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()


######注册####
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        user = Users()
        user.account = request.POST.get('account')
        user.password = genarate_password(request.POST.get('password'))
        user.phone = request.POST.get('phone')
        user.addr = request.POST.get('addr')
        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        user.save()
        # 状态保持
        request.session['token'] = user.token
        return redirect('myapp:home')


######注册######


######登陆#################
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        print('haha')
        try:
            user = Users.objects.get(account=account)
            if user.password == genarate_password(password):  # 登录成功
                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('myapp:home')
            else:  # 登录失败
                return render(request, 'login.html', context={'passwdErr': '密码错误!'})
        except:
            return render(request, 'login.html', context={'acountErr': '账号不存在!'})


#####以上为登陆######


### 验证校验码################
def checkVerifyCode(request):
    code = request.session.get('rand_str').lower()
    responseData = {
        'code': code,
    }
    return JsonResponse(responseData)


#########验证码验证#####

###########购物车#####
def shoppingCart(request):
    token = request.session.get('token')

    if token:  # 显示该用户下 购物车信息
        user = Users.objects.get(token=token)
        carts = shoppingCart.objects.filter(user=user).exclude(number=0)

        return render(request, 'shoppingCart.html', context={'carts': carts})
    else:  # 跳转到登录页面
        return redirect('myapp:login')
#######以上为购物车#####


#####闪购超市#####
# def market(request,brandid,placeid,priceid,suitid,sortid):
def market(request):
    brandIndex = int(request.COOKIES.get('brandIndex', 0))
    placeIndex = int(request.COOKIES.get('placeIndex', 0))
    priceIndex = int(request.COOKIES.get('priceIndex', 0))
    suitIndex = int(request.COOKIES.get('suitIndex', 0))
    sortIndex = int(request.COOKIES.get('sortIndex', 0))

    print(brandIndex, placeIndex, priceIndex, suitIndex, sortIndex)
    print(type(brandIndex))
    xfList = Goods.objects.filter(isxf=1)  # 精选列表

    if brandIndex == 0 or brandIndex == 1:
        goodsList1 = Goods.objects.all()
        # print('haha1')
    else:
        goodsList1 = Goods.objects.filter(brandid=brandIndex)
        # print('h哈哈2')

    if placeIndex == 0 or placeIndex == 1:
        goodsList2 = goodsList1
    else:
        goodsList2 = goodsList1.filter(placeid=placeIndex)

    if priceIndex == 0 or priceIndex == 1:  # 按价格区间筛选
        goodsList3 = goodsList2
    elif priceIndex == 2:
        goodsList3 = goodsList2.filter(price__gte=1, price__lte=99)
    elif priceIndex == 3:
        goodsList3 = goodsList2.filter(price__gte=100, price__lte=199)
    elif priceIndex == 4:
        goodsList3 = goodsList2.filter(price__gte=200)
    #
    if suitIndex == 0 or suitIndex == 1:
        goodsList4 = goodsList3
    else:
        goodsList4 = goodsList3.filter(suitid=suitIndex)

    if sortIndex == 0 or sortIndex == 1:
        goodsList5 = goodsList4
    elif sortIndex == 2:
        goodsList5 = goodsList4.order_by('-price')  # 按价格
    elif sortIndex == 3:
        goodsList5 = goodsList4.order_by('-commentsNum')  # 按评论数

    data = {
        'goodsList': goodsList5,
        'xfList': xfList,
    }
    return render(request, 'market.html', context=data)


#####闪购超市######################


#####账户验证#####
def checkaccount(request):
    account = request.GET.get('account')
    responseData = {
        'msg': '账号可用',
        'status': 1
    }
    try:
        user = Users.objects.get(account=account)
        responseData['msg'] = '账号已被占用'
        responseData['status'] = -1
        return JsonResponse(responseData)
    except:
        return JsonResponse(responseData)


########账号验证


#########登出#####
def logout(request):
    request.session.flush()
    return redirect('myapp:home')


########登出#######


####商品详情#######
def productMsg(request, num):
    product = Goods.objects.get(pk=num)
    photoList = []
    photoList = product.photo.split('#')
    # print(photoList)
    token = request.session.get('token')
    shoppingCart = []

    if token:  # 根据用户，获取对应用户下所有购物车数据
        user = Users.objects.get(token=token)
        account = user.account
    else:
        account = '未登录'


    if token:  # 根据用户，获取对应用户下所有购物车数据
        user = Users.objects.get(token=token)
        carts = shoppingCart.objects.filter(user=user)

    data = {
        'product': product,
        'photoList0': photoList[0],
        'photoList1': photoList[1],
        'photoList2': photoList[2],
        'photoList3': photoList[3],
        'photoList4': photoList[4],
        'carts':carts,
        'account': account,
    }
    return render(request, 'productMsg.html', context=data)
######商品详情######



def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg': '添加购物车成功',
        'status': 1  # 1标识添加成功，0标识添加失败，-1标识未登录
    }

    if token:  # 登录 [直接操作模型]
        # 获取用户
        user = Users.objects.get(token=token)
        # 获取商品
        goods = Goods.objects.get(pk=goodsid)

        # 商品已经在购物车，只修改商品个数
        # 商品不存在购物车，新建对象（加入一条新的数据）
        carts = shoppingCart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():  # 修改数量
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number
        else:  # 添加一条新记录
            cart = shoppingCart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()
            responseData['number'] = cart.number

        return JsonResponse(responseData)
    else:  # 未登录 [跳转到登录页面]
        responseData['msg'] = '未登录，请登录后操作'
        print('哈哈啊')
        responseData['status'] = -1
        return JsonResponse(responseData)


def subcart(request):
    # 获取数据
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    # 对应用户 和 商品
    user = Users.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    # 删减操作
    cart = shoppingCart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg': '购物车减操作成功',
        'status': 1,
        'number': cart.number,
    }

    return JsonResponse(responseData)