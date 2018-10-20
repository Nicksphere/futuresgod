from django.db import models

# Create user table


class User(models.Model):
    """
    操作员账号表
    """
    # 登陆账号
    username = models.CharField(max_length=100, null=False)
    # 登陆密码
    pwd = models.CharField(max_length=100, null = False)
    # 交易账号
    investorid = models.CharField(max_length=100, null=False, default='tradetest1')
    # 交易密码
    investorpwd = models.CharField(max_length=100, null=False, default='tradetest1')
    # 交易服务器
    frontaddr = models.CharField(max_length=100, null=False, default='trade_server1')
    # brokerid
    brokerid = models.BigIntegerField(default=10000)
    # 可用资金
    available = models.FloatField(default=0.0, null=False)
    # 当前保证金
    withdrawquota = models.FloatField(default=0.0, null=False)
    # 平仓盈亏
    currmargin = models.FloatField(default=0.0,null=False)
    create_date = models.DateTimeField('date published')
    type = models.BigIntegerField(default=1)
    is_valid = models.BigIntegerField(default=1)
    belongs = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)


class UserFunds(models.Model):
    """
    跟单账户表
    """
    # 交易账号
    investorid = models.CharField(max_length=100, null=False, default='tradetest1')
    # 交易密码
    investorpwd = models.CharField(max_length=100, null=False, default='tradetest1')
    # 交易服务器
    frontaddr = models.CharField(max_length=100, null=False, default='trade_server1')
    # brokerid
    brokerid = models.BigIntegerField(default=10000)
    # 可用资金
    available = models.FloatField(default=0.0, null=False)
    # 可取资金
    withdrawquota = models.FloatField(default=0.0, null=False)
    # 当前保证金
    currmargin = models.FloatField(default=0.0, null=False)
    # 平仓盈亏
    closeprofit = models.FloatField(default=0.0, null=False)
    # 跟单账户id
    followaccount = models.CharField(max_length=100)
    create_date = models.DateTimeField('date published')
    type = models.BigIntegerField(default=1)
    is_valid = models.BigIntegerField(default=1)
    belongs = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)


class Position(models.Model):
    """
    持仓表
    """
    # 交易账户
    investorid = models.CharField(max_length=100, null=False, default='tradetest1')
    # 合约代码
    instrumentid = models.CharField(max_length=100, null=False)
    # 持仓成本
    positioncost = models.FloatField(default=0.0, null=False)
    # 开仓量
    totalamt = models.BigIntegerField(default=0)
    # 开仓方向
    posidirection = models.CharField(max_length=100)
    # 占用保证金
    usemargin = models.FloatField(default=0.0)
    # 开仓日期
    position_date = models.DateTimeField('date published')
    is_valid = models.BigIntegerField(default=1)
    desc = models.TextField(max_length=500)