# Smart Medicine Box — Phase 1: Core Backend & Database

Backend API (FastAPI) + Firebase Firestore สำหรับจัดการ user / medicine / schedule

## โครงสร้างโปรเจค
```
smart-medbox-backend/
├── app/
│   ├── main.py              # entry point
│   ├── firebase_config.py   # เชื่อมต่อ Firestore
│   ├── models.py            # pydantic schema
│   └── routers/
│       ├── users.py
│       ├── medicines.py
│       └── schedules.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## ขั้นตอนที่ 1 — สร้าง Firebase Project

1. ไปที่ https://console.firebase.google.com → **Add project** → ตั้งชื่อ เช่น `smart-medbox`
2. ในเมนูซ้าย ไปที่ **Build > Firestore Database** → กด **Create database** → เลือก mode **Production** → เลือก location (เช่น `asia-southeast1`)
3. ไปที่ **Project settings (ไอคอนเฟือง) > Service accounts** → กด **Generate new private key** → จะได้ไฟล์ `.json` ดาวน์โหลดมา
4. เปลี่ยนชื่อไฟล์ที่ดาวน์โหลดเป็น `serviceAccountKey.json`

## ขั้นตอนที่ 2 — เปิดโปรเจคใน VS Code

1. เปิดโฟลเดอร์ `smart-medbox-backend` ด้วย VS Code (`File > Open Folder`)
2. วาง `serviceAccountKey.json` ไว้ที่ root ของโปรเจค (ระดับเดียวกับ `requirements.txt`) — **ห้าม commit ไฟล์นี้ขึ้น git** (มีอยู่ใน `.gitignore` แล้ว)
3. เปิด Terminal ใน VS Code (`Terminal > New Terminal`) แล้วสร้าง virtual environment:

   **Windows:**
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **Mac/Linux:**
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   > ถ้า VS Code ถาม "Select interpreter" ให้เลือกตัวที่อยู่ใน `.venv`

4. ติดตั้ง dependencies:
   ```
   pip install -r requirements.txt
   ```

5. สร้างไฟล์ `.env` โดยคัดลอกจาก `.env.example`:
   ```
   cp .env.example .env
   ```
   (Windows ใช้ `copy .env.example .env`)

   เปิด `.env` แล้วตรวจสอบว่า path ตรงกับที่วางไฟล์ `serviceAccountKey.json` ไว้จริง

## ขั้นตอนที่ 3 — รัน server

```
uvicorn app.main:app --reload
```

ถ้าสำเร็จจะเห็น log ประมาณ `Uvicorn running on http://127.0.0.1:8000`

เปิดเบราว์เซอร์ไปที่:
- `http://127.0.0.1:8000` → health check
- `http://127.0.0.1:8000/docs` → **Swagger UI** ทดสอบ API ได้ทันทีจากหน้านี้ (แนะนำให้ใช้หน้านี้ทดสอบทุก endpoint)

## ขั้นตอนที่ 4 — ทดสอบ flow ตาม Case 1

ใน `/docs` ลองยิงตามลำดับนี้:

1. `POST /users` — สร้าง user ใหม่ (ระบุ name, phone, device_id)
   → เก็บ `id` ที่ได้กลับมา
2. `POST /medicines` — เพิ่มยา โดยใส่ `user_id` จากข้อ 1, `name`, `total_pills`, `expire_date`
   → เก็บ `id` ของยา
3. `POST /schedules` — ตั้งเวลากินยา โดยใส่ `user_id`, `medicine_id`, `time` (เช่น "08:00"), `days_of_week` (เช่น `["daily"]`), `dose_amount`
4. `GET /medicines?user_id=...` — เช็คว่ายาถูกบันทึกจริง
5. `GET /schedules?user_id=...` — เช็คตารางเวลา
6. `PATCH /users/{user_id}/line?line_user_id=...` — จำลองการผูก LINE (ตอนนี้ยังเป็นค่าจำลอง เพราะ LINE integration จะทำใน phase ถัดไป)

ถ้าทุก endpoint ทำงานและเห็นข้อมูลใน Firebase Console (Firestore Database) แปลว่า Phase 1 เสร็จสมบูรณ์

## Endpoints ทั้งหมด

| Method | Path | คำอธิบาย |
|---|---|---|
| POST | /users | สร้าง user |
| GET | /users | list user ทั้งหมด |
| GET | /users/{id} | ดู user รายคน |
| PATCH | /users/{id}/line | ผูก line_user_id |
| DELETE | /users/{id} | ลบ user |
| POST | /medicines | เพิ่มยา |
| GET | /medicines?user_id= | list ยา (filter ตาม user) |
| GET | /medicines/{id} | ดูยารายตัว |
| PUT | /medicines/{id} | แก้ไขยา (เช่น ลด remaining_pills) |
| DELETE | /medicines/{id} | ลบยา |
| POST | /schedules | ตั้งเวลากินยา |
| GET | /schedules?user_id=&medicine_id= | list ตารางเวลา |
| GET | /schedules/{id} | ดูตารางเวลารายตัว |
| PUT | /schedules/{id} | แก้ไขตารางเวลา |
| DELETE | /schedules/{id} | ลบตารางเวลา |

## ปัญหาที่มักเจอ

- **`FileNotFoundError: serviceAccountKey.json`** → เช็คว่าวางไฟล์ถูกตำแหน่งและ path ใน `.env` ถูกต้อง
- **`ModuleNotFoundError`** → ลืม activate venv หรือยังไม่ได้ `pip install -r requirements.txt`
- **Firestore permission denied** → service account key ต้องมาจาก project เดียวกับที่สร้าง Firestore database

## ขั้นตอนถัดไป (Phase 2+)

เมื่อ Phase 1 รันได้ครบแล้ว แจ้งได้เลยว่าพร้อมทำ Phase 2 (ESP32 firmware เชื่อมกับ backend นี้) หรือ Phase 3 (LINE Messaging API webhook)
