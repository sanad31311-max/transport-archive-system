import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. قاعدة بيانات المستخدمين والصلاحيات ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "Jassim": {
            "pass": "Jassim2026",
            "role": "الإدارة",
            "perms": ["الإدارة العامة", "المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال", "إدارة المستخدمين"]
        }
    }

# --- 2. قائمة اللوحات الـ 63 المسحوبة من الخانة B6 ---
FLEET_PLATES = [
    '1140', '1527', '1644', '1716', '1811', '1994', '2070', '2430', '2672', '2700', 
    '3010', '3228', '3462', '3515', '3516', '3547', '3597', '3599', '3606', '3634', 
    '3635', '3636', '3656', '3830', '3838', '3850', '4179', '4383', '4669', '5471', 
    '5645', '5786', '5826', '6123', '6264', '6265', '6388', '6472', '6785', '6787', 
    '6800', '6901', '6922', '6972', '6995', '7123', '7233', '7353', '7455', '7646', 
    '7668', '7906', '8116', '8465', '8484', '8674', '8795', '8796', '8797', '8827', 
    '8834', '8940', '9109'
]

# إعدادات الصفحة وإخفاء العناصر الافتراضية المزعجة
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

# --- 3. التنسيق الجمالي الاحترافي (إزالة المستطيل العلوي وتوسيط النص) ---
st.markdown("""
    <style>
    /* إخفاء الهيدر الافتراضي لستريمليت لإزالة المستطيل الأبيض العلوي */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    .stApp { background-color: #f4f7f9; }
    
    /* تنسيق حاوية الدخول وتوسيطها */
    .login-wrapper {
        max-width: 500px;
        margin: 0 auto;
        padding: 50px 30px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* توسيط العناوين */
    .centered-title {
        text-align: center;
        color: #002e63;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* المربعات الإحصائية */
    .metric-container {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-right: 10px solid #002e63;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* الأزرار الرسمية */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #002e63 0%, #004aad 100%);
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 4. واجهة تسجيل الدخول المحدثة ---
if not st.session_state['auth']:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True) # فراغ علوي بسيط بدلاً من المستطيل
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<h1 class="centered-title">مؤسسة أسطول الخليج</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">نظام الإدارة والأرشفة المركزي</p>', unsafe_allow_html=True)
    
    users = list(st.session_state['user_db'].keys())
    u_name = st.selectbox("اختيار المستخدم", users)
    u_pass = st.text_input("كلمة المرور", type="password")
    
    if st.button("حفظ وإرسال بيانات الدخول"):
        if st.session_state['user_db'][u_name]['pass'] == u_pass:
            st.session_state['auth'] = True
            st.session_state['username'] = u_name
            st.session_state['user_perms'] = st.session_state['user_db'][u_name]['perms']
            st.rerun()
        else:
            st.error("البيانات المدخلة غير صحيحة")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. واجهة النظام الداخلية ---
else:
    with st.sidebar:
        st.markdown(f"### المستخدم: {st.session_state['username']}")
        available_menu = [i for i in ["الإدارة العامة", "المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال", "إدارة المستخدمين"] if i in st.session_state['user_perms']]
        choice = st.radio("القائمة:", available_menu)
        st.divider()
        if st.button("تسجيل الخروج من النظام"):
            st.session_state['auth'] = False
            st.rerun()

    if choice == "الإدارة العامة":
        st.markdown('<h1 class="centered-title">الإدارة العامة</h1>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-container"><h3>{len(FLEET_PLATES)}</h3>إجمالي المركبات</div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="metric-container"><h3>63</h3>لوحات مؤرشفة</div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="metric-container"><h3>101</h3>صفحة بيانات</div>', unsafe_allow_html=True)
        st.info("النظام يعمل بكافة صلاحياته الحالية.")

    elif choice == "المتابعة اليومية":
        st.header("المتابعة اليومية")
        v = st.selectbox("اختر رقم اللوحة للمتابعة", FLEET_PLATES)
        st.write(f"تاريخ العملية: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.camera_input("التقاط صورة الحالة اليومية")
        st.text_area("تقرير الفحص اليومي")
        if st.button("حفظ وإرسال التقرير اليومي"):
            st.success(f"تم حفظ وإرسال التقرير بنجاح.")

    elif choice == "معرض الأسطول":
        st.header("معرض الأسطول")
        search = st.text_input("البحث برقم اللوحة")
        display = [p for p in FLEET_PLATES if search in p] if search else FLEET_PLATES
        cols = st.columns(2)
        for i, p in enumerate(display):
            with cols[i % 2]:
                st.markdown(f'<div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; text-align: center; font-weight: bold;">لوحة رقم: {p}</div>', unsafe_allow_html=True)

    elif choice == "أرشفة المستندات والأعطال":
        st.header("إدارة الأرشفة والأعطال")
        target = st.selectbox("اختر اللوحة", FLEET_PLATES)
        t1, t2 = st.tabs(["أرشفة المستندات", "أعطال المركبة"])
        with t1:
            st.file_uploader("رفع صورة المستند")
            if st.button("حفظ وإرسال المستندات"): st.success("تم الحفظ")
        with t2:
            st.file_uploader("صور أعطال المركبة")
            st.text_area("وصف العطل")
            if st.button("حفظ وإرسال بيانات العطل"): st.success("تم الإرسال")

    elif choice == "إدارة المستخدمين":
        st.header("إدارة المستخدمين")
        with st.expander("إضافة مستخدم جديد"):
            nu = st.text_input("اسم المستخدم")
            np = st.text_input("كلمة المرور")
            pms = st.multiselect("الصلاحيات", ["الإدارة العامة", "المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال"])
            if st.button("حفظ وإرسال بيانات المستخدم"):
                st.session_state['user_db'][nu] = {"pass": np, "role": "موظف", "perms": pms}
                st.success(f"تم تفعيل حساب {nu}")
