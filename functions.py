import streamlit as st
from PIL import Image
import pandas as pd
import os
import boto3
import io
import pickle

def write_df_to_s3(s3_client, messages_df, bucket, key):
	# write message back to s3
	with io.StringIO() as csv_buffer:
		messages_df.to_csv(csv_buffer, index=False)

		response = s3_client.put_object(
			Bucket=bucket, Key=key, Body=csv_buffer.getvalue()
		)

		status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

		if status == 200:
			print(f"Successful S3 put_object response. Status - {status}")
		else:
			st.error(f"Unsuccessful S3 put_object response. Status - {status}")

def show_s3_image(s3_client, bucket, key):
	response_image = s3_client.get_object(Bucket=bucket, Key=key)
	st.image(Image.open(response_image.get("Body")), width=800)

def create_s3_client():
	AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID']
	AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']
	s3_client = boto3.client(
	    "s3",
	    aws_access_key_id=AWS_ACCESS_KEY_ID,
	    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
	    #aws_session_token=AWS_SESSION_TOKEN,
	)
	return s3_client

def read_s3_df(s3_client, bucket, key):
	response = s3_client.get_object(Bucket=bucket, Key=key)
	status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

	if status == 200:
	    print(f"Successful S3 get_object response. Status - {status}")
	    messages_df = pd.read_csv(response.get("Body"))
	else:
	    st.error(f"Unsuccessful S3 get_object response. Status - {status}")
	return messages_df

def read_s3_pickle(s3_client, bucket, key):
	response = s3_client.get_object(Bucket=bucket, Key=key)
	my_pickle = pickle.loads(response.get("Body").read())
	return my_pickle

def write_s3_pickle(s3_client, bucket, key, my_pickle):
	pickle_byte_obj = pickle.dumps(my_pickle)
	s3_client.put_object(Bucket=bucket, Key=key, Body=pickle_byte_obj)


