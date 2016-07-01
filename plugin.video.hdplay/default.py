import CommonFunctions as common
import urllib
import urllib2
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import urlfetch
import re
import json
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.hdplay')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
thumbnails = xbmc.translatePath( os.path.join( home, 'thumbnails\\' ) )

def _makeCookieHeader(cookie):
	cookieHeader = ""
	for value in cookie.values():
			cookieHeader += "%s=%s; " % (value.key, value.value)
	return cookieHeader

def make_request(url, headers=None):
	if headers is None:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
								 'Referer' : 'http://www.google.com'}
	try:
			req = urllib2.Request(url,headers=headers)
			f = urllib2.urlopen(req)
			body=f.read()
			return body
	except urllib2.URLError, e:
			print 'We failed to open "%s".' % url
			if hasattr(e, 'reason'):
					print 'We failed to reach a server.'
					print 'Reason: ', e.reason
			if hasattr(e, 'code'):
					print 'We failed with error code - %s.' % e.code
#def get_fpt():
	add_link('', 'Fashion TV', 0, 'http://hlscache.fptplay.net.vn/sopchannel/fashiontv.stream/playlist.m3u8', '', '')
	add_link('', 'MTV', 0, 'http://hlscache.fptplay.net.vn/sopchannel/mtvviet.stream/playlist.m3u8', '', '')
	add_link('', 'Star World', 0, 'http://hlscache.fptplay.net.vn/sopchannel/starworld.stream/playlist.m3u8', '', '')
	add_link('', 'Cinemax', 0, 'http://hlscache.fptplay.net.vn/sopchannel/cinemax.stream/playlist.m3u8', '', '')
	add_link('', 'Discovery Channel', 0, 'http://hlscache.fptplay.net.vn/sopchannel/discoverychannel.stream/playlist.m3u8', '', '')
	add_link('', 'Channel V', 0, 'http://hlscache.fptplay.net.vn/sopchannel/channelv.stream/playlist.m3u8', '', '')
	add_link('', 'Cartoon Network', 0, 'http://hlscache.fptplay.net.vn/sopchannel/cartoonnetwork.stream/playlist.m3u8', '', '')
	add_link('', 'Animal Planet', 0, 'http://hlscache.fptplay.net.vn/sopchannel/animalplanet.stream/playlist.m3u8', '', '')
	add_link('', 'National Geographic', 0, 'http://hlscache.fptplay.net.vn/sopchannel/nationalgeographic.stream/playlist.m3u8', '', '')
	add_link('', 'National Geographic Adventure', 0, 'http://hlscache.fptplay.net.vn/sopchannel/nationalgeographicadventure.stream/playlist.m3u8', '', '')
	add_link('', 'Nation Geographic Wild', 0, 'http://hlscache.fptplay.net.vn/sopchannel/nationalgeographicwild.stream/playlist.m3u8', '', '')
	add_link('', 'True Visions', 0, 'http://hlscache.fptplay.net.vn/sopchannel/truevisions.stream/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 1', 0, 'http://hlscache.fptplay.net.vn/event/sport1/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 2', 0, 'http://hlscache.fptplay.net.vn/event/sport2/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 3', 0, 'http://hlscache.fptplay.net.vn/event/sport3/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 4', 0, 'http://hlscache.fptplay.net.vn/event/sport4/playlist.m3u8', '', '')
	add_link('', 'Star Sport', 0, 'http://hlscache.fptplay.net.vn/sopchannel/starsports.stream/playlist.m3u8', '', '')
	add_link('', 'FOX Sport', 0, 'http://hlscache.fptplay.net.vn/sopchannel/foxsports.stream/playlist.m3u8', '', '')

	content = make_request('http://play.fpt.vn/livetv/')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', {'class' : 'channel_link'})
	for item in items:
		img = item.find('img')
		if img is not None:
			try:
				add_link('', item['channel'], 0, 'http://play.fpt.vn' + item['href'], img['src'], '')
			except:
				pass
