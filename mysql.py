# encoding = utf-8
# =====================================================
#   Copyright (C) 2019 All rights reserved.
#
#   filename : mysql.py
#   version  : 0.1
#   author   : Jack Wang / 544907049@qq.com
#   date     : 2019/11/7 下午 12:03
#   desc     : 用于对数据库进行操作
# =====================================================
import random
import sqlite3

# import configparser

# # 读取config
# conf = configparser.ConfigParser()
# conf.read('config.ini', encoding="utf-8-sig")
# items = conf.get("DETAIL", "columns").split('，')
import time

import bills


def init_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''create table user_tb(
        _id integer primary key autoincrement,
        name text,
        phone text,
        card integer,
        balance double,
        type text
        )''')

    c.execute('''create table bill_tb(
           _id integer primary key autoincrement,
           time text,
           type text,
           cost text,
           balance double,
           name text,
           phone text,
           card integer,
           id integer
           )''')

    c.execute('''create table balance_tb(
           _id integer primary key autoincrement,
           time text,
           balance double
           )''')

    c.execute('''create table system_tb(
           _id integer primary key autoincrement,
           current_card text
           )''')

    c.execute('insert into system_tb values(null, ?)', (' '))

    c.execute('insert into balance_tb values(null, ?, ?)', ('0', '0'))
    conn.commit()
    c.close()
    conn.close()


def table_exist(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("select count(*)  from sqlite_master where type='table' and name = '" + table_name + "';")
    result = c.fetchall()
    conn.commit()
    c.close()
    conn.close()

    if result[0][0] == 1:
        return True
    else:
        return False


def insert(table, *arg):
    """
    向表中插入数据
    :param table:
    :param arg:
    :return:
    """
    pass


def add_person(name, phone, card, balance, type):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('insert into user_tb values(null, ?, ?, ?, ?, ?)',
              (name, phone, card, balance, type))
    conn.commit()

    c.close()
    conn.close()


def del_person(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('select * from user_tb where _id = ' + id)
    result = c.fetchall()
    if result:
        print(result[0][0])
        c.execute('delete from user_tb where _id = ' + str(result[0][0]))
        conn.commit()
    c.close()
    conn.close()


def query(table, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('select * from ' + table + ' where +' + key + ' = ' + value)
    result = c.fetchall()
    c.close()
    conn.close()
    if result:
        return result
    return None


def query_str(table, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('select * from ' + table + ' where +' + key + ' = "' + value + '"')
    result = c.fetchall()
    c.close()
    conn.close()
    if result:
        return result
    return None


def like(table, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('select * from ' + table + ' where +' + key + ' like "%' + value + '%"')
    result = c.fetchall()
    c.close()
    conn.close()

    return result


def max(table):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT MAX(card) FROM ' + table)
    result = c.fetchall()
    c.close()
    conn.close()

    return result


def update(id, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('update user_tb set ' + key + ' = "' + value + '" where _id = ' + id)
    conn.commit()
    c.close()
    conn.close()


def add_bill(time, type, cost, balance, name, phone, card, id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('insert into bill_tb values(null, ?, ?, ?, ?, ?, ?, ?, ?)',
              (time, type, cost, balance, name, phone, card, id))
    conn.commit()
    c.close()
    conn.close()


def update_bill(id, key, value):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('update bill_tb set ' + key + ' = "' + value + '" where id = ' + id)
    conn.commit()
    c.close()
    conn.close()


def change_balance(time, balance):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('update balance_tb set balance =?,time =? where _id = 1', (balance, time))
    conn.commit()
    c.close()
    conn.close()


def check_table():
    """
    判断table的完整性
    :return:
    """
    if not table_exist('user_tb'):
        return False
    elif not table_exist('balance_tb'):
        return False
    elif not table_exist('bill_tb'):
        return False
    elif not table_exist('system_tb'):
        return False
    return True


def generate_card(type):
    """
    生成会员卡号
    :param type:
    :return:
    """
    pass
#
#
# from tqdm import tqdm
#
# a1 = ['张', '金', '李', '王', '赵', '孙', '刘', '石', '贾', '罗', '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
#       '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝',
#       '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
#
# a2 = ['子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
#       '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
#       '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
#       '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
#       '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
#       '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
#       '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
#       '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
#       '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
#       '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性', '马',
#       '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让', '母',
#       '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军',
#       '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
#       '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
#       '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
#       '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
#       '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运', '及',
#       '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司', '巴',
#       '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形', '影',
#       '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈', '容',
#       '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计', '您',
#       '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻', '统',
#       '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示', '愿',
#       '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社', '算',
#       '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息', '功',
#       '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图', '具',
#       '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引', '食',
#       '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试', '怀',
#       '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除', '跑',
#       '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳', '验',
#       '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡',
#       '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店', '否',
#       '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续',
#       '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索',
#       '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低',
#       '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街',
#       '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律',
#       '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属',
#       '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗',
#       '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差',
#       '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压',
#       '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶',
#       '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨',
#       '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付',
#       '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营',
#       '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊', '降',
#       '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
#       '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预', ]
#
# a = range(13000000000, 17800000000)
# b = random.sample(a, 50)
#
# init_database()
#
# def person_in(cost, name, phone, card, balance, id):
#     # balance = float(mysql.query('balance_tb', '_id', '1')[0][2])
#     # balance -= float(cost)
#     add_bill(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#                    '建户', '+' + str(cost), str(balance), str(name), str(phone), str(card), id)
#
# for i in tqdm(range(50)):
#     j = random.randint(0, 2)
#     if j != 0:
#         x = random.randint(0, len(a1) - 1)
#         y = random.randint(0, len(a2) - 1)
#         z = random.randint(0, len(a2) - 1)
#         name = a1[x] + a2[y] + a2[z]
#     else:
#         x = random.randint(0, len(a1) - 1)
#         y = random.randint(0, len(a2) - 1)
#         name = a1[x] + a2[y]
#
#     add_person(name, b[i], str(i), '0', '')
#     person_in('0', name, b[i], str(i), '0', str(i + 1))
