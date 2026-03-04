import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. إعدادات المجلدات
for folder in ["vehicle_files", "data"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 2. وظيفة حفظ وتحديث البيانات
def save_data(vin, plate, custom_id, car_type, color):
    file_path = "data/vehicles_db.csv"
    new_data = pd.DataFrame([[vin, plate, custom_id, car_type, color]], 
                            columns=["الهيكل", "اللوحة", "البطاقة", "النوع", "اللون"])
    if os.path.exists(file_path):
        db = pd.read_csv(file_path)
        # إذا كانت السيارة موجودة مسبقاً (بناءً على الهيكل أو اللوحة)، نقوم بتحديثها
        db = pd.concat([db, new_data]).drop_duplicates(subset=["الهيكل", "اللوحة"], keep='last')
        db.to_csv(file_path, index=False)
    else:
        new_data.to_csv(file_path, index=False)

# --- واجهة التطبيق ---
st.set_page_config(page_title="نظام أرشفة النقل", layout="wide")
st.title("🚗 نظام إدارة وأرشفة أسطول المركبات")

menu = ["🔍 البحث والتعديل", "🆕 إضافة مركبة جديدة"]
choice = st.sidebar.selectbox("القائمة", menu)

# --- قسم إضافة مركبة (خانات اختيارية) ---
if choice == "🆕 إضافة مركبة جديدة":
    st.header("تسجيل بيانات مركبة")
    col1, col2 = st.columns(2)
    with col1:
        vin = st.text_input("رقم الهيكل (اختياري)")
        plate = st.text_input("رقم اللوحة (اختياري)")
    with col2:
        custom_id = st.text_input("رقم البطاقة الجمركية (اختياري)")
        car_type = st.text_input("نوع السيارة")
    
    color = st.text_input("اللون")
    
    if st.button("حفظ البيانات الأساسية"):
        if vin or plate or custom_id:
            save_data(vin, plate, custom_id, car_type, color)
            st.success("✅ تم حفظ البيانات بنجاح!")
        else:
            st.error("⚠️ يرجى إدخال معلومة واحدة على الأقل (هيكل، لوحة، أو بطاقة).")

# --- قسم البحث والتعديل (إضافة صور/ملفات لسيارة موجودة) ---
elif choice == "🔍 البحث والتعديل":
    st.header("البحث عن سيارة وتحديث ملفاتها")
    query = st.text_input("ابحث برقم الهيكل، اللوحة، أو البطاقة الجمركية")
    
    if query:
        if os.path.exists("data/vehicles_db.csv"):
            db = pd.read_csv("data/vehicles_db.csv")
            # بحث مرن في كل الخانات
            result = db[(db['الهيكل'].astype(str) == query) | (db['اللوحة'].astype(str) == query) | (db['البطاقة'].astype(str) == query)]
            
            if not result.empty:
                car = result.iloc[0]
                st.write(f"📂 **ملف السيارة:** {car['النوع']} - {car['اللون']}")
                
                # خيارات الإضافة (صور أو استمارات)
                st.subheader("➕ إضافة/تعديل المرفقات")
                upload_type = st.radio("ماذا تريد أن تضيف؟", ["صورة سيارة", "ملف استمارة (PDF)", "مستند آخر"])
                
                uploaded_file = st.file_uploader("اختر الملف أو التقط صورة")
                
                if st.button("تحديث الملف"):
                    if uploaded_file:
                        # تسمية الملف باسم السيارة ونوعه لعدم التكرار
                        ext = uploaded_file.name.split('.')[-1]
                        ref = car['الهيكل'] if pd.notnull(car['الهيكل']) else car['اللوحة']
                        file_name = f"{ref}_{upload_type}.{ext}"
                        with open(f"vehicle_files/{file_name}", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success(f"✅ تم إضافة {upload_type} للملف بنجاح!")
            else:
                st.warning("لم يتم العثور على سيارة بهذه البيانات.")
