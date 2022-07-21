import streamlit as st
from streamlit.components.v1 import html
import time
from PIL import Image
from functions import create_s3_client, read_s3_pickle, write_s3_pickle

st.set_page_config()

qr_enable = st.sidebar.radio('', ('Hide QR Code', 'Display Page QR Code'))
if qr_enable == 'Display Page QR Code':
	qr_image = Image.open('./QR_codes/future_qr-min.png')
	st.sidebar.image(qr_image, width=200)

st.title('“明天的我”')

st.write("若干年前，我们都在校园里，为Tripos奋斗，为明天感到迷茫，为拿一份工作的Offer操碎了心；今天的我们都在英国扎下了小小的一步脚印，并在这里重聚。无论你是在学术圈燃烧自己的青春和头发，还是身为社畜为社会做着绵薄的贡献，你还记得当初踏入校园或是初入社会时的初心吗？明天呢，你对明天有什么憧憬，5年之后你又希望成为什么样的人，过着什么样的生活呢？")

st.write("我们希望在这次以“时光”为主题的活动上尽一些自己小小的努力。请在这里留下你想对五年之后的自己说的话，剑桥校友会将于五年之后的2027年9月23日准时将以下的信息发到你提供的邮箱里。连同我们现在留下的，对未来的大家小小的祝福")
st.write('Love')
st.write('CUCCS Alumni Network')
st.text('——————————————————————————————————————————————————————')

content = st.text_area(label = 'Input message here', value = '')
email = st.text_input('your personal email')
name = st.text_input('Your preferred name', '未来的我自己')
submit = st.button('Submit')

s3_client = create_s3_client()
future_name = read_s3_pickle(s3_client, 'boatpartystreamlit2', 'future_name.pkl')
future_messages = read_s3_pickle(s3_client, 'boatpartystreamlit2', 'future_messages.pkl')


if submit:
	if '@' not in email:
		st.warning('enter a valid email address')
	else:
		if len(content) == 0 or content == 'Input message here':
			st.warning('对自己写点儿什么吧！')
		else:
			if email in future_messages.keys():
				st.info('重复提交不会覆盖之前的信息！你可以对自己唠叨唠叨再唠叨...')
				future_messages[email] = future_messages[email] + [content]
				future_name[email] = future_messages[email] + [name]
			else:
				future_messages[email] = [content]
				future_name[email] = [name]
			write_s3_pickle(s3_client, 'boatpartystreamlit2', 'future_name.pkl', future_name)
			write_s3_pickle(s3_client, 'boatpartystreamlit2', 'future_messages.pkl', future_messages)
			st.success("提交成功")
			st.write("祝一切好，五年后见！")


st.info('TODO: slightly tricky if we want to automate. Data (mapped content) should be stored separately in remote database as well as locally for safety. May also consider applying security control')
			

my_html = """
<script>
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 * 60 * 24 * 365 * 5,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};
</script>

<body>
  <div>Wait time is over in <span id="time">05:00</span> minutes!</div>
</body>
"""



html(my_html)


if st.button("这里还有个气球，点击就可以放飞！"):
	st.balloons()
	st.text('如果点到1000000下的话会有惊喜哦！')