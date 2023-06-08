import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        pep_urls = response.css(
            '#numerical-index tbody > tr > td > a::attr(href)'
        ).getall()
        for pep_url in pep_urls:
            yield response.follow(
                f'{pep_url}/',
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        data = {
            'number': response.css('''section#pep-page-section header
                                      ul.breadcrumbs li:last-child::text'''
                                   ).get().strip('PEP '),
            'name': response.css('''section#pep-content
                                    h1.page-title::text''').get(),
            'status': response.xpath('''//dt[contains(text(), "Status")]
                                        /following-sibling::dd[1]
                                        /abbr/text()''').get()
        }
        yield PepParseItem(data)
