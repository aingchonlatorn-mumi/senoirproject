import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/api"

st.title("ระบบลงทะเบียนตู้ยาอัจฉริยะ")

with st.form("register_form"):
    st.subheader("1. ข้อมูลผู้ใช้งาน")
    name = st.text_input("ชื่อ-นามสกุล")
    phone = st.text_input("เบอร์โทรศัพท์")
    device_id = st.text_input("Device ID ของกล่องยา (เช่น BOX-001)")
    
    st.subheader("2. ข้อมูลยา")
    med_name = st.text_input("ชื่อยา")
    total_pills = st.number_input("จำนวนเม็ดทั้งหมด", min_value=1, value=30)
    expire_date = st.date_input("วันหมดอายุ")
    
    st.subheader("3. ตั้งเวลากินยา")
    time_slot = st.time_input("เวลาที่ต้องทาน")
    dose_amount = st.number_input("จำนวนเม็ดต่อครั้ง", min_value=1, value=1)
    days = st.multiselect(
        "วันที่ต้องทาน", 
        ["mon", "tue", "wed", "thu", "fri", "sat", "sun"], 
        default=["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    )

    submitted = st.form_submit_button("บันทึกข้อมูล")

if submitted:
    try:
        # 1. สมัคร User
        u_res = requests.post(f"{API_BASE_URL}/users/register", json={
            "name": name, "phone": phone, "device_id": device_id
        }).json()
        user_id = u_res["user_id"]

        # 2. เพิ่ม ยา
        m_res = requests.post(f"{API_BASE_URL}/medicines/", json={
            "user_id": user_id,
            "name": med_name,
            "total_pills": total_pills,
            "remaining_pills": total_pills,
            "expire_date": str(expire_date)
        }).json()
        med_id = m_res["medicine_id"]

        # 3. ตั้ง Schedule
        requests.post(f"{API_BASE_URL}/schedules/", json={
            "user_id": user_id,
            "medicine_id": med_id,
            "time": time_slot.strftime("%H:%M"),
            "days_of_week": days,
            "dose_amount": dose_amount,
            "active": True
        })

        st.success("บันทึกข้อมูลเรียบร้อยแล้ว!")
        st.info(f"User ID ของคุณคือ: {user_id}")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการบันทึก: {e}")