import scrapy
from urllib.parse import urlparse, ParseResult, parse_qs

def stripUrlParameter(urlStr, attributeToRemove):
    u = urlparse(urlStr)
    
    params = parse_qs(u.query)
    if attributeToRemove in params:
        del params[attributeToRemove]
    
    queryStr = ""
    for key, value in params.items():
        queryStr = queryStr + key + "=" + value[0] + "&"
    queryStr = queryStr[0:-1]
    
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=queryStr, fragment=u.fragment)
    return res.geturl()

def get_open_spoilers_html(html_str):
	html_str = html_str.replace('<div class="spoiler_content" hidden="until-found">', '<div class="spoiler_content hidden">')
	return html_str

def post_html_helper(sel_arr):
	post_html_strs = []
	for sel in sel_arr:
		html_str = sel.get()
		is_post_div = True if html_str.find('<div id="p') != -1 else False
		is_fake_post_div = True if html_str.find('"<div id="p0"') != -1 else False
		if is_post_div and (not is_fake_post_div):
			post_html_strs.append(html_str)
	return post_html_strs

def get_next_page_url(response):
	pag_img_sels = response.css("a.pag-img")
	for sel in pag_img_sels:
		if len(sel.css('img[alt="Next"]')) != 0:
			return sel.css("a").xpath("@href").get()
	return -1

def get_html_styles(response):
	external_stylesheets = ['<link rel="stylesheet" href="' + rel_link + '">' for rel_link in response.css('link[rel="stylesheet"]::attr(href)').getall()]
	other_styles = response.css('style').getall()
	return external_stylesheets + other_styles

class PhpBbThreadSpider(scrapy.Spider):
	name = "PhpBbThreadSpider"

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		print("Reading:\t" + response.url)

		base_tag = f'<base href="{response.url[:response.url.rfind("/")+1]}">'
		topic_title = response.css("h2.topic-title").css("a::text").get()
		topic_url = response.urljoin(stripUrlParameter(stripUrlParameter(response.css("h2.topic-title").css("a").xpath("@href").get(), "sid"), "start"))
		stylesheets_html_str = '\n'.join([base_tag] + get_html_styles(response))
		posts_html_str = get_open_spoilers_html('\n'.join(post_html_helper(response.css("div.post:not(.post--0)"))))	# The post--0 class corresponds to "Sponsored Content" posts

		yield {'topic_title' : topic_title, 'topic_url' : topic_url, 'stylesheets_html_str' : stylesheets_html_str, 'posts_html_str' : posts_html_str}

		next_page_url = get_next_page_url(response)
		if next_page_url != -1:
			next_page_url = response.urljoin(stripUrlParameter(next_page_url, "sid"))
			yield scrapy.Request(next_page_url, callback=self.parse)