#add_dir(name,url,mode,iconimage,query='',type='f',page=0):
def get_vtc_movies(url, query='25', type='', page=0):
	if url == '':
		content = make_request('http://117.103.206.21:88/Movie/GetMovieGenres?device=4')
		result = json.loads(content)
		for item in result:
			add_dir(item["Name"], 'http://117.103.206.21:88/Movie/GetMoviesByGenre?device=4&genreid=' + str(item["ID"]) + '&start=0&length=25', 11, '', '25', str(item["ID"]), 0)
	if 'GetMoviesByGenre' in url:
		content = make_request(url)
		result = json.loads(content)
		for item in result:
			add_link('', item["Title"], 0, 'http://117.103.206.21:88/Movie/GetMovieStream?device=4&path=' + item["MovieUrls"][0]["Path"].replace('SD', 'HD'), item["Thumbnail3"], item["SummaryShort"])
		add_dir('Next', 'http://117.103.206.21:88/Movie/GetMoviesByGenre?device=4&genreid=' + type + '&start=' + str(int(query)+page) + '&length=' + str(query), 11, '', str(int(query)+page), type, page)
	
def get_vtc(url = None):
	content = make_request(url)
	
	result = json.loads(content)
	for item in result:
		path = item["ChannelUrls"][0]["Path"]
		if 'http' in path:
			add_link('', item["Name"], 0, item["ChannelUrls"][0]["Path"], item["Thumbnail2"], '')
		else:
			add_link('', item["Name"], 0, "http://117.103.206.21:88/channel/GetChannelStream?device=4&path=" + item["ChannelUrls"][0]["Path"], item["Thumbnail2"], '')

def get_hdonline(url = None):
	if url == '':
		content = make_request('http://hdonline.vn/')
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.find('div',{'id' : 'full-mn-phim-le'}).findAll('a')
		for item in items:
			href = item.get('href')
			if href is not None:
				try:
					add_dir(item.text, href, 13, thumbnails + 'HDOnline.png', query, type, 0)
				except:
					pass
		return
	if 'xem-phim' in url:	
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.findAll('ul', {'class' : 'clearfix listmovie'})[1].findAll('li')
		for item in items:
			a = item.find('a')
			img = item.find('img')
			span = item.find('span',{'class' : 'type'})
			href = a.get('href')
			if href is not None:
				try:
					if span is not None:
						add_dir(a.get('title') + ' (' + span.text + ')', href, 9, a.img['src'], '', '', 0)
					else:	
						add_link('', a.get('title'), 0, href, img['src'], '')
				except:
					pass
		items = soup.find('div',{'class' : 'pagination pagination-right'})
		if items is not None:
			for item in items.findAll('a'):
				a = item
				href = a.get('href')
				if href is not None:
					try:
						add_dir(a.get('title'), href, 9, thumbnails + 'zui.png', '', '', 0)
					except:
						pass
		
def get_zui(url = None):
	if url == '':
		content = make_request('http://zui.vn')
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.find('div',{'class' : 'span8 visible-desktop visible-tablet'}).findAll('a')
		for item in items:
			href = item.get('href')
			if href is not None:
				try:
					add_dir(item.text, href, 9, thumbnails + 'zui.png', query, type, 0)
				except:
					pass
		return
	if 'the-loai' in url or 'phim-' in url:	
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		groups = soup.find('ul', {'class' : 'group'})
		if groups is not None:
			for item in groups.findAll('a'):
				matchObj = re.match( r'change_group_chapter\((\d+),(\d+),(\d+)\)', item['onclick'], re.M|re.I)
				response = urlfetch.fetch(
			url = 'http://zui.vn/?site=movie&view=show_group_chapter',
			method ='POST',
			data = {
				"pos": matchObj.group(1),
				"movie_id": matchObj.group(2),
				"type": matchObj.group(3)
			}
		)
				soup = BeautifulSoup(str(response.content), convertEntities=BeautifulSoup.HTML_ENTITIES)
				for item in soup.findAll('a'):
					add_link('', u'Tập ' + item.text, 0, 'http://zui.vn/' + item['href'], thumbnails + 'zui.png', '')
		else:
			items = soup.find('ul',{'class' : 'movie_chapter'})
			if items is not None:
				for item in items.findAll('a'):
					a = item
					href = a.get('href')
					if href is not None:
						try:
							add_link('', u'Tập ' + a.text, 0, 'http://zui.vn/' + href, thumbnails + 'zui.png', '')
							#add_dir(u'Tập ' + a.text, 'http://zui.vn/' + href, 9, thumbnails + 'zui.png', '', '', 0)
						except:
							pass
			else:
				items = soup.findAll('div',{'class' : 'poster'})
				for item in items:
					a = item.find('a')
					span = item.find('span',{'class' : 'type'})
					href = a.get('href')
					if href is not None:
						try:
							if span is not None:
								add_dir(a.get('title') + ' (' + span.text + ')', href, 9, a.img['src'], '', '', 0)
							else:	
								add_link('', a.get('title'), 0, href, a.img['src'], '')
						except:
							pass
				items = soup.find('div',{'class' : 'pagination pagination-right'})
				if items is not None:
					for item in items.findAll('a'):
						a = item
						href = a.get('href')
						if href is not None:
							try:
								add_dir(a.get('title'), href, 9, thumbnails + 'zui.png', '', '', 0)
							except:
								pass
	else:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		groups = soup.find('ul', {'class' : 'group'})
		if groups is not None:
			for item in groups.findAll('a'):
				matchObj = re.match( r'change_group_chapter\((\d+),(\d+),(\d+)\)', item['onclick'], re.M|re.I)
				response = urlfetch.fetch(
			url = 'http://zui.vn/?site=movie&view=show_group_chapter',
			method ='POST',
			data = {
				"pos": matchObj.group(1),
				"movie_id": matchObj.group(2),
				"type": matchObj.group(3)
			}
		)
				soup = BeautifulSoup(str(response.content), convertEntities=BeautifulSoup.HTML_ENTITIES)
				for item in soup.findAll('a'):
					add_link('', u'Tập ' + item.text, 0, 'http://zui.vn/' + item['href'], thumbnails + 'zui.png', '')
			return
	
		items = soup.find('ul',{'class' : 'movie_chapter'})
		if items is not None:
			for item in items.findAll('a'):
				a = item
				href = a.get('href')
				if href is not None:
					try:
						add_link('', u'Tập ' + a.text, 0, 'http://zui.vn/' + href, thumbnails + 'zui.png', '')
						#add_dir(u'Tập ' + a.text, 'http://zui.vn/' + href, 9, thumbnails + 'zui.png', '', '', 0)
					except:
						pass
	
