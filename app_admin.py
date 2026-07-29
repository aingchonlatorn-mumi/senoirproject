import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime

# --- CONFIG & STYLING ---
st.set_page_config(
    page_title="Smart Pill Box - ระบบกล่องยาอัจฉริยะ",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS ตกแต่ง UI ให้สวยงามทันสมัย
st.markdown("""
<style>
    /* Global Styles */
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e293b; font-family: 'Kanit', sans-serif; }
    
    /* Card Container */
    .stCard {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    
    /* Profile Badge */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #e0f2fe;
        padding: 12px 16px;
        border-radius: 12px;
        color: #0369a1;
        margin-bottom: 20px;
    }
    
    /* Status Badge */
    .status-online {
        display: inline-block;
        padding: 4px 12px;
        background-color: #dcfce7;
        color: #15803d;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Custom Button Style */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        height: 48px;
    }
</style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000/api"
LIFF_ID = "2010881248-4xHWQGRQ"

# --- SESSION STATES ---
if "user" not in st.session_state:
    st.session_state["user"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# ดึง Params จาก Query String (ที่ LIFF ส่งมาให้)
line_id = st.query_params.get("line_id", None)
line_name = st.query_params.get("line_name", "")
line_pic = st.query_params.get("line_pic", "")

# --- 1. LIFF AUTO AUTHENTICATION ---
if not line_id and not st.session_state["user"]:
    liff_script = f"""
    <script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
    <script>
      async function initLiff() {{
        try {{
          await liff.init({{ liffId: "{LIFF_ID}" }});
          if (!liff.isLoggedIn()) {{
            liff.login();
          }} else {{
            const profile = await liff.getProfile();
            const currentUrl = new URL(window.location.href);
            
            if (!currentUrl.searchParams.get('line_id')) {{
              currentUrl.searchParams.set('line_id', profile.userId);
              currentUrl.searchParams.set('line_name', profile.displayName || '');
              currentUrl.searchParams.set('line_pic', profile.pictureUrl || '');
              
              if (window.parent && window.parent !== window) {{
                window.parent.location.href = currentUrl.toString();
              }} else {{
                window.location.href = currentUrl.toString();
              }}
            }}
          }}
        }} catch (e) {{ console.error("LIFF Error:", e); }}
      }}
      document.addEventListener("DOMContentLoaded", initLiff);
      initLiff();
    </script>
    """
    components.html(liff_script, height=0, width=0)

# --- 2. AUTO LOGIN BY LINE ID ---
if line_id and not st.session_state["user"]:
    try:
        res = requests.get(f"{API_BASE_URL}/users/line/{line_id}", timeout=3)
        if res.status_code == 200:
            st.session_state["user"] = res.json()
            st.session_state["page"] = "dashboard"
            st.rerun()
    except Exception:
        pass

# =========================================================
# 🔴 1. LANDING PAGE
# =========================================================
if not st.session_state["user"] and st.session_state["page"] == "landing":
    st.markdown("<h1 style='text-align: center;'>💊 Smart Pill Box</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>ระบบดูแลการทานยาอัจฉริยะ เชื่อมต่อตรงผ่าน LINE</p>", unsafe_allow_html=True)
    st.divider()

    if line_name:
        st.markdown(f"""
        <div class="user-profile">
            <img src="{line_pic if line_pic else 'https://cdn-icons-png.flaticon.com/512/847/847969.png'}" width="40" height="40" style="border-radius: 50%;">
            <div>
                <div style="font-size: 0.8rem; color: #0284c7;">เชื่อมต่อบัญชี LINE:</div>
                <div style="font-weight: 600;">{line_name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 เข้าสู่ระบบ", type="primary", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()
    with col2:
        if st.button("📝 ลงทะเบียนใหม่", use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()

# =========================================================
# 🔵 2. LOGIN PAGE
# =========================================================
elif not st.session_state["user"] and st.session_state["page"] == "login":
    st.subheader("🔑 เข้าสู่ระบบ")
    st.caption("กรอกเบอร์โทรศัพท์ที่ลงทะเบียนไว้กับกล่องยา")
    
    phone = st.text_input("📱 เบอร์โทรศัพท์", placeholder="เช่น 0812345678")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("เข้าสู่ระบบ", type="primary", use_container_width=True):
            if phone:
                with st.spinner("กำลังตรวจสอบข้อมูล..."):
                    try:
                        res = requests.get(f"{API_BASE_URL}/users/phone/{phone}")
                        if res.status_code == 200:
                            st.session_state["user"] = res.json()
                            st.session_state["page"] = "dashboard"
                            st.rerun()
                        else:
                            st.error("❌ ไม่พบเบอร์โทรศัพท์นี้ในระบบ")
                    except Exception:
                        st.error("❌ ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้")
            else:
                st.warning("กรุณากรอกเบอร์โทรศัพท์")
    with col2:
        if st.button("⬅️ ย้อนกลับ", use_container_width=True):
            st.session_state["page"] = "landing"
            st.rerun()

# =========================================================
# 🟢 3. REGISTER PAGE
# =========================================================
elif not st.session_state["user"] and st.session_state["page"] == "register":
    st.subheader("📝 สมัครสมาชิกใหม่")
    st.caption("ผูกกล่องยาอัจฉริยะกับบัญชี LINE ของคุณ")
    
    with st.form("reg_form"):
        name = st.text_input("👤 ชื่อ-นามสกุล", value=line_name)
        phone = st.text_input("📱 เบอร์โทรศัพท์", placeholder="08XXXXXXXX")
        device_id = st.text_input("🤖 รหัสกล่องยา (Device ID)", value="BOX-001")
        
        submit = st.form_submit_button("💾 ยืนยันการลงทะเบียน", type="primary", use_container_width=True)
        
    if submit:
        if name and phone:
            with st.spinner("กำลังลงทะเบียน..."):
                payload = {
                    "name": name,
                    "phone": phone,
                    "device_id": device_id,
                    "line_user_id": line_id if line_id else None
                }
                try:
                    res = requests.post(f"{API_BASE_URL}/users/register", json=payload)
                    if res.status_code == 200:
                        st.success("🎉 ลงทะเบียนสำเร็จ!")
                        st.session_state["user"] = res.json()
                        st.session_state["page"] = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ เกิดข้อผิดพลาดในการลงทะเบียน")
                except Exception as e:
                    st.error(f"❌ ไม่สามารถเชื่อมต่อระบบได้: {e}")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
            
    if st.button("⬅️ ย้อนกลับ", use_container_width=True):
        st.session_state["page"] = "landing"
        st.rerun()

# =========================================================
# 🏠 4. MAIN DASHBOARD PAGE (เมื่อ Login แล้ว)
# =========================================================
# --- ปรับแก้การดึงข้อมูล user ในหน้า Dashboard / Profile ---
if st.session_state["user"]:
    user = st.session_state["user"]
    
    # ดึงค่าพร้อมใส่ fallback หากไม่มีข้อมูล
    user_name = user.get('name') or "ผู้ใช้งาน"
    user_phone = user.get('phone') or "-"
    device_id = user.get('device_id') or "BOX-001"
    line_uid = user.get('line_user_id') or line_id or "ยังไม่ได้ผูก"

    # แสดงผล
    st.markdown(f"### สวัสดี, คุณ {user_name} 👋")
    st.markdown(f"🟢 **กล่องยาออนไลน์:** `{device_id}`")
    # Tab Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 หน้าหลัก", "💊 ยาของฉัน", "⏰ ตั้งเวลาทานยา", "👤 โปรไฟล์"])

    # --- TAB 1: DASHBOARD ---
    with tab1:
        st.subheader("📊 สรุปการทานยาวันนี้")
        
        # Stat Cards
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="ยาที่ต้องทานวันนี้", value="3 มื้อ", delta="ทานแล้ว 2 มื้อ")
        with col2:
            st.metric(label="สถานะกล่องยา", value="ปกติ 🟢", delta="แบตเตอรี่ 85%")

        st.divider()
        st.subheader("🔔 แจ้งเตือนมื้อถัดไป")
        st.info("⏰ **12:00 น.** — ยาลดความดัน (1 เม็ด) [ช่องใส่ยาที่ 1]")

    # --- TAB 2: MEDICINE MANAGEMENT ---
    with tab2:
        st.subheader("💊 จัดการรายชื่อยา")
        
        with st.expander("➕ เพิ่มรายการยาใหม่", expanded=False):
            with st.form("add_med"):
                med_name = st.text_input("ชื่อยา", placeholder="เช่น ยาลดความดัน")
                slot_no = st.number_input("ช่องใส่ยาในกล่อง (Slot)", min_value=1, max_value=4, value=1)
                total = st.number_input("จำนวนยาทั้งหมด (เม็ด)", min_value=1, value=20)
                exp_date = st.date_input("วันหมดอายุ", value=datetime.today())
                
                if st.form_submit_button("บันทึกข้อมูลยา", type="primary", use_container_width=True):
                    payload = {
                        "user_id": user.get("id"),
                        "name": med_name,
                        "slot": slot_no,
                        "total_pills": total,
                        "remaining_pills": total,
                        "expire_date": str(exp_date)
                    }
                    try:
                        res = requests.post(f"{API_BASE_URL}/medicines/", json=payload)
                        if res.status_code == 200:
                            st.success("บันทึกข้อมูลยาเรียบร้อย!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")

    # --- TAB 3: SCHEDULES ---
    with tab3:
        st.subheader("⏰ ตั้งเวลาการทานยา")
        with st.form("add_sched"):
            med_id = st.text_input("รหัสยา (Medicine ID)")
            time_str = st.time_input("เวลาที่ต้องทาน")
            dose = st.number_input("จำนวนที่ต้องทาน (เม็ด)", min_value=1, value=1)
            
            if st.form_submit_button("ตั้งเวลาแจ้งเตือน", type="primary", use_container_width=True):
                payload = {
                    "user_id": user.get("id"),
                    "medicine_id": med_id,
                    "time": time_str.strftime("%H:%M"),
                    "dose_amount": dose,
                    "active": True
                }
                try:
                    res = requests.post(f"{API_BASE_URL}/schedules/", json=payload)
                    if res.status_code == 200:
                        st.success("บันทึกตารางเวลาทานยาเรียบร้อย!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")

    # --- TAB 4: PROFILE ---
    with tab4:
        st.subheader("👤 ข้อมูลผู้ใช้งาน")
        st.write(f"**ชื่อ-นามสกุล:** {user.get('name')}")
        st.write(f"**เบอร์โทรศัพท์:** {user.get('phone')}")
        st.write(f"**Device ID:** `{user.get('device_id')}`")
        st.write(f"**LINE ID:** `{user.get('line_user_id', 'ยังไม่ได้ผูก')}`")
        
        st.divider()
        if st.button("🚪 ออกจากระบบ", type="secondary", use_container_width=True):
            st.session_state["user"] = None
            st.session_state["page"] = "landing"
            st.query_params.clear()
            st.rerun()