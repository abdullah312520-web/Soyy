import streamlit as st
import time
import os
import requests  # เพิ่มตัวนี้เพื่อดึงพิกัด


# --- ตั้งค่าหน้าเว็บ ---
def get_user_ip():
    headers = st.context.headers
    # ดึงค่า IP จาก X-Forwarded-For (ที่ Streamlit Cloud ส่งมา)
    forwarded = headers.get("X-Forwarded-For", "")
    if forwarded:
        # เอา IP ตัวแรกสุด และลบช่องว่างออก
        ip_list = [ip.strip() for ip in forwarded.split(",")]
        # กรองเอา IP ตัวที่ไม่ใช่ Local (ไม่ใช่ 10.x, 127.x, 172.x)
        for ip in ip_list:
            if not (ip.startswith("10.") or ip.startswith("127.") or ip.startswith("172.") or ip.startswith("192.")):
                return ip
        return ip_list[0] # ถ้าหาไม่เจอจริงๆ ให้เอาตัวแรก
    return "Unknown"

def get_location_info(ip):
    # ถ้า IP เป็นค่าว่าง หรือหาไม่เจอ
    if ip == "Unknown" or not ip:
        return "พิกัดลับ (ระบบป้องกัน IP)"
        
    try:
        # ใช้ API ipapi.co (เสถียรที่สุดสำหรับมือถือ)
        url = f"https://ipapi.co{ip}/json/"
        # ใส่ Header เล็กน้อยเพื่อให้ API ยอมรับการเรียกข้อมูล
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        
        if "city" in response:
            city = response.get("city", "ไม่ระบุเมือง")
            region = response.get("region", "ไม่ระบุจังหวัด")
            country = response.get("country_name", "ไทย")
            return f"{city}, {region}, {country}"
    except:
        pass
    return "ไม่ทราบพิกัด (ข้อมูลถูกพราง)"


