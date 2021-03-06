# Generated by Django 2.1.7 on 2019-02-28 05:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nick', models.CharField(max_length=10, null=True, verbose_name='昵称')),
                ('avatar', models.ImageField(null=True, upload_to='', verbose_name='头像')),
                ('tel', models.CharField(max_length=11, null=True, verbose_name='手机')),
                ('sex', models.SmallIntegerField(choices=[(0, '女'), (1, '男'), (2, '保密')], default=2, verbose_name='性别')),
                ('birthday', models.DateField(null=True, verbose_name='生日')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '账号',
                'verbose_name_plural': '账号',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Addr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='收件人')),
                ('provin', models.CharField(max_length=40, verbose_name='省')),
                ('code', models.CharField(max_length=8, verbose_name='邮编')),
                ('tel', models.CharField(max_length=11, verbose_name='手机号')),
                ('approve', models.IntegerField(default=1, verbose_name='编号')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='图片名')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='图片')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='名称')),
                ('icon', models.CharField(blank=True, max_length=200, null=True, verbose_name='简介')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='图片')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='详情')),
                ('creayed_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='everyday.Category', verbose_name='父分类')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('price1', models.FloatField(verbose_name='原件')),
                ('price2', models.FloatField(verbose_name='现价')),
                ('status', models.CharField(max_length=10, null=True, verbose_name='现状')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='图片')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='详情')),
                ('creayed_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('icon', models.CharField(blank=True, max_length=200, null=True, verbose_name='简介')),
                ('num', models.IntegerField(default=1, verbose_name='首页展示商品')),
                ('Meta_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='everyday.Category', verbose_name='分类')),
            ],
        ),
        migrations.CreateModel(
            name='Over',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1, verbose_name='数量')),
                ('goods_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='everyday.Goods', verbose_name='商品id')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Shopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1, verbose_name='数量')),
                ('state', models.IntegerField(default=1, verbose_name='商品付款状态')),
                ('name', models.CharField(default=1, max_length=20, verbose_name='订单号')),
                ('goods_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='everyday.Goods', verbose_name='商品id')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户id')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='user_id',
            field=models.ManyToManyField(through='everyday.Shopping', to=settings.AUTH_USER_MODEL, verbose_name='用户商品'),
        ),
    ]
