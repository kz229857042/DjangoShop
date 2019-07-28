from alipay import AliPay

# 公钥
alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA+og6K1NnBIREA61pVM1Kqin4tGCugPMOpkV5+zDXheBJl9+LprQXlc+G62uar5amL6Nka0Rdd/EGsj9IGQvo8hrIoP70KxG3gl0phEIRohLDaqOPr1Uj4rlalSRaehNie0r8Etnj+bBHFsVJ+yQgYrq9g6E6whaGBw004ezSGmUCj1J++GL2SSq6U9qcL1N4C77LUlkEVT0wF7H+H91BZAFgzp04lgE8rdpsRe+pvGHknA+n0LAoHZwcqMuDztxYztye/IKA00GX7OvqGCl6xUoy1t2/4Y3is+ztd7MwTMAdZVZ1UhKcEiQkwUY7We8T9n74eD2++itQBfUkepQR1wIDAQAB
-----END PUBLIC KEY-----"""

# 私钥
app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA+og6K1NnBIREA61pVM1Kqin4tGCugPMOpkV5+zDXheBJl9+LprQXlc+G62uar5amL6Nka0Rdd/EGsj9IGQvo8hrIoP70KxG3gl0phEIRohLDaqOPr1Uj4rlalSRaehNie0r8Etnj+bBHFsVJ+yQgYrq9g6E6whaGBw004ezSGmUCj1J++GL2SSq6U9qcL1N4C77LUlkEVT0wF7H+H91BZAFgzp04lgE8rdpsRe+pvGHknA+n0LAoHZwcqMuDztxYztye/IKA00GX7OvqGCl6xUoy1t2/4Y3is+ztd7MwTMAdZVZ1UhKcEiQkwUY7We8T9n74eD2++itQBfUkepQR1wIDAQABAoIBAQCziDPHIHlOb0oeKIK21naPAozLFg13MrZoyJjlPNb1hQi34OY+jAfqv1C8G9w5wAdPVBN+GvuwG/Tkfxy3diV0eWUUmh93TbbnoMNDl+Ty8+c93//zcVvJ+XHENszvdjy4hb+l8qbAI2aOFssxQW5D0fZFAaENvP5Gx1wCGqdlaVozgtNMB5VcIvjEH5evByR34YQ4Ovoj9lOZ0Jbw359y59Sq+OwZkezLrePecBYQ9aVoGXxM8s3qldYuYEPdKRPVbpstjDnW8B7+dpl1LZvmfDDB5AKX1YYPiIyRlb5yzPbu5y12jTXK0gdL3+gv+Jg2Vt0HpLcGV3XT2pSOhkKhAoGBAP/13gvZ+mheb1PXdIdrNu4bdUMq1FIM/JIOuDW1ObZ7NVcncJOEzenleWJlzFgkg/z3OOszRiwC2nYDvltnMd6sN1y2mBOXHT0PjgP7IEe+2cZc6K4qW0ttqNbkNgRAwVINvNT0jbUmngeOPXHsRTELhYwYuDeMem6IjKh31lb1AoGBAPqSJRyV0Bf7IHTnPG/IgB7BfDQiYILBZHy3xt3Xg4LI1h0LEkRf/SZFq/ADqCVCl9uTqdGIjXG1FgcramxAQtZq7yCVzwAtG8DvyE1xiAFPyX83aFJ5YgEPuFihYyNSgy2oJ3WC2s7C1rYv67M1+Nv33Y+0Ihap5l1tW7R/qY4bAoGAXGX7NDgKBycf9Rov/LqdZ7MNz6NkZgI+ItOhd/Hl1ZQAm2enYfltA+RMv1KUQ7Va2DS+nVkzGawmBLgxPXmxLPrqOVPI7jl82pAE6jb7XirtHohnjofH0SDS9FAJl9twbhh7dDyb8yrvnTahw8BQ8fWAziQWTCcwAzrT2/T2sQkCgYA2jyfhh4VeE2JH0inItUGgcMTYnTuifPWiamm02D5cddqZTFXX6Ya3lKgRhNpR8qQaPZbWdwNFZQa83Ok5VOy4v2P+FmCSS0AlzJAyvKu+jV70gl4Gx0Nds8ySD+IESO0jPeAJqEp4htg1p02NIg1j6B6oMbLSeIAei7dSIBINTQKBgQDMamE7O8u7gNttruvPak4pVDz0arIrAd8qZhri/EqjpoR4vUZVFZxkKJHgRkVvNcZ3YFPyAN/M05iVR/ijF9mzAgKn3kEeZG/D8vykfswKBEG3u/grySGUWTqRPcG0/ay5GSblXs7QwQQO1++5jemq/a18GU67uiWcLhFPPbV4lw==
-----END RSA PRIVATE KEY-----"""

# 实例化支付请求
alipay = AliPay(
    appid = "2016101000652509",
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type = "RSA2"
)

# 发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no = '10003', #订单号
    total_amount= str(10000), #支付金额
    subject = '生鲜交易', # 交易主题
    return_url= None,
    notify_url=None
)
print("https://openapi.alipaydev.com/gateway.do?"+order_string)