def get_fpt_other(url):
	content = make_request(url)
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a')
	for item in items:
		href = item.get('href')
		if href is not None and 'the-loai-more' in href and 'Xem' not in item.text:
			try:
				add_dir(item.text, 'http://play.fpt.vn' + href, 8, thumbnails + 'fptplay.jpg', query, type, 0)
			except:
				pass

def get_fpt_tvshow_cat(url):
	content = make_request(url)
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	if url is not None and '/Video/' not in url:
		items = soup.findAll('div', {'class' : 'col'})
		for item in items:
			img = item.a.img['src']
			href = item.a['href']
			text = item.a.img['alt']	
			try:
				add_dir(text, 'http://play.fpt.vn' + href, 8, img, '', '', 0)
			except:
				pass

	items = soup.find('ul', {'class' : 'pagination pagination-sm'}).findAll('a')
	for item in items:
		href = ''
		href = item.get('href')
		if href is not None and 'the-loai-more' in href and 'Xem' not in item.text:
			try:
				add_dir('Trang ' + item.text, 'http://play.fpt.vn' + href, 8, thumbnails + 'fptplay.jpg', query, type, 0)
			except:
				pass
		if href is not None and '/Video/' in href:
			try:
				add_link('', u'Tập ' + item.text, 0, 'http://play.fpt.vn' + href, thumbnails + 'fptplay.jpg', '')
			except:
				pass
		
def get_htv():
	content = make_request('http://www.htvonline.com.vn/livetv')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', {'class' : 'mh-grids5-img'})
	for item in items:
		img = item.find('img')
		if img is not None:
			try:
				add_link('', item['title'], 0, item['href'], img['src'], '')
			except:
				pass

#def get_sctv(url):
	content = make_request('http://tv24.vn/LiveTV/Tivi_Truc_Tuyen_SCTV_VTV_HTV_THVL_HBO_STARMOVIES_VTC_VOV_BongDa_Thethao_Hai_ThoiTrang_Phim_PhimHongKong.html')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a')
	for item in items:
		img = item.find('img')
		if img is not None and 'LiveTV' in item['href']:
			try:
				add_link('', item['href'], 0, 'http://tv24.vn' + item['href'], img['src'], '')
			except:
				pass
		
