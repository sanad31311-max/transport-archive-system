import streamlit as st
import pandas as pd
import os

# 1. نظام المستخدمين والصلاحيات (أبو محمد هو الأدمن)
USERS = {
    "abu_mohammed": "123456",  # المستخدم الأساسي بصلاحيات كاملة
    "employee1": "emp123"      # موظف بصلاحيات تصفح فقط
}

# إعدادات واجهة التطبيق الرسمية لتناسب الجوال
st.set_page_config(page_title="نظام سند للأرشفة", layout="wide", initial_sidebar_state="collapsed")

# تنسيق المظهر العام ليناسب التصفح السريع (رسمي وبدون إيموجيات)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1a1a1a; color: white; height: 3.5em; font-weight: bold; }
    .car-card { padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; background-color: white; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1f1f1; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحقق من الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("نظام أرشفة مؤسسة النقل")
    st.subheader("تسجيل الدخول")
    u_input = st.text_input("اسم المستخدم")
    p_input = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if u_input in USERS and USERS[u_input] == p_input:
            st.session_state['authenticated'] = True
            st.session_state['username'] = u_input
            st.rerun()
        else:
            st.error("البيانات المدخلة غير صحيحة")
else:
    # القائمة الجانبية (3 خطوط)
    with st.sidebar:
        st.title("القائمة الرئيسية")
        menu = ["الصفحة الرئيسية", "معرض الأسطول (تصفح)", "إدارة ملفات المركبات", "تسجيل مركبة جديدة", "الإعدادات"]
        choice = st.radio("انتقل إلى:", menu)
        st.divider()
        if st.button("تسجيل الخروج"):
            st.session_state['authenticated'] = False
            st.rerun()

    # ركن الحساب أعلى اليسار
    col_acc1, col_acc2 = st.columns([0.85, 0.15])
    with col_acc2:
        st.write(f"الحساب: {st.session_state['username']}")

    # --- الأقسام ---
    if choice == "الصفحة الرئيسية":
        st.header("لوحة التحكم")
        st.write("مرحباً بك في النظام الرسمي لإدارة وأرشفة أسطول مؤسسة النقل.")
        st.info("استخدم القائمة الجانبية للتنقل بين المعرض وإدارة الملفات.")

    elif choice == "معرض الأسطول (تصفح)":
        st.header("استعراض الأسطول")
        st.write("قائمة السيارات المسجلة في النظام:")
        # مثال لعرض السيارات (سيتم ربطها بقاعدة البيانات لاحقاً)
        for i in range(1, 4): 
            with st.container():
                st.markdown(f'<div class="car-card"><b>مركبة رقم {i}</b><br>رقم اللوحة: 1234 س ن د | رقم الهيكل: VIN00000{i}</div>', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("عرض الاستمارة", key=f"v1_{i}"): st.info("جاري عرض المستندات الرسمية...")
                if c2.button("عرض صور السيارة", key=f"v2_{i}"): st.info("جاري فتح ألبوم الصور...")
                if c3.button("حالة عضلات السيارة", key=f"v3_{i}"): st.info("عرض تقرير الفحص الميكانيكي...")
                if c4.button("سجل الفواتير", key=f"v4_{i}"): st.info("عرض أرشيف الفواتير والتقارير...")

    elif choice == "إدارة ملفات المركبات":
        if st.session_state['username'] == "abu_mohammed":
            st.header("إدارة وتحديث ملفات المركبات")
            search_id = st.text_input("ابحث برقم الهيكل أو اللوحة للتعديل أو الإضافة")
            if search_id:
                st.subheader("تعديل ملف السيارة: " + search_id)
                tab1, tab2, tab3, tab4 = st.tabs(["البحث عن الاستمارة", "صور السياره", "عضلات السياره", "فواتير السياره"])
                with tab1:
                    st.file_uploader("رفع استمارة أو بطاقة جمركية جديدة", type=['pdf', 'jpg', 'png'])
                with tab2:
                    st.camera_input("التقاط صورة مباشرة للسيارة")
                with tab3:
                    st.write("توثيق الحالة الميكانيكية وعضلات السيارة")
                    st.file_uploader("رفع صور الفحص الميكانيكي", key="mech_up")
                with tab4:
                    st.file_uploader("رفع فواتير الصيانة والتقارير المالية", key="inv_up")
        else:
            st.warning("عذراً، صلاحية التعديل والإضافة متاحة للأدمن فقط.")

    elif choice == "تسجيل مركبة جديدة":
        st.header("إضافة مركبة للأسطول")
        with st.form("new_vehicle_form"):
            f1, f2 = st.columns(2)
            f1.text_input("رقم الهيكل")
            f1.text_input("رقم اللوحة")
            f2.text_input("رقم البطاقة الجمركية")
            f2.text_input("نوع السيارة")
            if st.form_submit_button("حفظ البيانات في الأرشيف"):
                st.success("تم تسجيل بيانات المركبة بنجاح")

    elif choice == "الإعدادات":
        st.header("إعدادات النظام والأمان")
        if st.session_state['username'] == "abu_mohammed":
            st.write("إدارة صلاحيات المستخدمين والنسخ الاحتياطي")
            st.button("تصدير قاعدة البيانات بالكامل (Excel)")
        else:
            st.write("يمكن للأدمن فقط الوصول لهذه الإعدادات والتحكم في النظام.")
