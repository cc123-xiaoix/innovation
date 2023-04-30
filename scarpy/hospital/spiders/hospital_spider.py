import scrapy
from hospital.items import HospitalItem


class HospitalSpiderSpider(scrapy.Spider):
    name = 'hospital_spider'
    allowed_domains = ['www.haodf.com']
    #start_urls = ['https://www.haodf.com/hospital/list-11.html']
    offset = 11
    base_urls = 'https://www.haodf.com/hospital/list-'
    start_urls = [base_urls+str(offset) +'.html']

    def parse(self, response):       
        hospital_list = response.xpath("//div[@class='m_box_green']//div[@class='ct']//li")

        for i_item in hospital_list:
            hospital_item = HospitalItem()
            
            hospital_item['name'] = i_item.xpath(".//a//text()").extract_first()
            hospital_item['hospital_rank'] = i_item.xpath(".//span//text()").extract_first()

            #print(hospital_item)
            yield hospital_item
 
        self.offset +=1
        if self.offset == 16:
            self.offset = 21
            yield scrapy.Request(self.base_urls+str(self.offset)+'.html',callback=self.parse)
        elif self.offset == 24:
            self.offset = 31
            yield scrapy.Request(self.base_urls+str(self.offset)+'.html',callback=self.parse)
        elif self.offset == 38:
            self.offset = 41
            yield scrapy.Request(self.base_urls+str(self.offset)+'.html',callback=self.parse)
        elif self.offset == 47:
            self.offset = 50
            yield scrapy.Request(self.base_urls+str(self.offset)+'.html',callback=self.parse)
        elif self.offset == 55:
            self.offset = 61
            yield scrapy.Request(self.base_urls+str(self.offset)+'.html',callback=self.parse)
        elif self.offset == 66:
            return
        else:
            yield scrapy.Request(self.base_urls+str(self.offset)+'.html',callback=self.parse)
         
        # next_link = response.xpath("//div[@class='m_box_green']//div[@class='ct']//li/a/@href").extract()
        # if next_link:
        #     next_link = next_link[0]
        #     yield scrapy.Request("https://www.haodf.com/hospital/list-11.html"+next_link,callback=self.parse)
 