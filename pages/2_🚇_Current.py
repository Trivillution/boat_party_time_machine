import streamlit as st
import numpy as np
from PIL import Image
from functions import create_s3_client, read_s3_pickle, write_s3_pickle

qr_enable = st.sidebar.radio('', ('Hide QR Code', 'Display Page QR Code'))
if qr_enable == 'Display Page QR Code':
	qr_image = Image.open('./QR_codes/current_qr-min.png')
	st.sidebar.image(qr_image, width=200)

st.title('“嘿，朋友”')

st.write("曾经的我们，或许一起结伴去过回味轩，或许在同一个Lecture Hall听过课，又或许素未平生。无论如何，我们都因剑桥这个纽带将在Boat Party相遇，你有什么想对Ta说的吗？")
st.text("请在这里留下你的话，可以是你今天的心情，可以是你的回忆，不然的话，编个段子吧！")
ticket_number = st.text_input('your ticket code')
comments = st.text_area('在此处留言')

s3_client = create_s3_client()
current_messages = read_s3_pickle(s3_client, 'boatpartystreamlit2', 'current_messages.pkl')

submit = st.button('Submit')

if submit:
	if len(comments) == 0:
		st.text('留一句话吧！不然小心当晚被踢下船哦')
	else:
		if ticket_number in ['', 'your ticket code']:
			st.text('请输入订单号（ticket code）')
		else:
			if ticket_number in current_messages.keys():
				st.info('你已经提交过了哟，重复提交会被我们当众鞭尸（当然不。）感谢你的热情！')
				current_messages[ticket_number] = current_messages[ticket_number] + [comments]
			else:
				current_messages[ticket_number] = [comments]
			st.success('感谢提交!')
			write_s3_pickle(s3_client, 'boatpartystreamlit2', 'current_messages.pkl', current_messages)


# st.info('TODO: connect the comment into a database, store ticket number & need to map to user. On the boat day, user should submit the ticket number in exchange for their message. Maybe can just try host on Github')
			
