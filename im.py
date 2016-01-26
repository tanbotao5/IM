#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
import hashlib
import requests
import json
import traceback


WEEK_DAY =  datetime.timedelta(days = 7)
JSON_HEADER = {'content-type': 'application/json',}
CLIENT_ID  =  'your ID'
CLIENT_SECRET =  'your secret'
URL = 'https://a1.easemob.com/%s/%s/%s'
APPKEY = "your ID"            #环信ID
APPKEY_NAME = "your appname"            #环信app应用名

class huanXingController:
      def __init__ (self):
            pass
      #获取企业token,修饰器其它的获取token操作,  可以用修饰器修饰其它需要token的方法，和环信服务器交互
      def getToken(self):
            try:
                  def wrop(func):
                        def pp(token,this, *args):
                              info = db.Name.objects.get(id = 1)
                              lastTime = info.lastActTime
                              Authorization = info.token                               #获取token
                              if (datetime.datetime.now() - lastTime) > WEEK_DAY:      #判断是否7天有效期
                                    if self.get_AppKey_Token():
                                          Authorization = db.Name.objects.get(id = 1).token   #存储token的地方，获取
                              ret = func(Authorization,this, *args)
                              return ret
                        return pp
                  return wrop
            except:
                  pass
      #获取企业token,和环信服务器交互
      def getUserToken(self):
            try:
                  info = db.Name.objects.get(id = 1)
                  lastTime = info.lastActTime
                  Authorization = info.token                             #获取token
                  if (datetime.datetime.now() - lastTime) > WEEK_DAY:    #判断是否7天有效期
                        if self.get_AppKey_Token():
                              Authorization = db.Name.objects.get(id = 1).token #存储token的地方，获取
                  return  Authorization
            except:
                  pass
            return []
      # 获取环信Token
      def get_AppKey_Token (self, ):
            try:
                  payload = {'grant_type': 'client_credentials', }
                  payload['client_id'] = CLIENT_ID
                  payload['client_secret'] = CLIENT_SECRET
                  url = URL % ( APPKEY, APPKEY_NAME, 'token')
                  auth = ''
                  reponse = requests.post(url, data = json.dumps(payload), headers = JSON_HEADER, auth = auth)
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        token = data["access_token"]
                        try:
                              p = db.Name.objects.get(id = 1)
                              p.token = token
                              p.save()         #同时更新时间
                              return True
                        except:
                              self.log_error()
                              pass
                  return False
            except:
                  self.log_error()
                  pass
      # 注册环信用户
      #@getToken('token')
      def addAppKeyUser (self, users=[{}, ]):  # [{"username":"u1", "password":"p1" ,"nickname":"逆称 "}, {"username":"u2", "password":"p2","nickname":"逆称 "}]
            try:
                  if users:
                        JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                        payload = users
                        url = URL % ( APPKEY, APPKEY_NAME, 'users')
                        reponse = requests.post(url, data = json.dumps(payload), headers = JSON_HEADER, auth = '')
                        if reponse.status_code == requests.codes.ok:
                              data = json.loads(reponse.text)
                              if data["entities"][0]["activated"]:
                                    return True
                        else:
                              return json.loads(reponse.text)
                        return False
            except:
                  self.log_error()
                  pass
      # 删除环信用户
      @getToken('token')
      def del_AppKey_User (self, user=''):  # name
            try:
                  if user:
                        JSON_HEADER['Authorization'] = 'Bearer ' + self
                        payload = user
                        url = URL % ( APPKEY, APPKEY_NAME, 'users')
                        reponse = requests.delete(url, data = json.dumps(payload), headers = JSON_HEADER, auth = '')
                        if reponse.status_code == requests.codes.ok:
                              return True
                        return False
            except:
                  self.log_error()
                  pass

      #群组删除人[批量/单个]
      def delGroupChatUsers(self,groupId ,person ,nameKey):
            try:
                  if nameKey != self.chechGroupOwner(groupId):
                        return False ,u'不好意思!您没有权限进行此操作!'
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId + '/users/' + reduce(lambda x, y: x + ',' + y,person) )
                  reponse = requests.delete(url,headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        if data:
                              return  True ,data['data']
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False ,u'删除不成功！'

      # 系统发送发透传消息.。  环信
      def sendMessageEvent (self, type, receiver_users=[], message={}):  #  type:消息action
            payload = {"target_type": "users", "target": "", "msg": {"type": "cmd", "action": ""}, "from": "", "ext": {"Items":"",}}
            payload["from"] = 'admin'
            payload["target"] = receiver_users
            payload["msg"]["action"] = type
            payload["ext"]["Items"] = message
            try:
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'messages')
                  reponse = requests.post(url, data = json.dumps(payload), headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        return True ,json.loads(reponse.text)
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
      #  添加群组
      @getToken('token')
      def createGroupChat(self, message={}):
            try:
                  JSON_HEADER['Authorization'] = 'Bearer ' + self
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups')
                  try:
                        if not message["maxusers"]:
                              message["maxusers"] = 2000
                  except:
                        pass
                  reponse = requests.post(url, data = json.dumps(message), headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        return True ,data['data']['groupid'],1
                  else:
                        return False,[],json.loads(reponse.text)
                        #return data
            except:
                  self.log_error()
                  pass
            return  False,[],u'创建不成功！'

      #   修改群组信息
      @getToken('token')
      def updateGroupChat(self,groupId, message={}):
            try:
                  JSON_HEADER['Authorization'] = 'Bearer ' + self
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId)
                  reponse = requests.put(url, data = json.dumps(message), headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        if data:
                              return  True,u'修改成功！'
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False,u'修改不成功！'

       #获取群组信息
      @getToken('token')
      def getGroupChatInfo(self,groupId):
            try:
                  groupinfo = {"groupname":"","description":"","maxusers":0,}
                  JSON_HEADER['Authorization'] = 'Bearer ' + self
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId)
                  reponse = requests.get(url, headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        if data['data']:
                              groupinfo["groupname"] = data['data'][0]["name"]
                              groupinfo["description"] = data['data'][0]["description"]
                              groupinfo["maxusers"] = data['data'][0]["maxusers"]
                              return   True,groupinfo,1
                        return   True,data['data'],1
                  else:
                        return False,[],json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False,groupinfo,u'获取不成功！'


      #   删除群组
      def delGroupChat(self,nameKey,groupId ):
            try:
                  if nameKey != self.chechGroupOwner(groupId):
                        return False ,u'不好意思!您没有权限进行此操作!'
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId)
                  reponse = requests.delete(url, headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        if data["data"]["success"]:
                              removepng = 'rm  ' + ABSPATH + groupId + '.png'
                              os.system(removepng)        # 删除群头像
                              return  True ,u'解散群成功！'
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False,u'解散不成功！'


      #群组易主
      def changeGroupChatAdmin(self,userId,nameKey,groupId ):
            try:
                  name = db.UserInfo.objects.get(user__id = int(userId)).appName
                  print name
                  print self.chechGroupOwner(groupId)
                  if name != self.chechGroupOwner(groupId):
                        return False ,u'不好意思!您没有权限进行此操作!'
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId)
                  reponse = requests.put(url,data = json.dumps({"newowner":nameKey}), headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        if data["data"]["newowner"]:
                              return  True ,u'成功更换群主！'
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False,u' 更换群主不成功！'

      #环信获取群组中的所有成员
      @getToken('token')
      def getGroupChatUsers(self,groupId ):
            try:
                  namekeys = {"owner":'',"members":[]}
                  userList = []

                  JSON_HEADER['Authorization'] = 'Bearer ' + self
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId +'/users')
                  reponse = requests.get(url, headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data =  json.loads(reponse.text)
                        if  data['data']:
                              for item in data['data']:
                                    if 'owner' in item.keys():
                                          namekeys["owner"] = item["owner"]
                                    else:
                                          userList.append(item["member"])
                              namekeys["members"] = userList
                              return True ,namekeys,1
                        return True ,data['data'],1
                  else:
                        return False,namekeys,json.loads(reponse.text)
                  return False,namekeys,0
            except:
                  pass
            return  False,namekeys,u'获取不成功！'

      #获取一个用户参与的所有群组
      @getToken('token')
      def getJoinChatGroups(self,nameKey ):
            try:
                  userList = []
                  JSON_HEADER['Authorization'] = 'Bearer ' + self
                  url = URL % ( APPKEY, APPKEY_NAME, 'users/'+nameKey +'/joined_chatgroups')
                  reponse = requests.get(url, headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data =  json.loads(reponse.text)
                        if  data['data']:
                              for item in data['data']:
                                    namekeys = {"groupid":'',"groupname":""}
                                    namekeys["groupid"] = item["groupid"]
                                    namekeys["groupname"] = item["groupname"]
                                    userList.append(namekeys)
                              return True ,userList,1
                        return True ,userList,1
                  else:
                        return False,userList,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False,userList,u'获取不成功！'

      #群组加人[批量/单个]
      @getToken('token')
      def addGroupChatUsers(self,groupId ,person ):
            try:
                  JSON_HEADER['Authorization'] = 'Bearer ' + self
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId +'/users')
                  reponse = requests.post(url,data = json.dumps( {"usernames":person} ), headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data =  json.loads(reponse.text)
                        if  data:
                              return True ,u'添加成功'
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False ,u'添加不成功！'

      #环信校验权限,是否为群主
      def chechGroupOwner(self,groupId ):
            try:
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId +'/users')
                  reponse = requests.get(url, headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data =  json.loads(reponse.text)
                        if  data['data']:
                              for item in data['data']:
                                    if 'owner' in item.keys():
                                          return item["owner"]
                  return []
            except:
                  self.log_error()
                  pass
            return  []


      #环信 退出群组
      def quitJoinChatGroups(self,groupId ,nameKey):
            try:
                  if nameKey == self.chechGroupOwner(groupId):
                        return False ,u'不好意思!群主不能退群,可以解散群!'
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'chatgroups/'+groupId + '/users/' + nameKey )
                  reponse = requests.delete(url,headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data = json.loads(reponse.text)
                        if data:
                              return  True ,data['data']
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False ,u'退群不成功！'

      #环信 修改用户密码
      def updateUsersAppNamePassword(self,appname ,password ):
            try:
                  JSON_HEADER['Authorization'] = 'Bearer ' + self.getUserToken()
                  url = URL % ( APPKEY, APPKEY_NAME, 'users/' + appname + '/password')
                  reponse = requests.put(url,data = json.dumps( {"newpassword":password} ), headers = JSON_HEADER, auth = '')
                  if reponse.status_code == requests.codes.ok:
                        data =  json.loads(reponse.text)
                        if  data:
                              return True ,u'修改成功'
                  else:
                        return False,json.loads(reponse.text)
            except:
                  self.log_error()
                  pass
            return  False ,u'修改不成功！'
