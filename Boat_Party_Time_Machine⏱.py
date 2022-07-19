import streamlit as st
from PIL import Image
import pandas as pd
import s3fs
import os

image = Image.open('./data/logo.PNG')
st.image(image, width=200)
st.title('CCS Alumni Boat Party 2022')

st.subheader('About US')

st.subheader('technical support contact')

st.subheader('留言板')
fs = s3fs.S3FileSystem(anon=False)

@st.experimental_memo(ttl=60)
def read_file(filename):
	with fs.open(filename) as f:
		return f.read().decode("utf-8")

messages_df = read_file('boatpartystreamlit2/feedback.csv')
# messages_df = read_file('boatpartystreamlit/feedback.csv')
# messages_df = pd.read_csv('./data/feedback.csv')
for messages in messages_df.index:
	name = messages_df.loc[messages, 'Name']
	content = messages_df.loc[messages, 'Content']
	st.text(name + ':')
	st.text(content)


comment = st.text_area('有什么话想跟大家说的，请在这里留言哦')
name = st.text_input('昵称', '')
if st.button('submit'):
	if name == '':
		st.warning('请输入一个昵称')
	else:
		df2 = pd.DataFrame([[name,comment]], columns = ['Name', 'Content'])
		messages_df = messages_df.append(df2, ignore_index=True)
		# messages_df.to_csv('./data/feedback.csv')


