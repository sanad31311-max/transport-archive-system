import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات النظام والقاعدة ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

# قائمة اللوحات الـ 63 المسحوبة من B6
FLEET_PLATES = [
    '1140', '1527', '1644', '1716', '1811', '1994', '2070', '2430', '2672', '2700', 
    '3010', '3228', '3462', '3515', '3516', '3547', '3597', '3599', '3606', '3634', 
    '3635', '3636', '3656', '3830', '3838', '3850', '4179', '4383', '4669', '5471', 
    '5645', '5786', '5826', '6123', '6264', '6265', '6388', '6472', '6785', '6787', 
    '6800', '6901', '6922', '6972', '6995', '7123', '7233', '7353', '7455', '7646', 
    '7668', '7906', '8116', '8465', '8484', '8674', '8795', '8796', '8797', '8827', 
    '8834', '8940', '9109'
]

# محاكي قاعدة البيانات (حفظ في ملف CSV)
DB_FILE = "fleet_database.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"]).to_csv(DB_FILE, index=False)

# --- 2. التنسيق الجمالي (CSS المطور) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #f8fafc; }
    
    .main-header {
        text-align: center;
        color: #002e63;
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    .section-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #002e63;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #002e63;
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام المستخدمين والصلاحيات ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "Jassim": {"pass": "Jassim2026", "role": "الإدارة", "perms": ["العمليات اليومية", "أرشيف الأسطول", "الإحصائيات العامة", "إعدادات النظام"]}
    }

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'current_page' not in st.session_state: st.session_state['current_page'] = "الرئيسية"

# --- 4. صفحة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-header"><h1>مؤسسة أسطول الخليج</h1><p>نظام الإدارة والأرشفة المركزي</p></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            u = st.selectbox("اختيار المستخدم", list(st.session_state['user_db'].keys()))
            p = st.text_input("كلمة المرور", type="password")
            if st.button("تسجيل الدخول"):
                if st.session_state['user_db'][u]['pass'] == p:
                    st.session_state['auth'] = True
                    st.session_state['username'] = u
                    st.session_state['user_perms'] = st.session_state['user_db'][u]['perms']
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")

# --- 5. واجهة النظام الرئيسية (القوائم المنسقة) ---
else:
    # شريط علوي للمعلومات
    col_u, col_l = st.columns([0.8, 0.2])
    col_u.write(f"المستخدم: {st.session_state['username']} | القسم: {st.session_state['user_db'][st.session_state['username']]['role']}")
    if col_l.button("خروج"):
        st.session_state['auth'] = False
        st.rerun()

    st.markdown('<div class="main-header"><h2>لوحة التحكم الرئيسية</h2></div>', unsafe_allow_html=True)

    # التقسيم الهرمي للقائمة
    if st.session_state['current_page'] == "الرئيسية":
        
        # قسم الإحصائيات (الإدارة العامة)
        if "الإحصائيات العامة" in st.session_state['user_perms']:
            with st.expander("إحصائيات الإدارة العامة", expanded=True):
                c1, c2, c3 = st.columns(3)
                c1.metric("إجمالي الأسطول", len(FLEET_PLATES))
                c2.metric("تقارير مسجلة", len(pd.read_csv(DB_FILE)))
                c3.metric("حالة النظام", "متصل")

        # قسم العمليات الميدانية
        if "العمليات اليومية" in st.session_state['user_perms']:
            st.markdown('<div class="section-card"><b>قسم العمليات اليومية</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("المتابعة اليومية للمركبات"):
                st.session_state['current_page'] = "المتابعة"
                st.rerun()
            if col2.button("تسجيل أعطال طارئة"):
                st.session_state['current_page'] = "الأعطال"
                st.rerun()

        # قسم الأرشفة والمعلومات
        if "أرشيف الأسطول" in st.session_state['user_perms']:
            st.markdown('<div class="section-card"><b>أرشيف الأسطول والمستندات</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            if col1.button("معرض صور الأسطول"):
                st.session_state['current_page'] = "المعرض"
                st.rerun()
            if col2.button("أرشفة الاستمارات والبطاقات"):
                st.session_state['current_page'] = "الأرشفة"
                st.rerun()

        # قسم الإعدادات
        if "إعدادات النظام" in st.session_state['user_perms']:
            st.markdown('<div class="section-card"><b>إعدادات النظام والسرية</b></div>', unsafe_allow_html=True)
            if st.button("إدارة المستخدمين والصلاحيات"):
                st.session_state['current_page'] = "المستخدمين"
                st.rerun()

    # --- صفحات الأقسام التفصيلية ---
    elif st.session_state['current_page'] == "المتابعة":
        if st.button("الرجوع للقائمة الرئيسية"): st.session_state['current_page'] = "الرئيسية"; st.rerun()
        st.header("تقرير المتابعة اليومية")
        v = st.selectbox("رقم اللوحة", FLEET_PLATES)
        st.camera_input("تصوير حالة المركبة")
        note = st.text_area("تقرير التشغيل اليومي")
        if st.button("حفظ وإرسال البيانات"):
            new_data = pd.DataFrame([[datetime.now(), st.session_state['username'], v, "متابعة يومية", note]], columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"])
            new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
            st.success("تم الحفظ في قاعدة البيانات")

    elif st.session_state['current_page'] == "المعرض":
        if st.button("الرجوع للقائمة الرئيسية"): st.session_state['current_page'] = "الرئيسية"; st.rerun()
        st.header("معرض أسطول الخليج")
        q = st.text_input("بحث برقم اللوحة")
        display = [p for p in FLEET_PLATES if q in p] if q else FLEET_PLATES
        cols = st.columns(3)
        for i, p in enumerate(display):
            with cols[i % 3]:
                st.markdown(f'<div style="background: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; text-align: center;">لوحة: {p}</div>', unsafe_allow_html=True)

    elif st.session_state['current_page'] == "المستخدمين":
        if st.button("الرجوع للقائمة الرئيسية"): st.session_state['current_page'] = "الرئيسية"; st.rerun()
        st.header("إدارة مستخدمي النظام")
        with st.expander("إضافة مستخدم جديد"):
            nu = st.text_input("اسم المستخدم")
            np = st.text_input("كلمة المرور")
            pms = st.multiselect("الصلاحيات", ["العمليات اليومية", "أرشيف الأسطول", "الإحصائيات العامة", "إعدادات النظام"])
            if st.button("حفظ وإرسال بيانات المستخدم"):
                st.session_state['user_db'][nu] = {"pass": np, "role": "موظف", "perms": pms}
                st.success("تم التفعيل")
