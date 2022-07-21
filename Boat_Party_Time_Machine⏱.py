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
if qr_enable == 'Display QR Code':
	qr_image = Image.open('./QR_codes/main_qr-min.png')
	st.sidebar.image(qr_image, width=200)


image = Image.open('./data/logo.PNG')
st.image(image, width=200)
st.title('CCS Alumni Boat Party 2022')

st.subheader('About US')

st.subheader('technical support contact')

st.subheader('留言板')
st.text('🗻________________________________________________________________________________🗻')

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
	st.text('——————————————————')

st.text('🗻________________________________________________________________________________🗻')
comment = st.text_area('有什么话想跟大家说的，请在这里留言哦')
name = st.text_input('昵称', '')
if st.button('submit'):
	if name == '':
		st.warning('请输入一个昵称')
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
# st.markdown('<p class="font">留言无法撤回。若需删除留言，请联系：chenyuanjie625@gmail.com</p>', unsafe_allow_html=True)
st.text('⚠️留言无法撤回。若需删除留言，请联系：chenyuanjie625@gmail.com')
