# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from tieba.items import TiebaItem


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/dota2']

    def parse(self, response):
        title_url_list = response.css('.j_th_tit::attr(href)').extract()

        if title_url_list:
            # 遍历每个连接，获取每篇帖子的具体数据
            for title_url in title_url_list:
                yield scrapy.Request(url=parse.urljoin(response.url, title_url), callback=self.parse_detail)
        
        next_page_url = response.css('.next.pagination-item::attr(href)').extract()[0]
        if next_page_url:
            yield scrapy.Request(url=parse.urljoin(response.url, next_page_url), callback=self.parse_detail)
    
    def parse_detail(self, response):
        title = response.css('.core_title_txt.pull-left.text-overflow::text').extract()[0]
        # 获取回复的作者
        author_list = response.css('.p_author_name.j_user_card::text').extract()
        # 获取回复内容
        content_list = response.css('.d_post_content.j_d_post_content').extract()
        # 获取回复时间和楼层

        print ("title: {}, author is {}, content: {}". format(title, author_list, content_list))

        for i in range(len(author_list)):
            item = TiebaItem()
            item['title'] = title
            item['author'] = author_list[i]
            item['content'] = content_list[i]
            yield item
            