def get_categories():
		
	add_link('', '[COLOR lime]************************* TH VP9 *****************************[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VTV1', 0, 'http://11e6.vp9.tv/chn/vtv1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV2', 0, 'http://11e6.vp9.tv/chn/vtv2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV3 HD', 0, 'http://11e6.vp9.tv/chn/vtv3/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV4', 0, 'http://11e6.vp9.tv/chn/vtv4/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV6 HD', 0, 'http://11e6.vp9.tv/chn/vtv6/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV8', 0, 'http://11e6.vp9.tv/chn/vtv8/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV9', 0, 'http://11e6.vp9.tv/chn/vtv9/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'ANTV', 0, 'http://11e6.vp9.tv/chn/antv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VOVTV', 0, 'http://11e6.vp9.tv/chn/vovtv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB2', 0, 'http://11e6.vp9.tv/chn/phimv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'THETHAOTV HD', 0, 'http://11e6.vp9.tv/chn/tttv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'BONGDATV HD', 0, 'http://11e6.vp9.tv/chn/bdtv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HN1', 0, 'http://11e6.vp9.tv/chn/hn1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HN2', 0, 'http://11e6.vp9.tv/chn/hn2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HTV7', 0, 'http://11e6.vp9.tv/chn/htv7/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HTV9', 0, 'http://11e6.vp9.tv/chn/htv9/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC1', 0, 'http://11e6.vp9.tv/chn/vtc1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC2', 0, 'http://11e6.vp9.tv/chn/vtc2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC6', 0, 'http://11e6.vp9.tv/chn/sgc6/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC7', 0, 'http://11e6.vp9.tv/chn/tdayt/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC9', 0, 'http://11e6.vp9.tv/chn/letsv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC11', 0, 'http://11e6.vp9.tv/chn/kids/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'DRT1', 0, 'http://11e6.vp9.tv/chn/drt1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'BTV1', 0, 'http://11e6.vp9.tv/chn/btv1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'THVL1', 0, 'http://11e6.vp9.tv/chn/vl1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'THVL2', 0, 'http://11e6.vp9.tv/chn/vl2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	
	add_link('', '[COLOR lime][B]********CHANNELS SPORTS *******[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'MS', 0, 'http://203.162.235.30/hls/MS/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Sport 24', 0, 'http://203.162.235.30/hls/SP24/playlist.m3u8', thumbnails + '', '')
	add_link('', 'ESPN', 0, 'http://203.162.235.30/hls/SN_ESPN/playlist.m3u8', thumbnails + '', '')
	add_link('', 'EDGE', 0, 'http://203.162.235.30/hls/EDGE/playlist.m3u8', thumbnails + '', '')
	add_link('', 'SKY SPORT', 0, 'http://203.162.235.30/hls/SKY_SPORT_N/playlist.m3u8', thumbnails + '', '')
	add_link('', 'BEIN1 PORT', 0, 'http://203.162.235.30/hls/BEIN1PORT/playlist.m3u8', thumbnails + '', '')
	add_link('', 'TRUE4U', 0, 'http://203.162.235.30/hls/TRUE4U/playlist.m3u8', thumbnails + '', '')
	add_link('', 'J SPORT 1', 0, 'http://203.162.235.45:17930', thumbnails + '', '')
	add_link('', 'J SPORT 2', 0, 'http://203.162.235.45:17931', thumbnails + '', '')
	add_link('', 'J SPORT 3', 0, 'http://203.162.235.45:17932', thumbnails + '', '')
	add_link('', 'J SPORT 4', 0, 'http://203.162.235.45:17933', thumbnails + '', '')
	add_link('', 'SUPER SPORT', 0, 'http://92.222.205.40:8085/lighd', thumbnails + '', '')
	add_link('', 'Thai:TRUE SPORT HD2', 0, 'rtmp://216.185.103.158/live2/chthaipremier11', thumbnails + '', '')
	add_link('', 'Thai:TRUE SPORT 2', 0, 'rtmp://216.185.103.158/live2/chthaipremier31', thumbnails + '', '')

	add_link('', '[COLOR lime][B]********TH QUỐC TẾ *******[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'WOWOW', 0, 'http://203.162.235.45:17934', thumbnails + '', '')
	add_link('', 'TRT BELGESEL HD', 0, 'http://trtcanlitv-lh.akamaihd.net/i/TRTBELGESEL_1@182145/index_1500_av-b.m3u8?sd=10&rebase=on&hdntl=', thumbnails + '', '')
	add_link('', 'AlJazeera Doc', 0, 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live//aljazeera_doc_high', thumbnails + '', '')
	add_link('', 'Arte', 0, 'http://frlive.artestras.cshls.lldns.net/artestras/contrib/frlive/frlive_925.m3u8', thumbnails + '', '')
	add_link('', 'Tom & Jerry', 0, 'rtmp://208.53.180.242/ctv playpath=tom swfUrl=http://www.canaistv.net/player.swf pageUrl=http://www.canaistv.net/tvamigos/two.html live=1', thumbnails + '', '')
	add_link('', 'CN:Lotus TV', 0, 'http://ktv039.cdnak.ds.kylintv.net/nlds/kylin/lotustv/as/live/lotustv_4.m3u8', thumbnails + '', '')
	add_link('', 'CN:Phoenix Chinese', 0, 'http://ktv028.cdnak.ds.kylintv.net/nlds/kylin/pxasia/as/live/pxasia_4.m3u8', thumbnails + '', '')
	add_link('', 'Thai: CH2', 0, 'http://iliketot.dyndns.tv/tot/web/4e38ed2fa4dd43999828eab81196deff.m3u8', thumbnails + '', '')
	add_link('', 'Thai: CH5', 0, 'http://iliketot.dyndns.tv/tot/web/1d92193b11fe490b8c67d0a88bee3fd6.m3u8', thumbnails + '', '')
	add_link('', 'Thai: CHANNEL7 HD', 0, 'http://edge5.psitv.tv:1935/liveedge/308091128717_600/chunklist_w.m3u8', thumbnails + '', '')
	add_link('', 'Thai: CH7', 0, 'http://iliketot.dyndns.tv/tot/web/ddfa47e726444446864b14e0e819fdde.m3u8', thumbnails + '', '')
	add_link('', 'Thai: CH8', 0, 'http://iliketot.dyndns.tv/tot/web/15c52eeb21b748319771eb794a6cf242.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Modern 9', 0, 'http://iliketot.dyndns.tv/tot/web/3ae2fd6ccaf6499e898de377ed74ea12.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Thaichaiyo', 0, 'http://iliketot.dyndns.tv/tot/web/a2ca06da9478412e9501d968e31bbf75.m3u8', thumbnails + '', '')
	add_link('', 'Thai: NEW TV18', 0, 'http://iliketot.dyndns.tv/tot/web/0d01fdc1362f427ca5527c645f5f908f.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Sky News HD', 0, 'http://iliketot.dyndns.tv/tot/web/31b003ab7e7749a798fe00424e3dd9ff.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Al Yazeera News', 0, 'http://iliketot.dyndns.tv/tot/web/ea4c9d2666bc411d8e6777e8a1d2b747.m3u8', thumbnails + '', '')
	add_link('', 'Thai:France 24 News', 0, 'http://iliketot.dyndns.tv/tot/web/82c764aa2d7f42579348b8717cb5b9a4.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Fox News', 0, 'http://iliketot.dyndns.tv/tot/web/1e2041858ca543fa90ec95d28197e907.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Nat Geo People', 0, 'http://iliketot.dyndns.tv/tot/web/7ad09373f65c48d5bb6aa6c3b2ca519a.m3u8', thumbnails + '', '')
	add_link('', 'Thai: Nat Geo Wild', 0, 'http://iliketot.dyndns.tv/tot/web/607fa33938bc4a3ea6c43ce47ddb8ed8.m3u8', thumbnails + '', '')
	add_link('', 'Thai: FyiAsia', 0, 'http://iliketot.dyndns.tv/tot/web/169a149fd1ef40edba0bbfc8e0f1bdd1.m3u8', thumbnails + '', '')
	add_link('', 'Thai: CI', 0, 'http://iliketot.dyndns.tv/tot/web/9961a963920f45f4bc0d81c3e478b334.m3u8', thumbnails + '', '')
	
	#add_link('', 'HBO HD', 0, '', '', '')
	#http://scache.fptplay.net.vn/live/htvcplusHD_1000.stream/manifest.f4m
	#add_dir('HTVOnline', url, 5, thumbnails + 'htv.jpg', query, type, 0)
	#add_dir('SCTV', url, 12, thumbnails + 'SCTV.png', query, type, 0)
	#add_dir('VTCPlay - TV', 'http://117.103.206.21:88/Channel/GetChannels?device=4', 10, thumbnails + 'vtcplay.jpg', query, type, 0)
	#add_dir('VTCPlay - Movies', '', 11, thumbnails + 'vtcplay.jpg', query, type, 0)
	#add_dir('FPTPlay - TV', url, 6, thumbnails + 'fptplay_logo.jpg', query, type, 0)
	#add_dir('FPTPlay - TVShow', url, 7, thumbnails + 'fptplay_logo.jpg', query, type, 0)
	#add_dir('ZUI.VN', url, 9, thumbnails + 'zui.png', query, type, 0)
	#add_dir('HDOnline.vn', url, 13, thumbnails + 'HDOnline.png', query, type, 0)

def searchMenu(url, query = '', type='f', page=0):
	add_dir('New Search', url, 2, icon, query, type, 0)
	add_dir('Clear Search', url, 3, icon, query, type, 0)

	searchList=cache.get('searchList').split("\n")
	for item in searchList:
		add_dir(item, url, 2, icon, item, type, 0)

def resolve_url(url):
	if 'zui.vn' in url:
		headers2 = {'User-agent' : 'iOS / Chrome 32: Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/32.0.1700.20 Mobile/11B554a Safari/9537.53',
											 'Referer' : 'http://www.google.com'}
		content = make_request(url, headers2)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('movie_play_chapter'):
				#movie_play_chapter('mediaplayer', '1', 'rtmp://103.28.37.89:1935/vod3/mp4:/phimle/Vikingdom.2013.720p.WEB-DL.H264-PHD.mp4', '/uploads/movie_view/5c65563b1ce8d106c013.jpg', 'http://zui.vn/subtitle/Vikingdom.2013.720p.WEB-DL.H264-PHD.srt');
				matchObj = re.match( r'[^\']*\'([^\']*)\', \'([^\']*)\', \'([^\']*)\', \'([^\']*)\', \'([^\']*)\'', s, re.M|re.I)
				url = matchObj.group(3)
				url = url.replace(' ','%20')
				xbmc.Player().play(url)
				xbmc.Player().setSubtitles(matchObj.group(5))
				return
				break

	if 'play.fpt.vn/Video' in url:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('"<source src='):
				start = s.index('\'')+1
				end = s.index('\'', start+1)
				url = s[start:end]
				break

	if 'play.fpt.vn' in url:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		item = soup.find('div', {'id' : 'bitrate-tag'})
		url = item['highbitrate-link']
		content = make_request(url)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('<id>'):
				start = s.index('<id>')+4
				end = s.index('<', start+1)
				url = url.replace('manifest.f4m',s[start:end])
				url = 'http://scache.fptplay.net.vn/live/' + s[start:end] + '/playlist.m3u8'
				break

	if 'htvonline' in url:
		content = make_request(url)
		for line in content.splitlines():
			if line.strip().startswith('file: '):
				url = line.strip().replace('file: ', '').replace('"', '').replace(',', '')
				break

	#if 'tv24' in url:
		content = make_request(url)
		for line in content.splitlines():
			if line.strip().startswith('\'file\': \'http'):
				url = line.strip().replace('\'file\': ', '').replace('\'', '').replace(',', '')
				break
		
	if 'GetChannelStream' in url or 'GetMovieStream' in url or 'vtvplay' in url:
		content = make_request(url)
		url = content.replace("\"", "")
		url = url[:-5]
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def add_link(date, name, duration, href, thumb, desc):
	description = date+'\n\n'+desc
	u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&mode=4"
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration})
	if 'zui' in href:
		liz.setProperty('IsPlayable', 'false')
	else:
		liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)



def add_dir(name,url,mode,iconimage,query='',type='f',page=0):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)#+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]

	return param

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=''
name=None
mode=None
query=None
type='f'
page=0

try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
try:
	page=int(urllib.unquote_plus(params["page"]))
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "type: "+str(type)
print "page: "+str(page)
print "query: "+str(query)

if mode==None:
	get_categories()
#		fslink_get_video_categories(FSLINK+'/phim-anh.html')

elif mode==1:
	searchMenu(url, '', type, page)

elif mode==2:
	search(url, query, type, page)

elif mode==3:
	clearSearch()

elif mode==4:
	resolve_url(url)
elif mode==5:
	get_htv()
elif mode==6:
	get_fpt()
elif mode==7:
	get_fpt_other('http://play.fpt.vn/the-loai/tvshow')
	#get_fpt_other('http://play.fpt.vn/the-loai/sport')
	#get_fpt_other('http://play.fpt.vn/the-loai/music')
	#get_fpt_other('http://play.fpt.vn/the-loai/general')
elif mode==8:
	get_fpt_tvshow_cat(url)
elif mode==9:
	get_zui(url)
elif mode==10:
	get_vtc(url)
elif mode==11:
	get_vtc_movies(url, query, type, page)
#elif mode==12:
	get_sctv(url)
elif mode==13:
	get_hdonline(url)
	 
xbmcplugin.endOfDirectory(int(sys.argv[1]))
