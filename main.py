#-*-coding:utf-8-*- #

import requests

# r = requests.get('https://m.weibo.cn/p/index?containerid=2304131664607484_-_WEIBO_SECOND_PROFILE_MORE_WEIBO')
# https://m.weibo.cn/api/container/getIndex?containerid=2304131664607484_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03


def get_data(containerid):
	page = 1

	while page:
		url = 'https://m.weibo.cn/api/container/getIndex?containerid=%d&page=%d' % (containerid,page)
		r = requests.get(url)

		if r.status_code != 200:
			break
		else :
			json = r.json()
			if json['ok'] == 0:
				break
			else:
				for i,card in enumerate(json['data']['cards']):
					if card['card_type'] == 58:
						return
					if card['card_type'] != 9:
						continue

					print('正在处理第%d页的第%d条微博'%(page,i+1))

					blog_data = {}
					blog_data['text'] = card['mblog']['text']
					blog_data['created_at'] = card['mblog']['created_at']
					blog_data['retweeted_status'] = 'retweeted_status' in card['mblog']
					blog_data['retweeted_text'] = card['mblog']['retweeted_status']['text'] if 'retweeted_status' in card['mblog'] else None
					blog_data['pics'] =  list(map(lambda pic:pic['url'],card['mblog']['pics'])) if 'pics' in card['mblog'] else []
					data_list.append(blog_data)

			page+=1

def handle_data():
	if len(data_list) == 0:
		return
	else:
		text = ''
		for blog in data_list:
			text += '''

	微博内容:%s 

	是否转发:%s 

	原博内容:%s 

	发布日期:%s 

	微博图片:%s 

======================================================================================''' % (blog['text'],'yes' if blog['retweeted_status'] else 'no',blog['retweeted_text'] if blog['retweeted_status'] else '',blog['created_at'],',\r\n'.join(blog['pics']))


		with open('./weibo.txt','w+',encoding='utf-8') as f:
			f.write(text)


data_list = []


if __name__ == '__main__':

	while True:
		try:
			containerid = int(input('请输入你的containerid: '))
			break
		except ValueError:
			print("请输入有效的数字")

	get_data(containerid)
	handle_data()






