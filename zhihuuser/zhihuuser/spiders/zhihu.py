# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import json
from ..items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #用户详细信息，并且最后用format匹配出来
    user_url='https://www.zhihu.com/api/v4/members/{url_token}?include={include}'
    url_token='excited-vczh'
    user_query='locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    #用户关注信息
    follows_url='https://www.zhihu.com/api/v4/members/{url_token}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    #用户粉丝信息
    followers_url = 'https://www.zhihu.com/api/v4/members/{url_token}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self): #相当于重写一个请求的url
        #测试用户关注信息
        #url='https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'
        #测试的是用户里面的详细信息
        #url='https://www.zhihu.com/api/v4/members/eudora-68-31/activities?limit=10&after_id=1510978388&desktop=True'
        #用户详细信息
        yield Request(self.user_url.format(url_token=self.url_token,include=self.user_query),callback=self.parse_user)
        #用户关注的信息
        yield Request(self.follows_url.format(url_token=self.url_token,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        #用户粉丝信息
        yield Request(self.followers_url.format(url_token=self.url_token, include=self.followers_query, offset=0, limit=20),callback=self.parse_followers)

    def parse_user(self, response):
        result=json.loads(response.text)  #response获取的是json
        item=UserItem()
        for field in item.fields:  #遍历UserItem里面的Item
            if field in result.keys(): #如果匹配上了
                item[field]=result.get(field)
        yield item

        #对关注的人传入链接后解析
        yield Request(self.follows_url.format(url_token=result.get('url_token'),include=self.follows_query,offset=0,limit=20),self.parse_follows)

        #对粉丝
        yield Request(self.follows_url.format(url_token=result.get('url_token'), include=self.follows_query, offset=0, limit=20),self.parse_followers)

    def parse_follows(self,response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                #print(result)
                #print(result.get('url_token'))
                yield Request(self.user_url.format(url_token=result.get('url_token'),include=self.user_query),self.parse_user)
        #判断分页情况
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            next_page=results.get('paging').get('next')
            yield Request(next_page,self.parse_follows)

    def parse_followers(self,response):
        results=json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                #print(result)
                #print(result.get('url_token'))
                yield Request(self.user_url.format(url_token=result.get('url_token'),include=self.user_query),self.parse_user)
        #判断分页情况
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            next_page=results.get('paging').get('next')
            yield Request(next_page,self.parse_followers)