# --- CSS ตกแต่งหน้าจอ ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; overflow: hidden; }
    .spam-text {
        position: fixed;
        font-weight: 900;
        text-transform: uppercase;
        pointer-events: none;
        z-index: 0;
        white-space: nowrap;
    }
    @keyframes scroll-left { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    @keyframes scroll-right { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
    .h1 { top: 2%; font-size: 20px; color: rgba(0, 191, 255, 0.4); animation: scroll-left 4s linear infinite; }
    .h2 { top: 8%; font-size: 15px; color: rgba(30, 144, 255, 0.2); animation: scroll-right 6s linear infinite; }
    .h3 { top: 15%; font-size: 25px; color: rgba(0, 255, 255, 0.3); animation: scroll-left 8s linear infinite; }
    .h4 { top: 25%; font-size: 12px; color: rgba(255, 255, 255, 0.1); animation: scroll-right 12s linear infinite; }
    .h5 { bottom: 2%; font-size: 20px; color: rgba(0, 191, 255, 0.4); animation: scroll-right 5s linear infinite; }
    .h6 { bottom: 10%; font-size: 18px; color: rgba(30, 144, 255, 0.2); animation: scroll-left 7s linear infinite; }
    .h7 { bottom: 18%; font-size: 30px; color: rgba(0, 255, 255, 0.1); animation: scroll-right 10s linear infinite; }
    .h8 { bottom: 28%; font-size: 14px; color: rgba(255, 255, 255, 0.2); animation: scroll-left 15s linear infinite; }
    @keyframes scroll-down { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
    @keyframes scroll-up { 0% { transform: translateY(100%); } 100% { transform: translateY(-100%); } }
    .v1 { left: 2%; writing-mode: vertical-rl; font-size: 20px; color: rgba(0, 191, 255, 0.3); animation: scroll-down 5s linear infinite; }
    .v2 { left: 8%; writing-mode: vertical-rl; font-size: 15px; color: rgba(30, 144, 255, 0.1); animation: scroll-up 8s linear infinite; }
    .v3 { left: 15%; writing-mode: vertical-rl; font-size: 25px; color: rgba(0, 255, 255, 0.2); animation: scroll-down 12s linear infinite; }
    .v4 { right: 2%; writing-mode: vertical-rl; font-size: 20px; color: rgba(0, 191, 255, 0.3); animation: scroll-up 6s linear infinite; }
    .v5 { right: 10%; writing-mode: vertical-rl; font-size: 18px; color: rgba(30, 144, 255, 0.1); animation: scroll-down 9s linear infinite; }
    .v6 { right: 20%; writing-mode: vertical-rl; font-size: 30px; color: rgba(0, 255, 255, 0.05); animation: scroll-up 15s linear infinite; }
    .block-container { display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; z-index: 100; }
    .shaking-blue {
        font-size: 60px !important;
        font-weight: 900;
        background: linear-gradient(to right, #0000FF, #00BFFF, #1E90FF, #00FFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 100%;
        animation: blue-move 2s linear infinite, shake-move 0.1s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes blue-move { 0% { background-position: 0% 50%; } 100% { background-position: 100% 50%; } }
    @keyframes shake-move { 0% { transform: translate(2px, 2px); } 50% { transform: translate(-2px, -2px); } 100% { transform: translate(2px, -2px); } }
    input, textarea { color: #00BFFF !important; background-color: rgba(0, 0, 0, 0.9) !important; border: 1px solid #1E90FF !important; text-align: center; }
    label { color: #1E90FF !important; width: 100%; text-align: center; }
    .stButton > button { width: 100% !important; max-width: 450px; background-color: transparent !important; color: #00BFFF !important; border: 2px solid #1E90FF !important; border-radius: 30px !important; font-weight: bold; transition: 0.4s; }
    .stButton > button:hover { background-color: #1E90FF !important; color: white !important; box-shadow: 0 0 30px #00BFFF !important; transform: scale(1.05); }
    img { border: 4px solid #1E90FF; box-shadow: 0 0 25px #00BFFF; border-radius: 15px; }
    </style>

    <div class="spam-text h1">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text h2">I SEE YOU I SEE YOU I SEE YOU I SEE YOU I SEE YOU</div>
    <div class="spam-text h3">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text h4">HACKED HACKED HACKED HACKED HACKED HACKED HACKED</div>
    <div class="spam-text h5">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text h6">ACCESS DENIED ACCESS DENIED ACCESS DENIED ACCESS DENIED</div>
    <div class="spam-text h7">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text h8">GET OUT GET OUT GET OUT GET OUT GET OUT GET OUT</div>
    <div class="spam-text v1">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text v2">WATCHING YOU WATCHING YOU WATCHING YOU</div>
    <div class="spam-text v3">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text v4">SYSTEM FAILURE SYSTEM FAILURE SYSTEM FAILURE</div>
    <div class="spam-text v5">ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ ส่องเพื่อออ</div>
    <div class="spam-text v6">WHO ARE YOU? WHO ARE YOU? WHO ARE YOU?</div>
    <div class="shaking-blue">ส่องเพื่อออ</div>
    """, unsafe_allow_html=True)

# --- ส่วนรูปภาพ (แก้ไขเป็น GIF) ---
gif_path = "robot.gif"  # <-- เปลี่ยนชื่อไฟล์ให้ตรงกับไฟล์ GIF ของคุณ
if os.path.exists(gif_path):
    st.image(gif_path, width=450)
else:
    st.error("ไม่พบไฟล์ GIF! (ตรวจสอบชื่อไฟล์ robot.gif)")

# --- ระบบส่งข้อความ ---
if 'last_time' not in st.session_state:
    st.session_state.last_time = 0

st.markdown("<br>", unsafe_allow_html=True)
name = st.text_input("ระบุตัวตน (ชื่อ):", placeholder="ใครน่ะ?")
msg = st.text_area("ส่งข้อความลับมา:", placeholder="พิมพ์มาซะดีๆ...")

if st.button("SEND MESSAGE"):
    now = time.time()
    user_ip = get_user_ip() 
    user_loc = get_location_info(user_ip) # <-- ดึงจังหวัด/ประเทศ

    if now - st.session_state.last_time < 5:
        st.error(f"รอก่อน! อีก {int(5 - (now - st.session_state.last_time))} วิ")
    elif name and msg:
        st.session_state.last_time = now
        
        # มัดรวมข้อมูลดิบ (วันเวลา | IP | พิกัด | ชื่อ | ข้อความ)
        log_entry = f"📍 [{time.strftime('%H:%M:%S')}] IP: {user_ip} ({user_loc}) | NAME: {name} | MSG: {msg}"
        
        print(log_entry, flush=True) # พ่นออกหน้า Logs ดำๆ ทันที
        
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
            
        st.toast(f"ตรวจพบพิกัดจาก {user_loc}!", icon='🛰️')
        st.success("ส่งเรียบร้อย! (เรารู้นะว่าคุณอยู่ที่ไหน...)")
    else:
        st.warning("กรอกให้ครบก่อน!")
