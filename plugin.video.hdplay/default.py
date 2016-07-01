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
		
	add_link('', '[COLOR lime][B]********TH ONETV *******[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'THETHAO TV HD S1', 0, 'udp://@225.1.2.241:30120', thumbnails + '', '')
	add_link('', 'THETHAOTV HD S2', 0, 'http://118.69.252.4/tv1/thethaoTVHD/index.m3u8', thumbnails + '', '')
	add_link('', 'BONGDATV HD S1', 0, 'udp://@225.1.2.243:30120', thumbnails + '', '')
	add_link('', 'BONGDATV HD S2', 0, 'http://118.69.252.4/tv1/bongdaTVHD/index.m3u8', thumbnails + '', '')
	add_link('', 'MUSIC 1 HD', 0, 'udp://@225.1.1.7:30120', thumbnails + '', '')
	add_link('', 'MUSIC 2 HD', 0, 'udp://@225.1.1.8:30120', thumbnails + '', '')
	add_link('', 'VTV1 HD S1', 0, 'udp://@225.1.2.249:30120', thumbnails + '', '')
	add_link('', 'VTV1 HD S2', 0, 'http://118.69.252.4/tv/vtv1HD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV3 HD S1', 0, 'udp://@225.1.2.247:30120', thumbnails + '', '')
	add_link('', 'VTV3 HD S2', 0, 'http://118.69.252.4/tv/vtv3HD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV3 HD S1', 0, 'udp://@225.1.2.247:30120', thumbnails + '', '')
	add_link('', 'VTV3 HD S2', 0, 'http://118.69.252.4/tv/vtv3HD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV6 HD S1', 0, 'udp://@225.1.2.244:30120', thumbnails + '', '')
	add_link('', 'VTV6 HD S2', 0, 'http://118.69.252.4/tv/vtv6HD/index.m3u8', thumbnails + '', '')
	add_link('', 'NHAN DAN HD', 0, 'udp://@225.1.1.91:30120', thumbnails + '', '')
	add_link('', 'QUOC HOI HD S1', 0, 'udp://@225.1.2.148:30120', thumbnails + '', '')
	add_link('', 'QUOC HOI HD S2', 0, 'http://118.69.184.194/tv1/quochoi/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV1', 0, 'udp://@225.1.1.250:30120', thumbnails + '', '')
	add_link('', 'VTV2 S1', 0, 'udp://@225.1.1.249:30120', thumbnails + '', '')
	add_link('', 'VTV2 S2', 0, 'http://118.69.252.4/tv/vtv2/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV4 S1', 0, 'udp://@225.1.1.248:30120', thumbnails + '', '')
	add_link('', 'VTV4 S2', 0, 'http://118.69.184.194/tv/vtv4/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV5', 0, 'udp://@225.1.1.247:30120', thumbnails + '', '')
	add_link('', 'VTV6', 0, 'udp://@225.1.1.246:30120', thumbnails + '', '')
	add_link('', 'VTV9 S1', 0, 'udp://@225.1.1.153:30120', thumbnails + '', '')
	add_link('', 'VTV9 S2', 0, 'http://118.69.252.4/tv/vtv9/index.m3u8', thumbnails + '', '')
	add_link('', 'VOV', 0, 'udp://@225.1.2.171:30120', thumbnails + '', '')
	add_link('', 'VIETNAMNET', 0, 'udp://@225.1.1.194:30120', thumbnails + '', '')
	add_link('', 'TTXVN S1', 0, 'udp://@225.1.1.167:30120', thumbnails + '', '')
	add_link('', 'TTXVN S2', 0, 'http://118.69.252.4/tv1/vnews/index.m3u8', thumbnails + '', '')
	add_link('', 'QPVN', 0, 'udp://@225.1.1.226:30120', thumbnails + '', '')
	add_link('', 'ANTV S1', 0, 'udp://@225.1.2.169:30120', thumbnails + '', '')
	add_link('', 'ANTV S2', 0, 'http://118.69.252.4/tv/anninhtv/index.m3u8', thumbnails + '', '')
	add_link('', 'GIAI TRI TV', 0, 'udp://@225.1.2.150:30120', thumbnails + '', '')
	add_link('', 'PHIM VIET', 0, 'udp://@225.1.2.159:30120', thumbnails + '', '')
	add_link('', 'THETHAO TV', 0, 'udp://@225.1.2.158:30120', thumbnails + '', '')
	add_link('', 'VAN HOA', 0, 'udp://@225.1.2.153:30120', thumbnails + '', '')
	add_link('', 'E CHANNEL', 0, 'udp://@225.1.2.156:30120', thumbnails + '', '')
	add_link('', 'HAY TV', 0, 'udp://@225.1.1.254:30120', thumbnails + '', '')
	add_link('', 'D DRAMAS', 0, 'udp://@225.1.2.157:30120', thumbnails + '', '')
	add_link('', 'BIBI', 0, 'udp://@225.1.2.161:30120', thumbnails + '', '')
	add_link('', 'INFO TV', 0, 'udp://@225.1.2.154:30120', thumbnails + '', '')
	add_link('', 'O2 TV', 0, 'udp://@225.1.2.152:30120', thumbnails + '', '')
	add_link('', 'TV SHOPPING', 0, 'udp://@225.1.1.252:30120', thumbnails + '', '')
	add_link('', 'STYLE TV', 0, 'udp://@225.1.2.155:30120', thumbnails + '', '')
	add_link('', 'VTVCAB13', 0, 'udp://@225.1.1.122:30120', thumbnails + '', '')
	add_link('', 'VTVCAB14', 0, 'udp://@225.1.1.253:30120', thumbnails + '', '')
	add_link('', 'M CHANNEL', 0, 'udp://@225.1.1.251:30120', thumbnails + '', '')
	add_link('', 'BONGDA TV', 0, 'udp://@225.1.2.160:30120', thumbnails + '', '')
	add_link('', 'YEAH1 TV', 0, 'udp://@225.1.2.151:30120', thumbnails + '', '')
	add_link('', 'VFAMILY', 0, 'udp://@225.1.1.15:30120', thumbnails + '', '')
	add_link('', 'HTV2 HD S1', 0, 'udp://@225.1.1.193:30120', thumbnails + '', '')
	add_link('', 'HTV2 HD S2', 0, 'http://118.69.252.4/tv/htv2HD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV7 HD S1', 0, 'udp://@225.1.1.192:30120', thumbnails + '', '')
	add_link('', 'HTV7 S2', 0, 'http://118.69.252.4/tv/htv7HD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV9 HD S1', 0, 'udp://@225.1.1.189:30120', thumbnails + '', '')
	add_link('', 'HTV9 HD S2', 0, 'http://118.69.252.4/tv/htv9HD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC MOVIE HD S1', 0, 'udp://@225.1.1.184:30120', thumbnails + '', '')
	add_link('', 'HTVC MOVIE HD S2', 0, 'http://118.69.252.4/tv1/htvcmovieHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC THUAN VIET HD S1', 0, 'udp://@225.1.1.186:30120', thumbnails + '', '')
	add_link('', 'HTVC THUAN VIET HD S2', 0, 'http://118.69.252.4/tv1/htvcthuanvietHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC FBNC HD', 0, 'udp://@225.1.1.182:30120', thumbnails + '', '')
	add_link('', 'VTC1 HD', 0, 'udp://@225.1.2.254:30120', thumbnails + '', '')
	add_link('', 'VTC3 HD S1', 0, 'udp://@225.1.2.251:30120', thumbnails + '', '')
	add_link('', 'VTC3 HD S2', 0, 'http://118.69.252.4/tv1/vtc3HD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC4 HD', 0, 'udp://@225.1.2.200:30120', thumbnails + '', '')
	add_link('', 'ITV HD S1', 0, 'udp://@225.1.2.250:30120', thumbnails + '', '')
	add_link('', 'ITV HD S2', 0, 'http://118.69.184.194/tv1/itvHD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC14 HD', 0, 'udp://@225.1.2.88:30120', thumbnails + '', '')
	add_link('', 'HTV1', 0, 'udp://@225.1.1.180:30120', thumbnails + '', '')
	add_link('', 'HTV2', 0, 'udp://@225.1.1.179:30120', thumbnails + '', '')
	add_link('', 'HTV3 S1', 0, 'udp://@225.1.1.178:30120', thumbnails + '', '')
	add_link('', 'HTV3 S2', 0, 'http://118.69.252.4/tv/htv3/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV4 S1', 0, 'udp://@225.1.1.177:30120', thumbnails + '', '')
	add_link('', 'HTV4 S2', 0, 'http://118.69.252.4/tv1/htv4/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV7', 0, 'udp://@225.1.1.176:30120', thumbnails + '', '')
	add_link('', 'HTV9', 0, 'udp://@225.1.1.175:30120', thumbnails + '', '')
	add_link('', 'HTVC THETHAO S1', 0, 'udp://@225.1.1.165:30120', thumbnails + '', '')
	add_link('', 'HTVC THETHAO S2', 0, 'http://118.69.252.4/tv1/htvcthethao/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC PHU NU', 0, 'udp://@225.1.1.171:30120', thumbnails + '', '')
	add_link('', 'HTVC GIA DINH S1', 0, 'udp://@225.1.1.170:30120', thumbnails + '', '')
	add_link('', 'HTVC GIA DINH S2', 0, 'http://118.69.252.4/tv1/htvcgiadinh/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC THUAN VIET', 0, 'http://118.69.252.4/tv1/htvcthuanviet/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC MOVIE', 0, 'udp://@225.1.1.173:30120', thumbnails + '', '')
	add_link('', 'DU LICH CUOC SONG', 0, 'udp://@225.1.1.166:30120', thumbnails + '', '')
	add_link('', 'HTVC SHOPPING', 0, 'udp://@225.1.1.166:30120', thumbnails + '', '')
	add_link('', 'VTC1', 0, 'udp://@225.1.2.203:30120', thumbnails + '', '')
	add_link('', 'VTC2', 0, 'udp://@225.1.2.202:30120', thumbnails + '', '')
	add_link('', 'VTC3', 0, 'udp://@225.1.2.201:30120', thumbnails + '', '')
	add_link('', 'VTC4', 0, 'udp://@225.1.2.200:30120', thumbnails + '', '')
	add_link('', 'VTC5', 0, 'udp://@225.1.2.199:30120', thumbnails + '', '')
	add_link('', 'VTC6 S1', 0, 'udp://@225.1.2.198:30120', thumbnails + '', '')
	add_link('', 'VTC6 S2', 0, 'http://118.69.184.194/tv1/vtc6/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC7 S1', 0, 'udp://@225.1.2.197:30120', thumbnails + '', '')
	add_link('', 'VTC7 S2', 0, 'http://118.69.252.4/tv/vtc7/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC8', 0, 'udp://@225.1.2.196:30120', thumbnails + '', '')
	add_link('', 'VTC9 S1', 0, 'udp://@225.1.2.195:30120', thumbnails + '', '')
	add_link('', 'VTC9 S2', 0, 'http://118.69.184.194/tv1/vtc9/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC10', 0, 'udp://@225.1.2.194:30120', thumbnails + '', '')
	add_link('', 'VTC11', 0, 'udp://@225.1.2.193:30120', thumbnails + '', '')
	add_link('', 'VTC12', 0, 'udp://@225.1.2.192:30120', thumbnails + '', '')
	add_link('', 'ITV', 0, 'udp://@225.1.2.189:30120', thumbnails + '', '')
	add_link('', 'VTC14 S1', 0, 'udp://@225.1.2.191:30120', thumbnails + '', '')
	add_link('', 'VTC14 S2', 0, 'http://118.69.184.194/tv1/vtc14/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC16 S1', 0, 'udp://@225.1.2.190:30120', thumbnails + '', '')
	add_link('', 'VTC16 S2', 0, 'http://118.69.184.194/tv1/quocphongHD/index.m3u8', thumbnails + '', '')
	add_link('', 'ANTG', 0, 'udp://@225.1.1.208:30120', thumbnails + '', '')
	add_link('', 'PHIM HAY', 0, 'udp://@225.1.1.222:30120', thumbnails + '', '')
	add_link('', 'NCM', 0, 'udp://@225.1.1.225:30120', thumbnails + '', '')
	add_link('', 'MIEN TAY', 0, 'udp://@225.1.1.221:30120', thumbnails + '', '')
	add_link('', 'SAM', 0, 'udp://@225.1.1.224:30120', thumbnails + '', '')
	add_link('', 'VIETTEEN', 0, 'udp://@225.1.1.223:30120', thumbnails + '', '')
	add_link('', 'HA NOI 1', 0, 'udp://@225.1.2.186:30120', thumbnails + '', '')
	add_link('', 'HA NOI 2', 0, 'udp://@225.1.1.125:30120', thumbnails + '', '')
	add_link('', 'HITV', 0, 'udp://@225.1.1.209:30120', thumbnails + '', '')
	add_link('', 'YOUTV', 0, 'udp://@225.1.1.207:30120', thumbnails + '', '')
	add_link('', 'HCATV5', 0, 'udp://@225.1.1.210:30120', thumbnails + '', '')
	add_link('', 'MOV', 0, 'udp://@225.1.1.206:30120', thumbnails + '', '')
	add_link('', 'HAI DUONG', 0, 'udp://@225.1.1.158:30120', thumbnails + '', '')
	add_link('', 'HAI PHONG', 0, 'udp://@225.1.2.187:30120', thumbnails + '', '')
	add_link('', 'HA GIANG', 0, 'udp://@225.1.1.62:30120', thumbnails + '', '')
	add_link('', 'HA NAM', 0, 'udp://@225.1.1.63:30120', thumbnails + '', '')
	add_link('', 'THAI NGUYEN', 0, 'udp://@225.1.2.179:30120', thumbnails + '', '')
	add_link('', 'TUYEN QUANG', 0, 'udp://@225.1.2.188:30120', thumbnails + '', '')
	add_link('', 'QUANG NINH 1', 0, 'udp://@225.1.2.181:30120', thumbnails + '', '')
	add_link('', 'QUANG NINH 3', 0, 'udp://@225.1.2.180:30120', thumbnails + '', '')
	add_link('', 'THANH HOA', 0, 'udp://@225.1.2.184:30120', thumbnails + '', '')
	add_link('', 'NGHE AN', 0, 'udp://@225.1.2.183:30120', thumbnails + '', '')
	add_link('', 'NINH BINH', 0, 'udp://@225.1.2.185:30120', thumbnails + '', '')
	add_link('', 'HOA BINH', 0, 'udp://@225.1.2.168:30120', thumbnails + '', '')
	add_link('', 'BAC GIANG', 0, 'udp://@225.1.1.164:30120', thumbnails + '', '')
	add_link('', 'LANG SON', 0, 'udp://@225.1.1.160:30120', thumbnails + '', '')
	add_link('', 'NAM DINH', 0, 'udp://@225.1.1.120:30120', thumbnails + '', '')
	add_link('', 'LAO CAI', 0, 'udp://@225.1.1.118:30120', thumbnails + '', '')
	add_link('', 'THAI BINH', 0, 'udp://@225.1.1.99:30120', thumbnails + '', '')
	add_link('', 'SON LA', 0, 'udp://@225.1.1.98:30120', thumbnails + '', '')
	add_link('', 'HA TINH', 0, 'udp://@225.1.1.75:30120', thumbnails + '', '')
	add_link('', 'DIEN BIEN', 0, 'udp://@225.1.1.74:30120', thumbnails + '', '')
	add_link('', 'BAC NINH', 0, 'udp://@225.1.1.40:30120', thumbnails + '', '')
	add_link('', 'YEN BAI', 0, 'udp://@225.1.1.39:30120', thumbnails + '', '')
	add_link('', 'PHU THO', 0, 'udp://@225.1.2.165:30120', thumbnails + '', '')
	add_link('', 'VINH PHUC', 0, 'udp://@225.1.2.99:30120', thumbnails + '', '')
	add_link('', 'QUANG TRI', 0, 'udp://@225.1.1.117:30120', thumbnails + '', '')
	add_link('', 'HUE', 0, 'udp://@225.1.1.161:30120', thumbnails + '', '')
	add_link('', 'DA NANG 1', 0, 'udp://@225.1.1.147:30120', thumbnails + '', '')
	add_link('', 'DA NANG 2', 0, 'udp://@225.1.1.146:30120', thumbnails + '', '')
	add_link('', 'QUANG NAM', 0, 'udp://@225.1.2.50:30120', thumbnails + '', '')
	add_link('', 'BTV (BINH DINH)', 0, 'udp://@225.1.2.173:30120', thumbnails + '', '')
	add_link('', 'KHANH HOA', 0, 'udp://@225.1.1.133:30120', thumbnails + '', '')
	add_link('', 'BINH THUAN', 0, 'udp://@225.1.1.124:30120', thumbnails + '', '')
	add_link('', 'NINH THUAN', 0, 'udp://@225.1.2.178:30120', thumbnails + '', '')
	add_link('', 'LAM DONG', 0, 'udp://@225.1.2.177:30120', thumbnails + '', '')
	add_link('', 'KON TUM', 0, 'udp://@225.1.1.36:30120', thumbnails + '', '')
	add_link('', 'GIA LAI', 0, 'udp://@225.1.2.176:30120', thumbnails + '', '')
	add_link('', 'DONG NAI 1', 0, 'udp://@225.1.1.152:30120', thumbnails + '', '')
	add_link('', 'DONG NAI 2', 0, 'udp://@225.1.1.151:30120', thumbnails + '', '')
	add_link('', 'BTV1', 0, 'udp://@225.1.1.150:30120', thumbnails + '', '')
	add_link('', 'BTV2', 0, 'udp://@225.1.1.149:30120', thumbnails + '', '')
	add_link('', 'BTV4 HD', 0, 'udp://@225.1.1.29:30120', thumbnails + '', '')
	add_link('', 'BINH PHUOC 1', 0, 'udp://@225.1.2.23:30120', thumbnails + '', '')
	add_link('', 'BINH PHUOC 2', 0, 'udp://@225.1.2.38:30120', thumbnails + '', '')
	add_link('', 'BA RIA VUNG TAU', 0, 'udp://@225.1.2.175:30120', thumbnails + '', '')
	add_link('', 'TAY NINH', 0, 'udp://@225.1.1.130:30120', thumbnails + '', '')
	add_link('', 'LONG AN', 0, 'udp://@225.1.1.162:30120', thumbnails + '', '')
	add_link('', 'VINH LONG 1 S1', 0, 'udp://@225.1.1.155:30120', thumbnails + '', '')
	add_link('', 'VINH LONG 1 S2', 0, 'http://118.69.252.4/tv/vinhlong1/index.m3u8', thumbnails + '', '')
	add_link('', 'VINH LONG 2 S1', 0, 'udp://@225.1.1.154:30120', thumbnails + '', '')
	add_link('', 'VINH LONG 2 S2', 0, 'http://118.69.252.4/tv/vinhlong2/index.m3u8', thumbnails + '', '')
	add_link('', 'TIEN GIANG', 0, 'udp://@225.1.2.170:30120', thumbnails + '', '')
	add_link('', 'CAN THO', 0, 'udp://@225.1.1.132:30120', thumbnails + '', '')
	add_link('', 'KIEN GIANG', 0, 'udp://@225.1.2.182:30120', thumbnails + '', '')
	add_link('', 'BAC LIEU', 0, 'udp://@225.1.1.61:30120', thumbnails + '', '')
	add_link('', 'DONG THAP', 0, 'udp://@225.1.1.163:30120', thumbnails + '', '')
	add_link('', 'SOC TRANG', 0, 'udp://@225.1.1.159:30120', thumbnails + '', '')
	add_link('', 'BEN TRE', 0, 'udp://@225.1.1.156:30120', thumbnails + '', '')
	add_link('', 'HAU GIANG', 0, 'udp://@225.1.1.157:30120', thumbnails + '', '')
	add_link('', 'TRA VINH', 0, 'udp://@225.1.2.172:30120', thumbnails + '', '')
	add_link('', 'CA MAU', 0, 'udp://@225.1.1.104:30120', thumbnails + '', '')
	add_link('', 'STAR MOVIES HD S1', 0, 'udp://@225.1.2.239:30120', thumbnails + '', '')
	add_link('', 'STARMOVIES HD S2', 0, 'http://118.69.252.4/tv3/StarMoviesHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HBO HD S1', 0, 'udp://@225.1.2.233:30120', thumbnails + '', '')
	add_link('', 'HBO HD S2', 0, 'http://118.69.252.4/tv3/HBOHD/index.m3u8', thumbnails + '', '')
	add_link('', 'RED by HBO HD', 0, 'udp://@225.1.1.89:30120', thumbnails + '', '')
	add_link('', 'AXN HD S1', 0, 'udp://@225.1.2.225:30120', thumbnails + '', '')
	add_link('', 'AXN HD S2', 0, 'http://118.69.252.4/tv3/AXNHD/index.m3u8', thumbnails + '', '')
	add_link('', 'DISCOVERY WORLD HD S1', 0, 'udp://@225.1.2.223:30120', thumbnails + '', '')
	add_link('', 'DISCOVERY WORLD HD S2', 0, 'http://118.69.252.4/tv3/DiscoveryWorldHD/index.m3u8', thumbnails + '', '')
	add_link('', 'NATGEO HD S1', 0, 'udp://@225.1.2.235:30120', thumbnails + '', '')
	add_link('', 'NATGEO HD S2', 0, 'http://118.69.252.4/tv3/NationalGeographicHD/index.m3u8', thumbnails + '', '')
	add_link('', 'DA VINCI HD', 0, 'udp://@225.1.1.197:30120', thumbnails + '', '')
	add_link('', 'OUTDOOR CHANNEL HD', 0, 'udp://@225.1.2.215:30120', thumbnails + '', '')
	add_link('', 'CN HD S1', 0, 'udp://@225.1.2.231:30120', thumbnails + '', '')
	add_link('', 'CN HD S2', 0, 'http://118.69.252.4/tv3/CartoonNetworkHD/index.m3u8', thumbnails + '', '')
	add_link('', 'TOONAMI HD', 0, 'udp://@225.1.1.60:30120', thumbnails + '', '')
	add_link('', 'S GEM HD', 0, 'udp://@225.1.2.220:30120', thumbnails + '', '')
	add_link('', 'FOX SPORTS HD S1', 0, 'udp://@225.1.2.229:30120', thumbnails + '', '')
	add_link('', 'FOX SPORTS HD S2', 0, 'http://118.69.252.4/tv3/FoxSportsHD/index.m3u8', thumbnails + '', '')
	add_link('', 'FOX SPORTS 2HD1', 0, 'udp://@225.1.1.141:30120', thumbnails + '', '')
	add_link('', 'STAR WORLD HD', 0, 'udp://@225.1.2.237:30120', thumbnails + '', '')
	add_link('', 'CHANNEL V HD', 0, 'udp://@225.1.1.188:30120', thumbnails + '', '')
	add_link('', 'ASIAN FOOD CHANNEL HD', 0, 'udp://@225.1.1.198:30120', thumbnails + '', '')
	add_link('', 'FASHIONTV HD S1', 0, 'udp://@225.1.2.227:30120', thumbnails + '', '')
	add_link('', 'FASHIONTV HD S2', 0, 'http://118.69.252.4/tv3/FashionTVHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HBO', 0, 'udp://@225.1.1.235:30120', thumbnails + '', '')
	add_link('', 'STAR MOVIES', 0, 'udp://@225.1.1.205:30120', thumbnails + '', '')
	add_link('', 'AXN', 0, 'udp://@225.1.1.237:30120', thumbnails + '', '')
	add_link('', 'CINEMAX S1', 0, 'udp://@225.1.1.230:30120', thumbnails + '', '')
	add_link('', 'CINEMAX S2', 0, 'http://118.69.252.4/tv3/Cinemax/index.m3u8', thumbnails + '', '')
	add_link('', 'NATGEO', 0, 'udp://@225.1.1.244:30120', thumbnails + '', '')
	add_link('', 'DISCOVERY S1', 0, 'udp://@225.1.1.238:30120', thumbnails + '', '')
	add_link('', 'DISCOVERY S2', 0, 'http://118.69.252.4/tv3/Discovery/index.m3u8', thumbnails + '', '')
	add_link('', 'TLC S1', 0, 'udp://@225.1.1.236:30120', thumbnails + '', '')
	add_link('', 'TLC S2', 0, 'http://118.69.252.4/tv3/TravelLiving/index.m3u8', thumbnails + '', '')
	add_link('', 'ANIMAL PLANET S1', 0, 'udp://@225.1.1.231:30120', thumbnails + '', '')
	add_link('', 'ANIMAL PLANET S2', 0, 'http://118.69.252.4/tv3/AnimalPlanet/index.m3u8', thumbnails + '', '')
	add_link('', 'CN', 0, 'udp://@225.1.1.240:30120', thumbnails + '', '')
	add_link('', 'DISNEY', 0, 'udp://@225.1.1.232:30120', thumbnails + '', '')
	add_link('', 'DISNEY JUNIOR', 0, 'udp://@225.1.1.233:30120', thumbnails + '', '')
	add_link('', 'BLOOMBERG', 0, 'udp://@225.1.1.227:30120', thumbnails + '', '')
	add_link('', 'CNN', 0, 'udp://@225.1.1.242:30120', thumbnails + '', '')
	add_link('', 'ARIRANG', 0, 'udp://@225.1.1.201:30120', thumbnails + '', '')
	add_link('', 'CHANNEL NEWS ASIA', 0, 'udp://@225.1.1.202:30120', thumbnails + '', '')
	add_link('', 'AUSTRALIA PLUS', 0, 'udp://@225.1.2.21:30120', thumbnails + '', '')
	add_link('', 'TV5MONDE', 0, 'udp://@225.1.1.200:30120', thumbnails + '', '')
	add_link('', 'DW', 0, 'udp://@225.1.1.203:30120', thumbnails + '', '')
	add_link('', 'NHK WORLD', 0, 'udp://@225.1.1.196:30120', thumbnails + '', '')
	add_link('', 'FOX SPORTS S1', 0, 'udp://@225.1.1.239:30120', thumbnails + '', '')
	add_link('', 'FOX SPORTS S2', 0, 'http://118.69.252.4/tv3/FoxSports/index.m3u8', thumbnails + '', '')
	add_link('', 'FOX SPORTS 2 S1', 0, 'udp://@225.1.1.241:30120', thumbnails + '', '')
	add_link('', 'FOX SPORTS 2 S2', 0, 'http://118.69.252.4/tv3/FoxSports2/index.m3u8', thumbnails + '', '')
	add_link('', 'STAR WORD', 0, 'udp://@225.1.1.204:30120', thumbnails + '', '')
	add_link('', 'MTV', 0, 'udp://@225.1.1.245:30120', thumbnails + '', '')
	add_link('', 'DIVA', 0, 'udp://@225.1.1.199:30120', thumbnails + '', '')
	add_link('', 'KBS WORLD', 0, 'udp://@225.1.2.91:30120', thumbnails + '', '')

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