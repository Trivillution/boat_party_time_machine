import streamlit as st
from PIL import Image
import pandas as pd
import os
import boto3
import io

from functions import *

# AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']
qr_enable = st.sidebar.radio('', ('Hide QR Code', 'Display Page QR Code'))
if qr_enable == 'Display Page QR Code':
	qr_image = Image.open('./QR_codes/main_qr-min.png')
	st.sidebar.image(qr_image, width=200)


image = Image.open('./data/logo.PNG')
st.image(image, width=200)
st.title('CCS Alumni Boat Party 2022')

st.subheader('About US')

st.subheader('technical support contact')

st.subheader('็่จๆฟ')
st.text('๐ป________________________________________________________________________________๐ป')

s3_client = create_s3_client()

messages_df = read_s3_df(s3_client, bucket='boatpartystreamlit2', key="feedback.csv")
messages_df = messages_df[['Name', 'Content']]

for messages in messages_df.index:
	name = messages_df.loc[messages, 'Name']
	content = messages_df.loc[messages, 'Content']
	# st.markdown(""" <style> .font {
	# font-size:13px; font-family:Arial; color: #F0FFFF;} 
	# </style> """, unsafe_allow_html=True)
	# st.markdown('<p class="font">{}</p>'.format(name + ':'), unsafe_allow_html=True)
	st.caption(name + ':')
	st.markdown(""" <style> .font {
	font-size:13px; font-family:Arial; font-style:italic; color: #F0FFFF;} 
	</style> """, unsafe_allow_html=True)
	st.markdown('<p class="font">{}</p>'.format(content), unsafe_allow_html=True)

	#st.text(content)
	st.text('โโโโโโโโโโโโโโโโโโ')

st.text('๐ป________________________________________________________________________________๐ป')
comment = st.text_area('ๆไปไน่ฏๆณ่ทๅคงๅฎถ่ฏด็๏ผ่ฏทๅจ่ฟ้็่จๅฆ')
name = st.text_input('ๆต็งฐ', '')
if st.button('submit'):
	if name == '':
		st.warning('่ฏท่พๅฅไธไธชๆต็งฐ')
	else:
		df2 = pd.DataFrame([[name,comment]], columns = ['Name', 'Content'])
		messages_df = messages_df.append(df2, ignore_index=True)

		# write message back to s3
		write_df_to_s3(s3_client, messages_df, bucket='boatpartystreamlit2', key="feedback.csv")
		

def show_s3_image(bucket, key):
	response_image = s3_client.get_object(Bucket=bucket, Key=key)
	st.image(Image.open(response_image.get("Body")), width=800)

show_s3_image(bucket='boatpartystreamlit2', key="JJC_5143.jpeg")

# st.markdown(""" <style> .font {
# font-size:13px; font-family:Arial; color: #F0FFFF;} 
# </style> """, unsafe_allow_html=True)
# st.markdown('<p class="font">็่จๆ?ๆณๆคๅใ่ฅ้ๅ?้ค็่จ๏ผ่ฏท่็ณป๏ผchenyuanjie625@gmail.com</p>', unsafe_allow_html=True)
st.text('โ?๏ธ็่จๆ?ๆณๆคๅใ่ฅ้ๅ?้ค็่จ๏ผ่ฏท่็ณป๏ผchenyuanjie625@gmail.com')
