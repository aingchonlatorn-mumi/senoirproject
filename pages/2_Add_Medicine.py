import streamlit as st
import requests
from datetime import time

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(page_title="เพิ่มข้อมูลยา", page_icon="💊")

st.title("💊 เพิ่มข้อมูลยาและตั้งเวลาทานยา")

# ตรวจสอบการ Login
if "user_id" not in st.session_state or not st.session_state["user_id"]:
    st.warning("⚠️ กรุณาเข้าสู่ระบบที่หน้าแรก หรือ สมัครสมาชิก ก่อนทำรายการ")
    st.stop()

st.write(f"กำลังตั้งค่าให้ผู้ใช้: **{st.session_state.get('user_name')}** (ID: `{st.session_state['user_id']}`)")
st.divider()

# --- ส่วนที่ 1: ข้อมูลยา ---
st.subheader("1. ข้อมูลรายละเอียดของยา")
med_name = st.text_input("ชื่อยา")
col1, col2 = st.columns(2)
with col1:
    total_pills = st.number_input("จำนวนยาทั้งหมด (เม็ด)", min_value=1, value=30)
with col2:
    expire_date = st.date_input("วันหมดอายุ")

st.divider()

# --- ส่วนที่ 2: ตั้งเวลาทานยา ---
st.subheader("2. กำหนดเวลาทานยา")

meal_preset = st.radio(
    "เลือกชุดเวลากินยาสำเร็จรูป",
    ["กำหนดมื้อเอง", "หลังอาหาร 3 มื้อ (07:00, 12:00, 18:00)", "ก่อนอาหาร 3 มื้อ (06:30, 11:30, 17:30)"],
    horizontal=True
)

times_and_doses = []

if "3 มื้อ" in meal_preset:
    dose = st.number_input("จำนวนเม็ดต่อมื้อ", min_value=1, value=1)
    if "หลังอาหาร" in meal_preset:
        times_and_doses = [{"time": "07:00", "dose": dose}, {"time": "12:00", "dose": dose}, {"time": "18:00", "dose": dose}]
    else:
        times_and_doses = [{"time": "06:30", "dose": dose}, {"time": "11:30", "dose": dose}, {"time": "17:30", "dose": dose}]
else:
    num_times = st.number_input("จำนวนมื้อต่อวัน", min_value=1, max_value=4, value=1)
    for i in range(int(num_times)):
        c1, c2 = st.columns(2)
        with c1:
            t = st.time_input(f"มื้อที่ {i+1}: เวลา", value=time(8, 0), key=f"t_{i}")
        with c2:
            d = st.number_input(f"มื้อที่ {i+1}: จำนวนเม็ด", min_value=1, value=1, key=f"d_{i}")
        times_and_doses.append({"time": t.strftime("%H:%M"), "dose": d})

days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

st.divider()

if st.button("💾 บันทึกตารางทานยา", type="primary", use_container_width=True):
    if not med_name:
        st.warning("⚠️ กรุณากรอกชื่อยา")
    else:
        try:
            # 1. บันทึกข้อมูลยา
            m_res = requests.post(f"{API_BASE_URL}/medicines/", json={
                "user_id": st.session_state["user_id"],
                "name": med_name,
                "total_pills": total_pills,
                "remaining_pills": total_pills,
                "expire_date": str(expire_date)
            }).json()
            
            med_id = m_res.get("medicine_id")

            # 2. บันทึกตารางเวลากินยา
            for slot in times_and_doses:
                requests.post(f"{API_BASE_URL}/schedules/", json={
                    "user_id": st.session_state["user_id"],
                    "medicine_id": med_id,
                    "time": slot["time"],
                    "days_of_week": days,
                    "dose_amount": slot["dose"],
                    "active": True
                })

            st.success("🎉 บันทึกข้อมูลยาและตารางเวลาเรียบร้อยแล้ว!")
            st.balloons()
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")