import scrapy

class TwitchScrapy(scrapy.Spider):
    name = "twitch-spider"
    start_urls = [
        "https://twitch.tv"
    ]

    def parse(self, response):
        streamers = response.xpath('//a[@data-test-selector="ChannelLink"]/text()').extract()
        playings = response.xpath('//a[@data-test-selector="GameLink"]/text()').extract()

        for streamer, playing in zip(streamers, playings):
            yield {
                'streamer': streamer,
                'playing': playing
            }