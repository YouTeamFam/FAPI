# coding: utf-8

from tools.ext import db


class TAdPo(db.Model):#广告位置模型
    __tablename__ = 't_ad_pos'

    ad_pos_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    c_pos = db.Column(db.String(30))

class TAdBm(db.Model):#广告商模型
    __tablename__ = 't_ad_bm'

    ad_bm_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    pwd = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    ad_num = db.Column(db.Integer, nullable=False)
    set_time = db.Column(db.DateTime, nullable=False)
    val_ad_num = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(30), nullable=False)


class TAd(db.Model):#广告模型
    __tablename__ = 't_ad'

    ad_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    ad_url = db.Column(db.String(255), nullable=False)
    fabu_time = db.Column(db.DateTime)
    val = db.Column(db.DateTime)
    audit_state = db.Column(db.Integer)
    ad_bm_id = db.Column(db.Integer,db.ForeignKey('t_ad_bm.ad_bm_id'), index=True)
    ad_pos_id = db.Column(db.Integer,db.ForeignKey('t_ad_pos.ad_pos_id'), nullable=False, index=True)
    note = db.Column(db.String, nullable=False)

    # lazy = 'select' 表示查看属性时，才会执行selet查询语句, 如果是immediate 表示同当前所在的模型数据一起查询出来。
    ad_bm = db.relationship('TAdBm',backref='t_ads',lazy='immediate')
    ad_pos = db.relationship('TAdPo', backref='t_ads',lazy='immediate')


class TPtAdmin(db.Model):#普通管理员模型
    __tablename__ = 't_pt_admin'

    pt_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)



class TAdCheckRecord(db.Model):#广告审核记录表
    __tablename__ = 't_ad_check_record'

    ad_check_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    is_pass = db.Column(db.Integer, nullable=False)
    ad_id = db.Column(db.Integer,db.ForeignKey('t_ad.ad_id'), nullable=False, index=True)
    pt_id = db.Column(db.Integer,db.ForeignKey('t_pt_admin.pt_id'), nullable=False, index=True)
    ad = db.relationship('TAd', backref='t_ad_check_records')
    pt = db.relationship('TPtAdmin',  backref='t_ad_check_records')



class TAdExpireRenew(db.Model):#广告到期续费表
    __tablename__ = 't_ad_expire_renew'

    ad_renew_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    is_renew = db.Column(db.Integer)
    ad_id = db.Column(db.Integer,db.ForeignKey('t_ad.ad_id'), nullable=False, index=True)

    ad = db.relationship('TAd', backref='t_ad_expire_renews')

class TSup(db.Model):#超级管理员
    __tablename__ = 't_sup'

    sup_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    pwd = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(100), nullable=False,default='超级管理员')




class TAdNew(db.Model):#广告商推送消息
    __tablename__ = 't_ad_news'

    ad_news_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    news_title = db.Column(db.String(50))
    content = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False)
    ad_id = db.Column(db.Integer,db.ForeignKey('t_ad.ad_id'), index=True)
    sup_id = db.Column(db.Integer,db.ForeignKey('t_sup.sup_id'), index=True)

    ad = db.relationship('TAd', backref='t_ad_news')
    sup = db.relationship('TSup', backref='t_ad_news')


class TCompany(db.Model):#品牌公司
    __tablename__ = 't_company'
    company_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    c_name = db.Column(db.String(30))





class TBroker(db.Model):#经纪人
    __tablename__ = 't_broker'

    broker_id = db.Column(db.Integer, primary_key=True,autoincrement=True)#经纪人编号
    b_name = db.Column(db.String(30), nullable=False)#姓名
    sex = db.Column(db.String(30), nullable=False)#性别
    phone = db.Column(db.String(30), nullable=False)#电话
    b_uname = db.Column(db.String(30), nullable=False)#账户
    b_pwd = db.Column(db.String(255), nullable=False)#密码
    Avatar_path = db.Column(db.String(255))#头像
    regi_date = db.Column(db.DateTime, nullable=False)#创建时间
    status = db.Column(db.Integer, nullable=False)#在线状态
    clinch_num = db.Column(db.Integer, nullable=False)#
    sou_num = db.Column(db.Integer, nullable=False)#发布数量
    years = db.Column(db.Integer, nullable=False)#从业年限
    company_id = db.Column(db.Integer,db.ForeignKey('t_company.company_id'), nullable=False, index=True)#关联的公司id

    company = db.relationship('TCompany',  backref='t_brokers',lazy='immediate')

