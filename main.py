import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. تأسيس قاعدة البيانات الدائمة ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"

def init_databases():
    if not os.path.exists(DB_REPORTS):
        pd.DataFrame(columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"]).to_csv(DB_REPORTS, index=False)
    if not os.path.exists(DB_USERS):
        initial_users = pd.DataFrame([["Jassim", "Jassim2026", "الإدارة", "الإدارة العامة,المتابعة اليومية,معرض الأسطول,أرشفة المستندات والأعطال,إدارة المستخدمين"]], 
                                     columns=["username", "password", "role", "perms"])
        initial_users.to_csv(DB_USERS, index=False)

init_databases()

# --- 2. إعدادات الصفحة والتنسيق الرسمي المطور ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #f8fafc; }
    
    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] { background-color: #002e63 !important; color: white; }
    
    /* تصميم البطاقات المربعة والمستطيلة */
    .dashboard-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 8px solid #002e63;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    /* الأزرار الرسمية العريضة */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #002e63;
        color: white;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    
    /* زر التحديث والرجوع (تنسيق خاص) */
    .action-btn button {
        background-color: #64748b !important;
        height: 3em !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الحالة واللوحات ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

FLEET_PLATES = [
    '1140', '1527', '1644', '1716', '1811', '1994', '2070', '2430', '2672', '2700', 
    '3010', '3228', '3462', '3515', '3516', '3547', '3597', '3599', '3606', '3634', 
    '3635', '3636', '3656', '3830', '3838', '3850', '4179', '4383', '4669', '5471', 
    '5645', '5786', '5826', '6123', '6264', '6265', '6388', '6472', '6785', '6787', 
    '6800', '6901', '6922', '6972', '6995', '7123', '7233', '7353', '7455', '7646', 
    '7668', '7906', '8116', '8465', '8484', '8674', '8795', '8796', '8797', '8827', 
    '8834', '8940', '9109'
]

# --- 4. واجهة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown('<div style="text-align: center; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        st.markdown('<h1 style="color: #002e63;">مؤسسة أسطول الخليج</h1>', unsafe_allow_html=True)
        st.write("تسجيل الدخول للنظام المركزي")
        
        users_df = pd.read_csv(DB_USERS)
        u_name = st.selectbox("المستخدم", users_df['username'].tolist())
        u_pass = st.text_input("كلمة المرور", type="password")
        
        if st.button("حفظ وإرسال بيانات الدخول"):
            user_row = users_df[(users_df['username'] == u_name) & (users_df['password'] == u_pass)]
            if not user_row.empty:
                st.session_state['auth'] = True
                st.session_state['username'] = u_name
                st.session_state['role'] = user_row.iloc[0]['role']
                st.session_state['perms'] = user_row.iloc[0]['perms'].split(",")
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. واجهة النظام الداخلية ---
else:
    with st.sidebar:
        st.markdown(f"<h2 style='color: white;'>أسطول الخليج</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #cbd5e1;'>المستخدم: {st.session_state['username']}</p>", unsafe_allow_html=True)
        st.write("---")
        
        menu_selection = st.radio("القائمة الرئيسية", ["الرئيسية"] + st.session_state['perms'])
        
        st.write("---")
        if st.button("تحديث النظام", key="sidebar_refresh"): st.rerun()
        if st.button("تسجيل الخروج"):
            st.session_state['auth'] = False
            st.rerun()

    # شريط الأزرار العلوي (تحديث ورجوع)
    tcol1, tcol2, tcol3 = st.columns([0.2, 0.2, 0.6])
    if menu_selection != "الرئيسية":
        with tcol1: 
            if st.button("رجوع", key="back_btn"): st.rerun() # سيعود للرئيسية تلقائياً بسبب الراديو
        with tcol2:
            if st.button("تحديث", key="refresh_page"): st.rerun()
    else:
        with tcol1:
            if st.button("تحديث", key="refresh_dash"): st.rerun()

    # --- الصفحات ---
    if menu_selection == "الرئيسية":
        st.markdown('<h1 style="color: #002e63; text-align: center;">الإدارة العامة</h1>', unsafe_allow_html=True)
        reports_count = len(pd.read_csv(DB_REPORTS))
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="dashboard-card"><h3>{len(FLEET_PLATES)}</h3>المركبات</div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="dashboard-card"><h3>{reports_count}</h3>التقارير المحفوظة</div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="dashboard-card"><h3>نشط</h3>حالة الاتصال</div>', unsafe_allow_html=True)

    elif menu_selection == "المتابعة اليومية":
        st.header("المتابعة اليومية")
        v = st.selectbox("رقم اللوحة", FLEET_PLATES)
        st.camera_input("تصوير الحالة")
        note = st.text_area("تقرير التشغيل اليومي")
        if st.button("حفظ وإرسال التقرير"):
            new_entry = pd.DataFrame([[datetime.now(), st.session_state['username'], v, "متابعة يومية", note]], columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"])
            new_entry.to_csv(DB_REPORTS, mode='a', header=False, index=False)
            st.success("تم الحفظ بنجاح")

    elif menu_selection == "معرض الأسطول":
        st.header("معرض الأسطول")
        search = st.text_input("بحث برقم اللوحة")
        display = [p for p in FLEET_PLATES if search in p] if search else FLEET_PLATES
        cols = st.columns(2)
        for i, p in enumerate(display):
            with cols[i % 2]:
                st.markdown(f'<div class="dashboard-card">لوحة رقم: {p}</div>', unsafe_allow_html=True)

    elif menu_selection == "أرشفة المستندات والأعطال":
        st.header("الأرشفة والأعطال")
        target = st.selectbox("اللوحة", FLEET_PLATES)
        t1, t2 = st.tabs(["أرشفة المستندات", "بلاغات الأعطال"])
        with t1:
            st.file_uploader("رفع المستند")
            if st.button("حفظ المستندات"): st.success("تم الحفظ")
        with t2:
            st.file_uploader("صور العطل")
            st.text_area("تفاصيل العطل")
            if st.button("إرسال بلاغ العطل"): st.success("تم الإرسال")

    elif menu_selection == "إدارة المستخدمين":
        st.header("إدارة المستخدمين")
        if st.session_state['role'] == "الإدارة":
            with st.expander("إضافة مستخدم جديد"):
                nu = st.text_input("الاسم")
                np = st.text_input("كلمة المرور")
                pms = st.multiselect("الصلاحيات", ["المتابعة اليومية", "معرض الأسطول", "أرشفة المستندات والأعطال"])
                if st.button("حفظ وتفعيل المستخدم"):
                    new_u = pd.DataFrame([[nu, np, "موظف", ",".join(pms)]], columns=["username", "password", "role", "perms"])
                    new_u.to_csv(DB_USERS, mode='a', header=False, index=False)
                    st.success(f"تم تفعيل حساب {nu}")
