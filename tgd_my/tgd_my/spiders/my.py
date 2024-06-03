import scrapy


class MySpider(scrapy.Spider):
    name = "my"
    allowed_domains = ["tgd.kr"]
    start_urls = ["https://tgd.kr/member/mylist"]
    tgd_session = None

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            cookies=[
                {"name": "tgdsess", "value": self.tgd_session},
            ],
        )

    def parse(self, response, **kwargs):
        # update tgdsess cookie
        if response.headers.get("tgdsess"):
            self.tgd_session = response.headers["tgdsess"]

        # grab article link
        links = response.css('.mt-2 .table tbody tr td a::attr(href)').extract()
        if len(links) > 0:
            for link in links:
                yield scrapy.Request("https://tgd.kr{}".format(link), callback=self.parse_article)

            next_page = response.css('.mt-2 .pagination li').xpath('.//a[contains(@rel, "next")]/@href').get()
            if next_page:
                yield scrapy.Request(
                    "https://tgd.kr{}".format(next_page), cookies=[{"name": "tgdsess", "value": self.tgd_session}]
                )

    def parse_article(self, response):
        # update tgdsess cookie
        if response.headers.get("tgdsess"):
            self.tgd_session = response.headers["tgdsess"]

        def strip_text(text):
            return text.strip("                \n").strip("\uf27a ")

        # parse id, title, author, time, views, votes, content
        _id = response.css('#article-content::attr(data-id)').get()
        title = ''.join(response.css('#article-info h2::text').getall())
        category = ''.join(response.css('#article-info .category::text').getall())
        author = ''.join(response.css('#article-info-writer strong::text').getall())
        created_at = ''.join(response.css('#article-time span::text').getall())
        views = ''.join(response.css('#article-views::text').getall())
        votes = ''.join(response.css('#article-votes::text').getall())
        content = response.css('#article-content').get()
        image_urls = response.css('#article-content p').xpath(
            './/img[contains(@data-src, "upload.tgd.kr")]/@data-src'
        ).getall()
        image_urls = ["https:{}".format(str(image_url).lstrip('https:')) for image_url in image_urls]

        yield {
            "id": _id,
            "title": strip_text(title),
            "category": strip_text(category),
            "author": strip_text(author),
            "created_at": strip_text(created_at),
            "views": strip_text(views),
            "votes": strip_text(votes),
            "content": content,
            "link": response.url,
            "image_urls": image_urls,
        }