class TSource(db.Model):#新房源信息
    __tablename__ = 't_source'

    source_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    nearby = db.Column(db.String(255))
    region = db.Column(db.String(30), nullable=False)
    hu_type = db.Column(db.String(30))
    price_s = db.Column(db.Float())
    comm_name = db.Column(db.String(30))
    area = db.Column(db.String(30))
    sum_price = db.Column(db.String(30))
    face = db.Column(db.String(30))
    details = db.Column(db.String(255))
    floors = db.Column(db.Integer)
    k_time = db.Column(db.DateTime)
    ch_state = db.Column(db.Integer)
    broker_id = db.Column(db.Integer,db.ForeignKey('t_broker.broker_id'), nullable=False, index=True)

    broker = db.relationship('TBroker', backref='t_sources',lazy='immediate')
class TLandlord(db.Model):#房东信息表
    __tablename__ = 't_landlord'

    ld_id = db.Column(db.Integer, primary_key=True,autoincrement=True)#房东编号
    l_name = db.Column(db.String(30), nullable=False)#房东姓名
    sex = db.Column(db.String(30), nullable=False)#性别
    phone = db.Column(db.String(30), nullable=False)#电话
    l_uname = db.Column(db.String(30), nullable=False)#账号
    l_pwd = db.Column(db.String(100), nullable=False)#密码
    Avatar_path = db.Column(db.String(255),default='')#头像
    regi_date = db.Column(db.DateTime, nullable=False)#创建时间
    last_date = db.Column(db.DateTime, nullable=False)#修改时间
    status = db.Column(db.Integer, nullable=False)#在线状态，默认给个1
    sou_num = db.Column(db.Integer, nullable=False)#发布房源数
    mes_text = db.Column(db.String(255))#推送消息
    mes_title = db.Column(db.String(100))#推送消息标题

class TUser(db.Model):#***********用户表
    __tablename__ = 't_user'

    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)#用户id
    sex = db.Column(db.String(30), nullable=False)#性别
    phone = db.Column(db.String(30), nullable=False)#电话
    Avatar_path = db.Column(db.String(255))#头像地址
    u_name = db.Column(db.String(50), nullable=False)#用户名
    u_pwd = db.Column(db.String(255), nullable=False)#密码
    status = db.Column(db.Integer, nullable=False)#在线状态，默认给个1，表示在线
    balance = db.Column(db.Float(asdecimal=True), nullable=False)#账户余额
    regi_date = db.Column(db.DateTime, nullable=False)#注册时间
    last_date = db.Column(db.DateTime, nullable=False)#修改时间
    times = db.Column(db.Integer)#分享次数
    code = db.Column(db.String(20))#推荐码
    code_num = db.Column(db.Integer)#推荐成功次数
    mes_text = db.Column(db.String(50))
    mes_title = db.Column(db.String(255))

class TSecondSource(db.Model):#二手房源信息表
    __tablename__ = 't_second_source'

    source2_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    img_url = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime, nullable=False)
    nearby = db.Column(db.String(50))
    region = db.Column(db.String(50))
    hu_type = db.Column(db.String(50))
    price_s = db.Column(db.Integer)
    comm_name = db.Column(db.String(30))
    area = db.Column(db.Float())
    sum_price = db.Column(db.Float())
    dis_price = db.Column(db.Float())
    sell_rent = db.Column(db.String(30))
    rent_money = db.Column(db.Float())
    face = db.Column(db.String(30))
    details = db.Column(db.String(255))
    floors = db.Column(db.Integer)
    ch_state = db.Column(db.Integer)
    fav_num = db.Column(db.Integer)
    comment_num = db.Column(db.Integer)
    shared_num = db.Column(db.Integer)
    broker_id = db.Column(db.Integer,db.ForeignKey('t_broker.broker_id'), index=True)
    ld_id = db.Column(db.Integer,db.ForeignKey('t_landlord.ld_id'), index=True)
    title = db.Column(db.String(100))

    broker = db.relationship('TBroker', backref='t_second_sources',lazy='immediate')
    ld = db.relationship('TLandlord',  backref='t_second_sources',lazy='immediate')


