from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    nick = models.CharField('昵称', max_length=10, null=True)
    avatar = models.ImageField('头像', null=True)
    tel = models.CharField('手机', max_length=11, null=True)
    sex = models.SmallIntegerField('性别', choices=((0, '女'), (1, '男'), (2, '保密')), default=2)
    birthday = models.DateField('生日', null=True)
    ctime = models.DateTimeField('创建时间', auto_now_add=True)
    email=models.CharField('邮箱',max_length=20,null=True)




class Addr(models.Model):
    class Addr_name:
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    name = models.CharField('收件人',max_length=10)
    provin = models.CharField('省',max_length=40)
    code = models.CharField('邮编',max_length=8)
    tel = models.CharField('手机号',max_length=11)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    approve = models.IntegerField('编号',default=1)
    def __str__(self):
        return self.name

class Banner(models.Model):
    class Banners:
        verbose_name = '轮播'
        verbose_name_plural = verbose_name

    name = models.CharField('图片名',max_length=20)
    banner = models.ImageField('图片',upload_to='category/',null=True,blank=True)

    def __str__(self):
        return self.name



class Category(models.Model):
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
    parent = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name='父分类',null=True,blank=True)
    name = models.CharField('名称',max_length=100,unique=True)
    icon = models.CharField('简介',max_length=200,null=True,blank=True)
    banner = models.ImageField('图片',upload_to='category/',null=True,blank=True)
    desc =models.CharField('详情',max_length=200,null=True,blank=True)
    creayed_date=models.DateTimeField('创建日期',auto_now_add=True)
    def __str__(self):
        return self.name



class Goods(models.Model):
    class Good:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
    name = models.CharField('名称',max_length=20)
    price1 = models.FloatField('原件')
    price2 = models.FloatField('现价')
    status = models.CharField('现状',max_length=10,null=True)
    banner = models.ImageField('图片', upload_to='category/', null=True, blank=True)
    desc = models.CharField('详情', max_length=200, null=True, blank=True)
    creayed_date = models.DateTimeField('创建日期', auto_now_add=True)
    icon = models.CharField('简介',max_length=200,null=True,blank=True)
    Meta_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类',null=True,blank=True)
    user_id = models.ManyToManyField(User,through='Shopping',through_fields=('goods_id','user_id'),verbose_name='用户商品')
    num = models.IntegerField('首页展示商品',default=1)
    def __str__(self):
        return self.name



class Shopping(models.Model):
    goods_id = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品id',null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id', null=True, blank=True)
    number = models.IntegerField('数量',default=1)
    state = models.IntegerField('商品付款状态',default=1)
    name = models.CharField('订单号', max_length=20,default=1)
    # time = models.DateTimeField('时间',auto_now_add=True)


class Over(models.Model):
    goods_id = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品id', null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id', null=True, blank=True)
    number = models.IntegerField('数量', default=1)



















