import re # For regex stuff
from bs4 import BeautifulSoup # For working with HTML
import pdfkit as pdfkit

def clean_html(html_str):
	soup = BeautifulSoup(html_str, 'html.parser')
	for div in soup.find_all("div", class_=["signature","notice"]):	# Removing all div elements with class "signature" or "notice" ("notice" seems to be used for indicating when a post has been edited)
		div.decompose()
	for div in soup.find_all("div", id=re.compile(r'(div_post_reput\d+|list_thanks\d+)')):	# Removing all div elements with IDs that match the given regex
		div.decompose()
	for ul in soup.find_all("ul", "post-buttons"):	# Removing post buttons (e.g. the quote button)
		ul.decompose()
	for span in soup.find_all("span", "spoiler-status"):	# Removing the spoiler status indicators
		span.decompose()
	for div in soup.find_all("div", class_ = "online"):	# Removing the online indicators for users
		div['class'].remove("online")
	return str(soup)

class CrawlPhpBbForumPipeline(object):
	topic_title = None
	topic_url = None
	stylesheets_html_str = None
	posts_html_strs = []

	def process_item(self, item, spider):
		if self.topic_title is None:
			self.topic_title = item['topic_title']
		if self.topic_url is None:
			self.topic_url = item['topic_url']
		if self.stylesheets_html_str is None:
			self.stylesheets_html_str = item['stylesheets_html_str']
		self.posts_html_strs.append(item['posts_html_str'])
		return item

	def close_spider(self, spider):
		n = "\n"
		title_post_html_str = f'<div class="post bg2"><div class="inner"><h3 style="font-size:2.05em; text-align:center;">{self.topic_title}</h3></div><br><div style="width:100%;text-align:center;font-size:1.5em;padding-bottom:10px;">{self.topic_url}</div></div>'
		body_html_str = f"{title_post_html_str}{n}{n.join(self.posts_html_strs)}{n}"
		post_width_px = spider.settings.get("POST_WIDTH_PX", None)	# Default to None if no value is defined for the setting
		post_alignment = spider.settings.get("POST_ALIGNMENT", None)	# Default to None if no value is defined for the setting
		if post_width_px is not None:	# If POST_WIDTH_PX is specified, set the width of the posts in the HTML document; otherwise, do not set the width.
			post_container_inline_style_str = f"width:{post_width_px}px;"
			if (post_alignment is None) or (post_alignment == "left"):
				post_container_inline_style_str = post_container_inline_style_str + "margin-right:auto;"
			elif post_alignment == "center":
				post_container_inline_style_str = post_container_inline_style_str + "margin-left:auto;margin-right:auto;"
			elif post_alignment == "right":
				post_container_inline_style_str = post_container_inline_style_str + "margin-left:auto;"
			else:
				raise Exception("Should not be in this state as a check should have occurred on the parameters before reaching this point.")
			body_html_str = f"<div style='{post_container_inline_style_str}'>{body_html_str}</div>"
		html_str = clean_html(f"<html>{n}<head>{n}{self.stylesheets_html_str}{n}</head>{n}<body>{n}{body_html_str}</body>{n}</html>")

		# It shouldn't be necessary to specify default settings here since it's handled elsewhere
		output_filename = spider.settings.get("OUTPUT_FILENAME", 'Thread')
		output_filetype = spider.settings.get("OUTPUT_FILETYPE", 'pdf')
		full_output_filename = output_filename + "." + output_filetype
		if output_filetype == 'pdf':
			pdfkit.from_string(html_str, full_output_filename)
		elif output_filetype == 'html':
			f = open(full_output_filename, 'w')
			f.write(html_str)
			f.close()
		else:
			raise Exception("Should not be in this state as a check should have occurred on the parameters before reaching this point.")
		
		print(f"\nSuccessfully exported the requested thread to '{full_output_filename}' .")