class TCheckHousetie(db.Model):#房源审核记录表
    __tablename__ = 't_check_housetie'

    check_house_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    is_pass = db.Column(db.Integer, nullable=False)
    pt_id = db.Column(db.Integer,db.ForeignKey('t_pt_admin.pt_id'), index=True)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), index=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), index=True)
    pt = db.relationship('TPtAdmin',  backref='t_check_houseties')
    source2 = db.relationship('TSecondSource',  backref='t_check_houseties')
    source = db.relationship('TSource',  backref='t_check_houseties')



class TCommunity(db.Model):#小区精选
    __tablename__ = 't_community'

    comm_hpk_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), index=True)

    source = db.relationship('TSource',  backref='t_communities')









class TForwardNew(db.Model):#用户推送消息
    __tablename__ = 't_forward_news'

    message_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    mess_title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    sup_id = db.Column(db.Integer,db.ForeignKey('t_sup.sup_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)
    sup = db.relationship('TSup', backref='t_forward_news')
    user = db.relationship('TUser', backref='t_forward_news')







class TNewImgDetail(db.Model):#新房图片详情
    __tablename__ = 't_new_img_details'

    new_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    pic_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    width = db.Column(db.Float(asdecimal=True))
    height = db.Column(db.Float(asdecimal=True))
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), nullable=False, index=True)

    source = db.relationship('TSource', backref='t_new_img_details')



class TNewTransaction(db.Model):#新房交易记录表
    __tablename__ = 't_new_transaction'

    new_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    deposit_amount = db.Column(db.Float(asdecimal=True), nullable=False)
    deposit_date = db.Column(db.DateTime, nullable=False)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    source = db.relationship('TSource', backref='t_new_transactions')
    user = db.relationship('TUser',  backref='t_new_transactions')







class TRentalTransaction(db.Model):#租房定金交易表
    __tablename__ = 't_rental_transaction'

    rental_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    deposit_amount = db.Column(db.Float(asdecimal=True), nullable=False)
    deposit_date = db.Column(db.DateTime, nullable=False)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    source2 = db.relationship('TSecondSource',  backref='t_rental_transactions')
    user = db.relationship('TUser',  backref='t_rental_transactions')



class TReportComplaint(db.Model):#举报投诉表
    __tablename__ = 't_report_complaints'

    report_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String)
    phone = db.Column(db.String(30))
    date = db.Column(db.DateTime, nullable=False)
    is_pass = db.Column(db.Integer, nullable=False)
    pt_id = db.Column(db.Integer,db.ForeignKey('t_pt_admin.pt_id'), index=True)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), index=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    pt = db.relationship('TPtAdmin',  backref='t_report_complaints')
    source2 = db.relationship('TSecondSource',  backref='t_report_complaints')
    source = db.relationship('TSource', backref='t_report_complaints')
    user = db.relationship('TUser', backref='t_report_complaints')



class TSecImgDetail(db.Model):#二手房详情
    __tablename__ = 't_sec_img_details'

    second_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    pic_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    width = db.Column(db.Float(asdecimal=True))
    height = db.Column(db.Float(asdecimal=True))
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), nullable=False, index=True)

    source2 = db.relationship('TSecondSource',  backref='t_sec_img_details')



class TSecondGoodHouse(db.Model):#二手好房推荐
    __tablename__ = 't_second_good_house'

    source2_good_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), index=True)

    source2 = db.relationship('TSecondSource',  backref='t_second_good_houses')



class TSecondHandTransaction(db.Model):#二手房交易记录
    __tablename__ = 't_second_hand_transaction'

    sec_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    deposit_amount = db.Column(db.Float(asdecimal=True), nullable=False)
    deposit_date = db.Column(db.DateTime)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    source2 = db.relationship('TSecondSource',  backref='t_second_hand_transactions')
    user = db.relationship('TUser', backref='t_second_hand_transactions')






