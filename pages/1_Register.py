import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(page_title="สมัครสมาชิก", page_icon="📝")

st.title("📝 สมัครสมาชิกผู้ใช้งานใหม่")

with st.form("register_form"):
    name = st.text_input("ชื่อ-นามสกุล")
    phone = st.text_input("เบอร์โทรศัพท์")
    device_id = st.text_input("Device ID ของกล่องยา", value="BOX-001")
    
    submit_reg = st.form_submit_button("บันทึกข้อมูลสมัครสมาชิก", type="primary")

if submit_reg:
    if name and phone and device_id:
        try:
            res = requests.post(f"{API_BASE_URL}/users/register", json={
                "name": name,
                "phone": phone,
                "device_id": device_id
            })
            
            if res.status_code == 200 or res.status_code == 201:
                u_data = res.json()
                user_id = u_data.get("user_id")
                
                st.success("🎉 ลงทะเบียนสำเร็จเรียบร้อย!")
                st.info(f"🔑 **User ID ของคุณคือ:** `{user_id}`")
                
                # ล็อกอินเข้าใช้งานให้ทันที
                st.session_state["user_id"] = user_id
                st.session_state["user_name"] = name
            else:
                st.error("เกิดข้อผิดพลาดในการสร้างบัญชี")
        except Exception as e:
            st.error(f"❌ ไม่สามารถเชื่อมต่อกับ Backend ได้: {e}")
    else:
        st.warning("⚠️ กรุณากรอกข้อมูลให้ครบทุกช่อง")