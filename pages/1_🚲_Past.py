import streamlit as st
from PIL import Image
import numpy as np

st.title('“过去”')

st.write("每个人都在剑桥留下了不同的过去，不同的回忆。我们为每个人精心（其实是随机）准备了一张我们搜集到的过去的照片，点击下面一键领取吧！")

def show_image(random_number):
	image_name = './data/image' + str(random_number) + '.JPG'
	image = Image.open(image_name)
	st.image(image, width=800)



images = ['image1', 'image 2']

submitted_tickets = []
remaining_images = [1,2]

ticket_number = st.text_input('your ticket number')
ticket_mapping = {}


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
			st.text('No image left in database')
		else:
			random_number = np.random.choice(remaining_images, 1)[0]
			remaining_images.remove(random_number)
			show_image(random_number)
			submitted_tickets.append(ticket_number)
			ticket_mapping[ticket_number] = random_number

			st.success('成功领取!')




st.info('TODO: we will need a database if we want to provide the full-size image, google drive API worth a try?')
