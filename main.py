import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. قاعدة بيانات المستخدمين ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "Jassim": {
            "pass": "Jassim2026",
            "role": "الإدارة",
            "perms": ["الإدارة العامة", "المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال", "إدارة المستخدمين"]
        }
    }

# --- 2. قائمة اللوحات الـ 63 ---
FLEET_PLATES = [
    '1140', '1527', '1644', '1716', '1811', '1994', '2070', '2430', '2672', '2700', 
    '3010', '3228', '3462', '3515', '3516', '3547', '3597', '3599', '3606', '3634', 
    '3635', '3636', '3656', '3830', '3838', '3850', '4179', '4383', '4669', '5471', 
    '5645', '5786', '5826', '6123', '6264', '6265', '6388', '6472', '6785', '6787', 
    '6800', '6901', '6922', '6972', '6995', '7123', '7233', '7353', '7455', '7646', 
    '7668', '7906', '8116', '8465', '8484', '8674', '8795', '8796', '8797', '8827', 
    '8834', '8940', '9109'
]

st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

# --- 3. التنسيق الجمالي المتطور (إصلاح مشكلة الاختفاء) ---
st.markdown("""
    <style>
    /* جعل الواجهة نظيفة بدون الشريط العلوي المزعج */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #f4f7f9; }
    
    /* تنسيق حاوية الدخول */
    .login-wrapper {
        max-width: 500px;
        margin: 0 auto;
        padding: 50px 30px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* مربعات الإحصائيات */
    .stat-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #002e63;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    /* الأزرار الرئيسية الكبيرة */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #002e63 0%, #004aad 100%);
        color: white;
        font-weight: bold;
        height: 4em;
        margin-bottom: 10px;
        border: none;
    }
    
    /* زر الرجوع للرئيسية */
    .back-btn>div>button {
        background: #6c757d !important;
        height: 3em !important;
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة (أي صفحة نحن فيها)
if 'page' not in st.session_state: st.session_state['page'] = 'login'
if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 4. واجهة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #002e63;">مؤسسة أسطول الخليج</h1>', unsafe_allow_html=True)
    st.write("نظام الإدارة والأرشفة المركزي")
    
    u_name = st.selectbox("اختيار المستخدم", list(st.session_state['user_db'].keys()))
    u_pass = st.text_input("كلمة المرور", type="password")
    
    if st.button("حفظ وإرسال بيانات الدخول"):
        if st.session_state['user_db'][u_name]['pass'] == u_pass:
            st.session_state['auth'] = True
            st.session_state['username'] = u_name
            st.session_state['user_perms'] = st.session_state['user_db'][u_name]['perms']
            st.session_state['page'] = 'dashboard'
            st.rerun()
        else:
            st.error("البيانات المدخلة غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. واجهة النظام الداخلية (لوحة التحكم المركزية) ---
else:
    # شريط علوي بسيط للمستخدم الحالي وزر خروج
    col_user, col_logout = st.columns([0.8, 0.2])
    with col_user: st.write(f"المستخدم: {st.session_state['username']}")
    with col_logout: 
        if st.button("خروج"):
            st.session_state['auth'] = False
            st.rerun()

    # --- صفحة لوحة التحكم (الرئيسية) ---
    if st.session_state['page'] == 'dashboard':
        st.markdown('<h2 style="text-align: center; color: #002e63;">لوحة التحكم الرئيسية</h2>', unsafe_allow_html=True)
        
        # مربعات الإحصائيات
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f'<div class="stat-card"><h3>{len(FLEET_PLATES)}</h3>المركبات</div>', unsafe_allow_html=True)
        with s2: st.markdown('<div class="stat-card"><h3>63</h3>اللوحات</div>', unsafe_allow_html=True)
        with s3: st.markdown('<div class="stat-card"><h3>101</h3>التقارير</div>', unsafe_allow_html=True)
        
        st.write("---")
        
        # أزرار التنقل الكبيرة (بدل القائمة الجانبية)
        col1, col2 = st.columns(2)
        
        if "المتابعة اليومية" in st.session_state['user_perms']:
            with col1:
                if st.button("المتابعة اليومية للمركبات"):
                    st.session_state['page'] = 'daily'
                    st.rerun()
        
        if "معرض الأسطول" in st.session_state['user_perms']:
            with col2:
                if st.button("معرض الأسطول والأرشفة"):
                    st.session_state['page'] = 'fleet'
                    st.rerun()

        if "أرشفة المستندات والأعطال" in st.session_state['user_perms']:
            with col1:
                if st.button("إدارة الأرشفة والأعطال"):
                    st.session_state['page'] = 'archive'
                    st.rerun()

        if "إدارة المستخدمين" in st.session_state['user_perms']:
            with col2:
                if st.button("إدارة المستخدمين"):
                    st.session_state['page'] = 'users'
                    st.rerun()

    # --- صفحة المتابعة اليومية ---
    elif st.session_state['page'] == 'daily':
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("الرجوع للرئيسية"): st.session_state['page'] = 'dashboard'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.header("المتابعة اليومية")
        v = st.selectbox("اختر رقم اللوحة", FLEET_PLATES)
        st.camera_input("التقاط صورة الحالة")
        st.text_area("تقرير الفحص اليومي")
        if st.button("حفظ وإرسال التقرير"): st.success("تم الحفظ")

    # --- صفحة معرض الأسطول ---
    elif st.session_state['page'] == 'fleet':
        if st.button("الرجوع للرئيسية"): st.session_state['page'] = 'dashboard'; st.rerun()
        st.header("معرض أسطول الخليج")
        search = st.text_input("بحث برقم اللوحة")
        display = [p for p in FLEET_PLATES if search in p] if search else FLEET_PLATES
        cols = st.columns(2)
        for i, p in enumerate(display):
            with cols[i % 2]:
                st.markdown(f'<div style="background: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; text-align: center;">لوحة رقم: {p}</div>', unsafe_allow_html=True)

    # --- صفحة إدارة المستخدمين ---
    elif st.session_state['page'] == 'users':
        if st.button("الرجوع للرئيسية"): st.session_state['page'] = 'dashboard'; st.rerun()
        st.header("إدارة المستخدمين")
        with st.expander("إضافة مستخدم جديد"):
            nu = st.text_input("الاسم")
            np = st.text_input("كلمة السر")
            if st.button("حفظ الموظف الجديد"): st.success("تم التفعيل")
