from django.conf.urls import url

from myapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),                        #登录
    url(r'^logout/$', views.logout, name='logout'),                     #登出
    url(r'^market/$', views.market, name='market'),                      #商场选购
    url(r'^verifycode/$', views.verifycode, name='verifycode'),
    url(r'^verifycode/\d+/$', views.verifycode),                #验证码刷新
    url(r'^shoppingCart/$', views.shoppingCart, name='shoppingCart'),

    url(r'^checkVerifyCode/$', views.checkVerifyCode, name='checkVerifyCode'),    #校验码验证
    url(r'^checkaccount/$', views.checkaccount, name='checkaccount'),
    url(r'^productMsg/(\d+)/$', views.productMsg, name='productMsg'),              #商品详情
    url(r'^addcart/$', views.addcart, name='addcart'),        #加购物车
    url(r'^subcart/$', views.subcart, name='subcart'),        #减购物车
    url(r'^joinCart/$', views.joinCart, name='joinCart'),      #加入购物车

]
