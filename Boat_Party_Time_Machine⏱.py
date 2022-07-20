import streamlit as st
from PIL import Image
import pandas as pd
import os
import boto3
import io

image = Image.open('./data/logo.PNG')
st.image(image, width=200)
st.title('CCS Alumni Boat Party 2022')

st.subheader('About US')

st.subheader('technical support contact')

st.subheader('留言板')
st.text('🗻________________________________________________________________________________🗻')

@st.experimental_memo(ttl=60)
def read_file(filename):
	with fs.open(filename) as f:
		return f.read().decode("utf-8")

###########
AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    #aws_session_token=AWS_SESSION_TOKEN,
)
response = s3_client.get_object(Bucket='boatpartystreamlit2', Key="feedback.csv")
status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

if status == 200:
    print(f"Successful S3 get_object response. Status - {status}")
    messages_df = pd.read_csv(response.get("Body"))
else:
    st.error(f"Unsuccessful S3 get_object response. Status - {status}")


for messages in messages_df.index:
	name = messages_df.loc[messages, 'Name']
	content = messages_df.loc[messages, 'Content']
	st.text(name + ':')
	st.text(content)
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
		with io.StringIO() as csv_buffer:
			messages_df.to_csv(csv_buffer, index=False)

			response = s3_client.put_object(
				Bucket='boatpartystreamlit2', Key="feedback.csv", Body=csv_buffer.getvalue()
			)

			status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

			if status == 200:
				print(f"Successful S3 put_object response. Status - {status}")
			else:
				st.error(f"Unsuccessful S3 put_object response. Status - {status}")



#st.write('留言无法撤回。若需删除留言，请联系：chenyuanjie625@gmail.com')
st.markdown(""" <style> .font {
font-size:13px; font-family:Arial; color: #F0FFFF;} 
</style> """, unsafe_allow_html=True)
st.markdown('<p class="font">留言无法撤回。若需删除留言，请联系：chenyuanjie625@gmail.com</p>', unsafe_allow_html=True)
