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

st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

# --- 3. التنسيق الجمالي الحديث (Modern UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    
    /* تصميم المربعات الإحصائية */
    .metric-container {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-right: 10px solid #002e63;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* تصميم بطاقات السيارات في المعرض */
    .fleet-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin-bottom: 15px;
        text-align: center;
        font-weight: bold;
        color: #002e63;
    }
    
    /* تصميم الأزرار الاحترافي */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #002e63 0%, #004aad 100%);
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* توسيط واجهة الدخول */
    .login-wrapper {
        max-width: 450px;
        margin: auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = False

# --- 4. واجهة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.title("مؤسسة أسطول الخليج")
    st.write("نظام إدارة وأرشفة البيانات المركزية")
    
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
        st.write(f"المستخدم الحالي: {st.session_state['username']}")
        available_menu = [i for i in ["الإدارة العامة", "المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال", "إدارة المستخدمين"] if i in st.session_state['user_perms']]
        choice = st.radio("قائمة النظام:", available_menu)
        st.divider()
        if st.button("تسجيل الخروج من النظام"):
            st.session_state['auth'] = False
            st.rerun()

    if choice == "الإدارة العامة":
        st.header("الإدارة العامة")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-container"><h3>{len(FLEET_PLATES)}</h3>إجمالي المركبات</div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="metric-container"><h3>63</h3>لوحات مؤرشفة</div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="metric-container"><h3>101</h3>صفحة بيانات</div>', unsafe_allow_html=True)
        
        st.subheader("التحديثات الأخيرة")
        st.info("النظام يعمل بكافة صلاحياته الحالية.")

    elif choice == "المتابعة اليومية":
        st.header("المتابعة اليومية")
        v = st.selectbox("اختر رقم اللوحة للمتابعة", FLEET_PLATES)
        st.write(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.camera_input("التقاط صورة الحالة اليومية للمركبة")
        st.text_area("تقرير الفحص والتشغيل اليومي")
        if st.button("حفظ وإرسال التقرير اليومي"):
            st.success(f"تم حفظ وإرسال تقرير المركبة رقم {v} بنجاح.")

    elif choice == "معرض الأسطول":
        st.header("معرض الأسطول")
        search = st.text_input("البحث السريع برقم اللوحة")
        display = [p for p in FLEET_PLATES if search in p] if search else FLEET_PLATES
        
        cols = st.columns(2)
        for i, p in enumerate(display):
            with cols[i % 2]:
                st.markdown(f'<div class="fleet-card">رقم اللوحة: {p}</div>', unsafe_allow_html=True)

    elif choice == "أرشفة المستندات والأعطال":
        st.header("إدارة الأرشفة والأعطال")
        target = st.selectbox("اختر اللوحة المستهدفة", FLEET_PLATES)
        tab1, tab2 = st.tabs(["أرشفة المستندات", "توثيق أعطال المركبة"])
        
        with tab1:
            st.file_uploader("رفع صورة الاستمارة أو البطاقة الجمركية")
            if st.button("حفظ وإرسال المستندات"):
                st.success("تمت أرشفة المستند بنجاح.")
        
        with tab2:
            st.file_uploader("رفع صور أعطال المركبة")
            st.text_area("وصف العطل الحالي")
            if st.button("حفظ وإرسال بيانات العطل"):
                st.success("تم إرسال بلاغ العطل للقسم الفني.")

    elif choice == "إدارة المستخدمين":
        st.header("إدارة المستخدمين والصلاحيات")
        with st.expander("إضافة مستخدم جديد"):
            nu = st.text_input("اسم المستخدم الجديد")
            np = st.text_input("كلمة مرور المستخدم")
            pms = st.multiselect("تحديد صلاحيات الوصول", ["الإدارة العامة", "المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال"])
            if st.button("حفظ وإرسال بيانات المستخدم"):
                if nu and np:
                    st.session_state['user_db'][nu] = {"pass": np, "role": "موظف", "perms": pms}
                    st.success(f"تم تفعيل حساب {nu} في النظام.")
