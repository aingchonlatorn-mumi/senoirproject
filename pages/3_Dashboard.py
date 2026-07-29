import streamlit as st

st.set_page_config(page_title="Dashboard - Smart Pill Box", page_icon="🏠")

# เช็คความปลอดภัย ถ้ายังไม่มี user ใน session ให้กลับไปหน้าหลัก
if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("กรุณาเข้าสู่ระบบก่อนใช้งาน")
    st.stop()

user = st.session_state["user"]

st.title(f"👋 สวัสดีคุณ {user.get('name', 'ผู้ใช้งาน')}")
st.markdown(f"🟢 **สถานะกล่องยา:** `{user.get('device_id', 'BOX-001')}`")
st.markdown(f"📱 **เบอร์โทรศัพท์:** {user.get('phone', '-')}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="ยาที่ต้องทานวันนี้", value="3 มื้อ", delta="ทานแล้ว 2 มื้อ")
with col2:
    st.metric(label="สถานะแบตเตอรี่", value="85%", delta="ปกติ")

st.subheader("🔔 แจ้งเตือนมื้อถัดไป")
st.info("⏰ **12:00 น.** — ยาลดความดัน (1 เม็ด) [ช่องที่ 1]")