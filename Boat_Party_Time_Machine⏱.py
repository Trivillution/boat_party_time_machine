import streamlit as st
from PIL import Image
import pandas as pd

image = Image.open('./data/logo.PNG')
st.image(image, width=200)
st.title('CCS Alumni Boat Party 2022')

st.subheader('About US')

st.subheader('technical support contact')

st.subheader('留言板')
messages_df = pd.read_csv('./data/feedback.csv')
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
		messages_df.to_csv('./data/feedback.csv')


