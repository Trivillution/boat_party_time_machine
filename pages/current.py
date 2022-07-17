import streamlit as st


st.title('“嘿，朋友”')

st.write("曾经的同学，或是校友。或许一起结伴去过回味轩，或许在同一个Lecture Hall听过课，或许未曾谋面。无论如何，你们将会在我们的Boat Party上见到。你有什么想对Ta说的吗？")
st.text("请在这里留下你的话，可以是你今天的心情，一段你的回忆，不然的话，编个段子吧！")
ticket_number = st.text_input('your ticket number')
comments = st.text_area()

submit = st.button('Submit')

if submit:
	if ticket_number in ['', 'your ticket number']:
		st.text('请输入订单号（ticket number）')
	else:
		if len(comments) == 0:
			st.text('留一句话吧！不然小心当晚被踢下船哦')
		else:
			print('TODO: connect the comment into a database, store ticket number & need to map to user. On the boat day, user should submit the ticket number in exchange for their message')
			print('感谢提交！')