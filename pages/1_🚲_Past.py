import streamlit as st
from PIL import Image
import numpy as np
from functions import create_s3_client, read_s3_pickle, write_s3_pickle

qr_enable = st.sidebar.radio('', ('Hide QR Code', 'Display QR Code'))
if qr_enable == 'Display QR Code':
	qr_image = Image.open('./QR_codes/past_qr-min.png')
	st.sidebar.image(qr_image, width=200)

st.title('“过去”')

st.write("每个人都在剑桥留下了不同的过去，不同的回忆。我们为每个人精心（其实是随机）准备了一张我们搜集到的过去的照片，点击下面一键领取吧！")


def show_image(random_number):
	image_name = './data/image' + str(random_number) + '.JPG'
	image = Image.open(image_name)
	st.image(image, width=800)

s3_client = create_s3_client()
submitted_tickets = read_s3_pickle(s3_client, 'boatpartystreamlit2', 'past_redeemed_ticket_number.pkl')
ticket_mapping = read_s3_pickle(s3_client, 'boatpartystreamlit2', 'ticket_number_to_photo_id.pkl')
#images = ['image1', 'image 2']

all_images = {1,2} # needs update

occupied_images = set(ticket_mapping.values())
remaining_images = list(all_images - set(occupied_images))

ticket_number = st.text_input('your ticket number')



click = st.button("一键领取")
if click:
	if ticket_number in ['', 'your ticket number']:
		st.warning('请输入订单号（ticket number）')
	elif ticket_number in submitted_tickets:
		st.warning('请勿重复领取！以下是你的专属回忆照片：')
		random_number = ticket_mapping[ticket_number]
		show_image(random_number)
	else:

		if len(remaining_images) == 0:
			st.warning('No unique image remaining in database, however, I can give you a duplicated one')
			random_number = np.random.choice(list(all_images), 1)[0] 
			show_image(random_number)
		else:
			random_number = np.random.choice(remaining_images, 1)[0]
			remaining_images.remove(random_number)
			show_image(random_number)
			submitted_tickets.append(ticket_number)
			ticket_mapping[ticket_number] = random_number
			write_s3_pickle(s3_client, 'boatpartystreamlit2', 'past_redeemed_ticket_number.pkl', submitted_tickets)
			write_s3_pickle(s3_client, 'boatpartystreamlit2', 'ticket_number_to_photo_id.pkl', ticket_mapping)


			st.success('成功领取!')




st.info('TODO: we will need a database if we want to provide the full-size image, google drive API worth a try?')
