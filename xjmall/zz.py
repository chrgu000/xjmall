# -*- coding: utf-8 -*-

#
# import M2Crypto
#
# SignEVP = M2Crypto.EVP.load_key('test.pem')
# SignEVP.sign_init()
# SignEVP.sign_update('1234567890123456789012345678901234567890')
# StringSignature = SignEVP.sign_final()
# a = StringSignature.encode('base64')
# print a


# PubKey = M2Crypto.RSA.load_pub_key('test.pem')
# VerifyEVP = M2Crypto.EVP.PKey()
# VerifyEVP.assign_rsa(PubKey)
# VerifyEVP.verify_init()
# VerifyEVP.verify_update('1234567890123456789012345678901234567890')
# print VerifyEVP.verify_final(StringSignature)

# a = []
# print bool(a)


# import xlwt
# workbook = xlwt.Workbook(encoding='utf-8')
# worksheet = workbook.add_sheet('My Worksheet')
#
# style1 = xlwt.XFStyle()
# al = xlwt.Alignment()
# al.horz = 0x02      # 设置水平居中
# al.vert = 0x01      # 设置垂直居中
# style1.alignment = al
# font = xlwt.Font()
# font.bold = True
# font.height = 0x00E8
# style1.font = font
#
# style2 = xlwt.XFStyle()
# al = xlwt.Alignment()
# al.horz = 0x02      # 设置水平居中
# al.vert = 0x01      # 设置垂直居中
# style2.alignment = al
#
# worksheet.write_merge(0,0,0,5,u'新疆润滑油分公司促销品申请单',style1)
# worksheet.write(1,4,u'编号')
# worksheet.write(1,5,u'01')
# worksheet.write(2,0,u'申请人')
# worksheet.write(2,1,u'王磊')
# worksheet.write(2,2,u'日期')
# worksheet.write(2,3,u'2019-2-11')
# worksheet.write(2,4,u'销售组')
# worksheet.write(3,0,u'申请事由')
# worksheet.write_merge(3,3,1,5,u' ')
# worksheet.write_merge(4,17, 0,5, u'乌鲁木齐市希尔顿大酒店二楼会议室召开昆仑润滑超长里程解决方案发布会需领取促销品',style2)
# worksheet.write(18,0,u'促销品领取名称')
# worksheet.write(18,1,u'单位')
# worksheet.write(18,2,u'类型')
# worksheet.write(18,3,u'数量')
# worksheet.write_merge(18,18,4,5,u'领取人签名')
# # for i in range(19,)
# workbook.save('Excel_Workbook2.xls')
# virtual_type =None
# print virtual_type==0 or virtual_type==1

# x = 1

b = lambda x :True if x==1 else False
print b(2)