class TSelectRentalHouse(db.Model):#精选租房表
    __tablename__ = 't_select_rental_house'

    sselect_good_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'),index=True)

    source2 = db.relationship('TSecondSource',  backref='t_select_rental_houses')



class TServ(db.Model):#客服表
    __tablename__ = 't_serv'

    serv_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    pwd = db.Column(db.String(50))
    name = db.Column(db.String(50))
    ser_phone = db.Column(db.String(50))
    login_state = db.Column(db.Integer)
    type = db.Column(db.String(30), nullable=False)


class TUserVIP(db.Model):#vip登记表
    __tablename__ = 't_user_VIP'

    vip_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    VIP_grade = db.Column(db.Integer)
    integral = db.Column(db.Integer)
class TUserPost(db.Model):#用户发帖表
    __tablename__ = 't_user_post'

    post_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)
    tie_pic = db.Column(db.String(500))
    user = db.relationship('TUser', backref='t_user_posts')

class TUserComment(db.Model):#用户评论表
    __tablename__ = 't_user_comment'

    comment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String, nullable=False)
    comment_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('t_user_post.post_id'), nullable=False, index=True)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), index=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    post = db.relationship('TUserPost',  backref='t_user_comments')
    source2 = db.relationship('TSecondSource', backref='t_user_comments')
    source = db.relationship('TSource', backref='t_user_comments')
    user = db.relationship('TUser', backref='t_user_comments')


class TUserFavourity(db.Model):#用户收藏
    __tablename__ = 't_user_favourity'

    fav_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), index=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    source2 = db.relationship('TSecondSource',  backref='t_user_favourities')
    source = db.relationship('TSource',  backref='t_user_favourities')
    user = db.relationship('TUser',  backref='t_user_favourities')

class TUserHistory(db.Model):#用户浏览记录
    __tablename__ = 't_user_history'

    history_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), index=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    source2 = db.relationship('TSecondSource',  backref='t_user_histories')
    source = db.relationship('TSource',  backref='t_user_histories')
    user = db.relationship('TUser',  backref='t_user_histories')

class TUserIntegral(db.Model):#积分表
    __tablename__ = 't_user_integral'

    integ_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    integral = db.Column(db.Integer)
    VIP_grade = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    user = db.relationship('TUser',  backref='t_user_integrals')

class TUserLd(db.Model):#用户房东聊天历史
    __tablename__ = 't_user_ld'

    user_ld_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    ld_id = db.Column(db.Integer,db.ForeignKey('t_landlord.ld_id'), index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), index=True)

    ld = db.relationship('TLandlord',  backref='t_user_lds')
    user = db.relationship('TUser',  backref='t_user_lds')

class TUserRecharge(db.Model):#冲值表
    __tablename__ = 't_user_recharge'

    recharge_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    recharge_type = db.Column(db.String(50))
    recharge_amount = db.Column(db.Float(asdecimal=True), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    user = db.relationship('TUser',  backref='t_user_recharges')

class TUserServ(db.Model):#用户客服聊天历史
    __tablename__ = 't_user_serv'

    user_serv_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    serv_id = db.Column(db.Integer,db.ForeignKey('t_serv.serv_id'), index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), index=True)

    serv = db.relationship('TServ',  backref='t_user_servs')
    user = db.relationship('TUser',  backref='t_user_servs')
class TUserShare(db.Model):#分享房源
    __tablename__ = 't_user_share'

    share_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    source_id = db.Column(db.Integer,db.ForeignKey('t_source.source_id'), nullable=False, index=True)
    source2_id = db.Column(db.Integer,db.ForeignKey('t_second_source.source2_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.user_id'), nullable=False, index=True)

    source2 = db.relationship('TSecondSource',  backref='t_user_shares')
    source = db.relationship('TSource', backref='t_user_shares')
    user = db.relationship('TUser',  backref='t_user_shares')
class TWheelPic(db.Model):#轮播图
    __tablename__ = 't_wheel_pic'

    wheel_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    house_url = db.Column(db.String(255))
    link = db.Column(db.String(255))

class TSysRole(db.Model):
    __tablename__ = 't_sys_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
