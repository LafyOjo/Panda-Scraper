import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

class JobSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        'https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10',
    ]

    def parse(self, response):
        for job in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'title': job.css('a.jobtitle::text').extract_first(),
                'company': job.css('span.company::text').extract_first(),
                'location': job.css('div.location::text').extract_first(),
                'salary': job.css('span.salaryText::text').extract_first(),
            }

process = CrawlerProcess()
process.crawl(JobSpider)
process.start()

job_data = pd.DataFrame(JobSpider.job_data)
job_data.to_csv("job_listings.csv", index=False)

print(job_data.groupby(['location']).mean())
