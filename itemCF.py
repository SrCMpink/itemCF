#coding=utf-8

#Customer: A B C D E
#Goods:apple beer cup decoration beer = a,b,c,d,e
#     Browse goods / Favorites Goods / Recommended goods / Purchase goods
# A     ab                  cde             bd                  bcd
# B     cde                 bde             ae                  cd
# C     abc                 ce              bc                  ab
# D     a                   de              c                   e
# E     b                   ac              de                  abc
#

#Customer:
customer = ['A','B','C','D','E']

#Customer:
store = ['a','b','c','d','e']

#Browse goods
Cus_Brow_Goods = ['A,1,a','A,1,b','B,1,c','B,1,d','B,1,e','C,1,a','C,1,b','D,1,c','D,1,a','E,1,b']

#Favorites goods:
Cus_Fav_Goods = ['A,1,c','A,1,d','A,1,e','B,1,b','B,1,d','B,1,e','C,1,c','C,1,e','D,1,d','D,1,e','D,1,a','E,1,c']

#Recommended goods:
Cus_Rec_Goods = ['A,1,b','A,1,d','A,1,a','B,1,e','C,1,b','C,1,c','D,1,c','E,1,d','E,1,e']

#Purchase goods:
Cus_Purc_Goods = ['A,1,b','A,1,c','A,1,d','B,1,c','B,1,b','C,1,a','C,1,b','D,1,e','E,1,a','E,1,b','E,1,c']

#data
uid_score_bid = [Cus_Brow_Goods, Cus_Fav_Goods, Cus_Rec_Goods, Cus_Purc_Goods]
# uid_score_bid = ['A,1,a','A,1,b','A,1,d','B,1,b','B,1,c','B,1,e','C,1,c','C,1,d','D,1,b','D,1,c','D,1,d','E,1,a','E,1,d']

import math

class ItemBasedCF:
    def __init__(self,train_file):
        self.train_file = train_file
        self.readData()

    #读入数据
    def readData(self):
        self.train = dict()
        for line in self.train_file:
            user,score,item = line.strip().split(",")
            self.train.setdefault(user,{})
            self.train[user][item] = int(float(score))
        print (self.train)


    #协同过滤
    def ItemSimilarity(self):
        C = dict()
        N = dict()
        for user, items in self.train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                C.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1 / math.log(1 + len(items) * 1.0) #IUF （ Inverse User Frequence ）
        print ('N:', N)
        print ('C:', C)

        self.W = dict()
        self.W_max = dict()
        for i, related_items in C.items():
            self.W.setdefault(i, {})

            for j, cij in related_items.items():
                self.W_max.setdefault(j, 0.0)
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
                if self.W[i][j] > self.W_max[j]:
                    self.W_max[j] = self.W[i][j]
        print('W:', self.W)
        for i, related_items in C.items():
            for j, cij in related_items.items():
                self.W[i][j] = self.W[i][j] / self.W_max[j]

        print ('W_max:', self.W_max)
        for k, v in self.W.items():
            print (k + ':' + str(v))

        return self.W


    #向用户推荐商品
    def Recommend(self,user,K=3,N=10):
        rank = dict()
        action_item = self.train[user]
        for item,score in action_item.items():
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
                if j in action_item.keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])


if __name__ == '__main__':

    recommedCustomer = dict()
    for data in uid_score_bid:
        Item = ItemBasedCF(data)
        Item.ItemSimilarity()

        for i in customer:
            recommedDic = Item.Recommend(i)  #计算给用户A的推荐列表
            for k,v in recommedDic.items():
                if recommedCustomer.has_key(k) == False:
                    recommedCustomer.setdefault(k, {})
                if recommedCustomer[k].has_key(i) == False:
                    recommedCustomer[k].setdefault(i,0)
                recommedCustomer[k][i] += 1
        print (recommedCustomer)

    rank = dict()
    for item in store:
        print '\n' "向商家" + item + "推荐"
        for j, wj in sorted(recommedCustomer[item].items(), key=lambda x: x[1], reverse=True)[0:2]:
            print j,
