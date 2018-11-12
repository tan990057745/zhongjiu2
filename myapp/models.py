from django.db import models

# Create your models here.

class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=10)
    class Meta:
        abstract = True

class Wheel(Base):
    class Meta:
        db_table='zj_wheel'

# 首页商品白酒切换展示
# "img":"img/floor_liquor1.jpg",
# 			"id":11,
# 			"name":"52°泸州老窖头曲500ml",
# 			"price":"￥129.00",
# 			"small":{
# 					"img1":"img/floor_liquor1.jpg",
# 					"img2":"img/floor_liquor1 (2).jpg",
# 					"img3":"img/floor_liquor1 (3).jpg",
# 					"img4":"img/floor_liquor1 (4).jpg",
# # 					"img5":"img/floor_liquor1 (5).jpg"
# 			}

class HomeShow(models.Model):
    img = models.CharField(max_length=100)        #图片
    productid = models.CharField(max_length=10)   #产品ID
    name = models.CharField(max_length=100)       #名字
    price = models.DecimalField(max_digits=7, decimal_places=2)   #价格
    typeid = models.CharField(max_length=10)      #分类ID
    class Meta:
        abstract = True

class whiteSpirit(HomeShow):
    class Meta:
        db_table = 'zj_whiteSpirit'


#创建商城商品列表
class Goods(models.Model):
    img = models.CharField(max_length=256)  #图片
    photo = models.CharField(max_length=256)  #详细图片
    name = models.CharField(max_length=100) #名字
    price = models.DecimalField(max_digits=7, decimal_places=2) #价格
    saleNum = models.IntegerField()         #销量
    commentsNum = models.IntegerField()  #评论数量

    isxf = models.IntegerField()         #是否优选
    brandid = models.IntegerField()       #品牌ID
    placeid = models.IntegerField()     #产地
    suitid = models.IntegerField()        #适用ID
    goodsid = models.IntegerField()      #商品编号
    class Meta:
        db_table='zj_market'

class Users(models.Model):
    # 账号
    account = models.CharField(max_length=80, unique=True)
    # 密码
    password = models.CharField(max_length=256)
    # 手机号
    phone = models.CharField(max_length=20, unique=True)
    # 地址
    addr = models.CharField(max_length=256)
    # token
    token = models.CharField(max_length=256)
    class Meta:
        db_table = 'zj_users'

class shoppingCart(models.Model):
    # 用户
    user = models.ForeignKey(Users)
    # 商品
    goods = models.ForeignKey(Goods)
    # 商品数量(选择)
    number = models.IntegerField()
    # 是否选中
    isselect = models.BooleanField(default=True)
    class Meta:
        db_table = 'zj_shoppingcart'

class myCart(models.Model):
    user = models.ForeignKey(Users)
    goods = models.ForeignKey(Goods)
    number = models.IntegerField()
    isselect = models.BooleanField(default=True)
    class Mata:
        db_table = 'zj_maycart'




