from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from apiapp.models import *
from tools.serializor import to_json

kfblue = Blueprint('kfblue',__name__)

@kfblue.route('/xf/',methods=["GET"])#新房房源信息，一次20条
def xf():
    pgnum = request.args.get('page',1)
    fangs = TSource.query.all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })

@kfblue.route('/ershou/zu/',methods=["GET"])#二手房租展示
def ershouzu():
    pgnum = request.args.get('page',1)
    fangs = TSecondSource.query.filter_by(sell_rent='租').all()
    if fangs:
        pages = -(-len(fangs)//20)#向上取整,算出总页数
        print('总页为',pages)
        print('您访问的页码为',pgnum)
        if  int(pgnum)>pages:#访问的页码不存在
            return jsonify({
                    'state':0,
                    'msg':'您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            rets = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            rets = to_json(fangs)
        elif pages==int(pgnum):
            rets = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in rets:
            del ret['broker']
            del ret['broker_id']
            del ret['ld']['l_pwd']
            data.append(ret)
        return jsonify({
            'state':1,
            'msg':'返回数据成功',
            'data':data})
    else:
        return jsonify({
            'state':0,
            'msg':'您访问的资源不存在'
        })

@kfblue.route('/ershou/mai/', methods=["GET"])  # 二手房卖展示
def ershoumai():
    pgnum = request.args.get('page', 1)
    fangs = TSecondSource.query.filter_by(sell_rent='卖').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1 <= int(pgnum) < pages:  # 判断页数的范围
            rets = to_json(fangs[(int(pgnum) - 1) * 20:int(pgnum) * 20])
        elif pages == 1:  # 如果只有一页，直接返回
            rets = to_json(fangs)
        elif pages == int(pgnum):
            rets = to_json(fangs[(int(pgnum) - 1) * 20:])  # 返回最后一页数据
        data = []
        for ret in rets:
            del ret['ld']
            del ret['ld_id']
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })
@kfblue.route('/xf/p1/')#新房单价小于等于9000的接口
def xinfangp1():
    pgnum=request.args.get('page',1)
    fangs=TSource.query.filter(TSource.price_s.__le__(9000)).all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })
@kfblue.route('/ershou/zu/p1/')#二手房租房单价小于等于2000的接口
def ershouzup1():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(TSecondSource.rent_money.__le__(2000),TSecondSource.sell_rent=='租').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['broker']
            del ret['broker_id']
            del ret['ld']['l_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })
@kfblue.route('/ershou/mai/p1/')#二手房出售单价小于等于8000的接口
def ershoumaip1():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(TSecondSource.price_s.__le__(8000),TSecondSource.sell_rent=='卖').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['ld']
            del ret['ld_id']
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })
@kfblue.route('/ershou/mai/h1/')#二手房出售2室的
def ershoumaih1():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(TSecondSource.hu_type.startswith('2室'),TSecondSource.sell_rent=='卖').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['ld']
            del ret['ld_id']
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })
@kfblue.route('/ershou/mai/h2/')#二手房出售3室的
def ershoumaih2():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(TSecondSource.hu_type.startswith('3室'),TSecondSource.sell_rent=='卖').all()
    print(fangs)
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['ld']
            del ret['ld_id']
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })
@kfblue.route('/ershou/mai/h1h2/')#二手房出售3室或2室的
def ershoumaih1h2():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(or_(TSecondSource.hu_type.startswith('3室'),TSecondSource.hu_type.startswith('2室')),TSecondSource.sell_rent=='卖').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['ld']
            del ret['ld_id']
            del ret['broker']['b_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })



@kfblue.route('/ershou/zu/h1/')#二手房租2室的
def ershouzuh1():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(TSecondSource.hu_type.startswith('2室'),TSecondSource.sell_rent=='租').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['broker']
            del ret['broker_id']
            del ret['ld']['l_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })


@kfblue.route('/ershou/zu/h2/')#二手房租3室的
def ershouzuh2():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(TSecondSource.hu_type.startswith('3室'),TSecondSource.sell_rent=='租').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['broker']
            del ret['broker_id']
            del ret['ld']['l_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })

@kfblue.route('/ershou/zu/h1h2/')#二手房租3室或2室的
def ershouzuh1h2():
    pgnum=request.args.get('page',1)
    fangs=TSecondSource.query.filter(or_(TSecondSource.hu_type.startswith('3室'),TSecondSource.hu_type.startswith('2室')),TSecondSource.sell_rent=='租').all()
    if fangs:
        pages = -(-len(fangs) // 20)  # 向上取整,算出总页数
        print('总页为', pages)
        print('您访问的页码为', pgnum)
        if int(pgnum) > pages:  # 访问的页码不存在
            return jsonify({
                'state': 0,
                'msg': '您访问的资源不存在'
            })
        elif 1<=int(pgnum)<pages:#判断页数的范围
            res = to_json(fangs[(int(pgnum)-1)*20:int(pgnum)*20])
        elif pages==1:#如果只有一页，直接返回
            res = to_json(fangs)
        elif pages==int(pgnum):
            res = to_json(fangs[(int(pgnum)-1)*20:])#返回最后一页数据
        data=[]
        for ret in res:
            del ret['broker']
            del ret['broker_id']
            del ret['ld']['l_pwd']
            data.append(ret)
        return jsonify({
            'state': 1,
            'msg': '返回数据成功',
            'data': data})
    else:
        return jsonify({
            'state': 0,
            'msg': '您访问的资源不存在'
        })