import logging

from bs4 import BeautifulSoup

from core.models import ContentSearchIndex, ImageSearchIndex, SiteSearchIndex
from crawler.models import CrawlerPages

logger = logging.getLogger("django")
search_index_content = ContentSearchIndex.objects.using('search_db').all()
crawler_pages = CrawlerPages.objects.using('crawler_db').all()
image_search_index = ImageSearchIndex.objects.using('search_db').all()
site_search_index = SiteSearchIndex.objects.using('search_db').all()


def crawl_page_content(crid: int) -> None:
	"""
	Taking id from view where content was scrubbed and added no DB.
	Here function will 'ask' other functions to clean data, and then collect all the necessary page content,
	like title, keywords, etc.
	Also here we can update site content
	:param crid:
	:return:
	"""
	url = crawler_pages.get(id=crid).cr_url
	if search_index_content.filter(crawler_fk_pages=crid).exists():
		try:
			crawl_images_alt(idi=crid)
			#video(vid_id=crid)
			search_index_content.filter(crawler_fk_pages=crid).update(url=url, title=crawl_title(crid),
			                                                          keywords=crawl_keyword(idl=crid),
			                                                          description=crawl_desc(id_desc=crid),
			                                                          site_lang=crawl_lang(crid),
			                                                          site_content=crawl_content(crid),
			                                                          crawler_fk_pages=crid, status=1)
		except Exception as ex:
			logger.exception("Crawler, tasks, crawl_page_content (if statement), exception: %s", ex)
	else:
		try:
			crawl_images_alt(idi=crid)
			#video(vid_id=crid)
			sic = search_index_content.create(url=url, title=crawl_title(crid), keywords=crawl_keyword(idl=crid),
			                                  description=crawl_desc(id_desc=crid), site_lang=crawl_lang(crid),
			                                  site_content=crawl_content(crid), crawler_fk_pages=crid)
			sic.save(using='search_db')
		except Exception as ex:
			logger.exception("Crawler, tasks, crawl_page_content (else statement), exception %s", ex)


def video(vid_id):
	"""
	To be continue...
	:param vid_id:
	:return:
	"""
	to_crawl = crawler_pages.get(id=vid_id)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	# List of all video tag
	video_tags = soup.find_all('video')
	for video_tag in video_tags:
		# video_url = video_tag.find("a")['href']
		print(video_tag)


def add_site_to_search(site_url: str) -> None:
	"""
	Adding site URL to DB for indexing and searching
	:param site_url:
	:return: None
	"""
	if not site_search_index.filter(site_url=site_url).exists():
		try:
			site_search_index.create(site_url=site_url).save(using='search_db')
		except Exception as ex:
			logger.exception("Crawler, tasks, add_site_to_search exception %s", ex)
	else:
		print(str(site_url))


def crawl_images_alt(idi: int) -> None:
	"""
	This is The toughest function.
	Various conditions to take image url address, lack of image 'alt' attribute, etc.

	:param idi:
	:return: None
	"""
	to_crawl = crawler_pages.get(id=idi)
	# print("to crawl_images_alt", to_crawl)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	for img in soup.find_all('img'):
		if str(img.get('src')).startswith('data:'):
			img_src = str(img.get('data-src'))
		else:
			img_src = str(img.get('src'))
		image_alt = str(img.get('alt'))
		if len(image_alt) == 0:
			logger.info("Crawler, tasks, crawl_images_alt name length = 0; url %s, img_src: %s, image alt: %s",
			            to_crawl.cr_url, img_src, image_alt)
		elif image_alt == 'None':
			# image_alt = img_src.split("/")[-1]
			print(img_src, image_alt, idi)
			logger.info("Crawler, tasks, crawl_images_alt name None; url %s, img_src: %s, image alt: %s",
				to_crawl.cr_url, img_src, image_alt)
		elif image_alt.startswith('data:'):
			logger.info("Crawler, tasks, crawl_images_alt name startswith data; url %s, img_src: %s, image alt: %s",
			            to_crawl.cr_url, img_src, image_alt)
		else:
			create_image(img_src, image_alt, idi)


