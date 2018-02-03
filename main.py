from src.SACache import SACache

#criar estrutura
#cria l1d a=8, l=64, c=32KB, n=64 (lookup 6, offset 6, tag 20)
x = cl1d = SACache(32768, 8, 64)
print(x.getTamLookup(), x.getTamOffset(), x.getTamTag())

#cria l1i a=4, l=64, c=32KB, n=128 (lookup 7, offset 6, tag 19)
x = cl1i = SACache(32768, 4, 64)
print(x.getTamLookup(), x.getTamOffset(), x.getTamTag())

#cria l2 a=8, l=64, c=256KB, n=512 (lookup 9, offset 6, tag 17)
x = cl2 = SACache(262144, 8, 64)
print(x.getTamLookup(), x.getTamOffset(), x.getTamTag())

#cria l3 a=16, l=128, c=8MB, n=4096 (lookup 12, offset 7, tag 13)
x = cl3 = SACache(8388608, 16, 128)
print(x.getTamLookup(), x.getTamOffset(), x.getTamTag())