def create_image(img_src: str, image_alt: str, idi: int) -> None:
	"""
	Getting filtered and cleaned data, adding to DB as well as updating
	:param img_src: Image URL address
	:param image_alt: Image keyword
	:param idi: ID of image
	:return:
	"""
	if not image_search_index.filter(img_url=img_src).exists():
		try:
			isi = image_search_index.create(img_url=img_src, img_alt=image_alt, crawler_fk_pages=idi)
			isi.save(using='search_db')
		except Exception as ex:
			logger.exception("Crawler, tasks, create_image, create statement, exception %s", str(ex))
	else:
		try:
			image_search_index.filter(img_url=img_src).update(img_alt=image_alt, crawler_fk_pages=idi)
		except Exception as ex:
			logger.exception("Crawler, tasks, create_image, update statement, exception %s", str(ex))


def crawl_desc(id_desc: int) -> str:
	"""
	Description
	:param id_desc:
	:return: If not description then asking other function to check one more place where it can be stored.
	"""
	to_crawl = crawler_pages.get(id=id_desc)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	try:
		description = soup.find("meta", {"name": "description"})['content']
		return description
	except (Exception, TypeError) as ex_te:
		logger.exception("Crawler, tasks, crawl_desc exception %s", str(ex_te))
		return _get_description_og(id_desc_og=id_desc)


def crawl_content(idc: int) -> str:
	"""
	Cleaning content Here, accuracy of completely and ideally clean content is not so important because
	it will be indexed and all that we need.
	:param idc: ID of content
	:return: string containing content
	"""
	to_crawl = crawler_pages.get(id=idc)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	for s in soup.select('footer'):
		s.extract()
		contents = soup.text.strip().replace("\n", " ")
		return str(contents)


def crawl_lang(idl: int) -> str:
	"""
	Getting language of the site
	:param idl: ID
	:return: Lang code or empty string
	"""
	to_crawl = crawler_pages.get(id=idl)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	try:
		lang = soup.find("html")["lang"]
		return lang
	except TypeError as te:
		logger.info("Crawler, tasks, crawl_lang, TypeError exception %s", te)
	except Exception as ex:
		logger.exception("Crawler, tasks, crawl_lang, exception %s", ex)
		lang = ""
		return lang


def crawl_title(idt: int) -> str:
	"""
	Title
	:param idt: ID
	:return: Title or empty string
	"""
	to_crawl = crawler_pages.get(id=idt)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	try:
		title = str(soup.find('title').string)
		return title
	except TypeError as te:
		logger.info("Crawler, tasks, crawl_title, TypeError exception %s", te)
	except Exception as ex:
		logger.exception("Crawler, tasks, crawl_title, exception %s", ex)
		title = ''
		return title


def crawl_keyword(idl: int) -> str:
	"""
	Keywords
	:param idl: ID
	:return: Keywords or empty string
	"""
	key_words = ''
	to_crawl = crawler_pages.get(id=idl)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	try:
		key_words = soup.find("meta", {"name": "keywords"})['content']
		return key_words
	except TypeError as te:
		logger.info("Crawler, tasks, crawl_keyword, TypeError exception %s", te)
	except Exception as ex:
		logger.exception("Crawler, tasks, crawl_keyword, exception %s", ex)
		return key_words


def _get_description_og(id_desc_og: int) -> str:
	"""
	Description in the og property
	:param id_desc_og:
	:return: description or empty string
	"""
	to_crawl = crawler_pages.get(id=id_desc_og)
	soup = BeautifulSoup(to_crawl.cr_content, "lxml")
	try:
		description = soup.find("meta", {"property": "og:description"})['content']
		return description
	except TypeError as te:
		logger.info("Crawler, tasks, _get_description_og, TypeError exception %s", te)
	except Exception as ex:
		logger.exception("Crawler, tasks, _get_description_og, exception %s", ex)
		description = ''
		return description
