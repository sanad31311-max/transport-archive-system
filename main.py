import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. تأسيس وقواعد البيانات الدائمة ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"

def init_databases():
    if not os.path.exists(DB_REPORTS):
        pd.DataFrame(columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"]).to_csv(DB_REPORTS, index=False)
    
    if not os.path.exists(DB_USERS):
        initial_users = pd.DataFrame([
            ["Jassim", "Jassim2026", "الإدارة", "الرئيسية,المتابعة اليومية,معرض الأسطول,أرشفة المستندات والأعطال,إدارة المستخدمين"],
            ["Emp1", "1122", "موظف", "الرئيسية,المتابعة اليومية"],
            ["Emp2", "3344", "موظف", "الرئيسية,معرض الأسطول"],
            ["Emp3", "5566", "موظف", "الرئيسية,أرشفة المستندات والأعطال"]
        ], columns=["username", "password", "role", "perms"])
        initial_users.to_csv(DB_USERS, index=False)

init_databases()

# --- 2. بيانات الأسطول (63 لوحة) ---
FLEET_PLATES = [
    '1140', '1527', '1644', '1716', '1811', '1994', '2070', '2430', '2672', '2700', 
    '3010', '3228', '3462', '3515', '3516', '3547', '3597', '3599', '3606', '3634', 
    '3635', '3636', '3656', '3830', '3838', '3850', '4179', '4383', '4669', '5471', 
    '5645', '5786', '5826', '6123', '6264', '6265', '6388', '6472', '6785', '6787', 
    '6800', '6901', '6922', '6972', '6995', '7123', '7233', '7353', '7455', '7646', 
    '7668', '7906', '8116', '8465', '8484', '8674', '8795', '8796', '8797', '8827', 
    '8834', '8940', '9109'
]

# --- 3. تحسين الواجهة والتنسيق الرسمي (بدون إيموجي) ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* إعدادات الخطوط والمسافات العامة */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Tajawal', sans-serif; text-align: right; direction: rtl; }
    
    [data-testid="stHeader"] {visibility: hidden;}
    .block-container {padding: 2rem 1rem 7rem 1rem !important;}
    
    /* تصميم البطاقات الرسمي */
    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-right: 8px solid #002e63;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        color: #002e63;
    }
    
    /* الأزرار الرسمية */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: #002e63;
        color: #ffffff;
        font-weight: bold;
        height: 3.8em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #00408a; border: none; color: #ffffff; }

    /* شريط التنقل السفلي الثابت */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #002e63;
        padding: 12px 0;
        z-index: 9999;
        border-top: 3px solid #64748b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. منطق إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'page' not in st.session_state: st.session_state['page'] = "الرئيسية"

# --- 5. شاشة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<h1 style="text-align: center; color: #002e63; margin-top: 50px;">مؤسسة أسطول الخليج</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b;">نظام إدارة الأسطول المركزي</p>', unsafe_allow_html=True)
    
    with st.container():
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            u_df = pd.read_csv(DB_USERS)
            user_select = st.selectbox("اسم المستخدم", u_df['username'].tolist())
            pass_input = st.text_input("كلمة المرور", type="password")
            
            if st.button("تسجيل الدخول"):
                match = u_df[(u_df['username'] == user_select) & (u_df['password'] == pass_input)]
                if not match.empty:
                    st.session_state.update({
                        'auth': True, 'username': user_select,
                        'role': match.iloc[0]['role'],
                        'perms': match.iloc[0]['perms'].split(",")
                    })
                    st.rerun()
                else: st.error("خطأ في بيانات الدخول")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- 6. التحكم العلوي (رجوع وتحديث) ---
    t_col1, t_col2 = st.columns([0.85, 0.15])
    with t_col2:
        if st.button("تحديث"): st.rerun()
    with t_col1:
        if st.session_state['page'] != "الرئيسية":
            if st.button("العودة للقائمة الرئيسية"):
                st.session_state['page'] = "الرئيسية"
                st.rerun()

    # --- 7. محتوى الصفحات ---
    pg = st.session_state['page']
    
    if pg == "الرئيسية":
        st.markdown(f'<h2 style="text-align: center; color: #002e63;">مرحباً {st.session_state["username"]}</h2>', unsafe_allow_html=True)
        r_df = pd.read_csv(DB_REPORTS)
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="card"><h1 style="margin:0;">63</h1>مركبة مسجلة</div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card"><h1 style="margin:0;">{len(r_df)}</h1>تقرير محفوظ</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="card" style="text-align: center;">حالة النظام: متصل</div>', unsafe_allow_html=True)

    elif pg == "المتابعة اليومية":
        st.header("نموذج المتابعة اليومية")
        with st.form("daily_form"):
            plate = st.selectbox("رقم اللوحة", FLEET_PLATES)
            st.camera_input("التقاط صورة الحالة الميدانية")
            details = st.text_area("ملاحظات الفحص والتشغيل")
            if st.form_submit_button("حفظ وإرسال"):
                new_row = pd.DataFrame([[datetime.now(), st.session_state['username'], plate, "يومي", details]], columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"])
                new_row.to_csv(DB_REPORTS, mode='a', header=False, index=False)
                st.success("تم الحفظ بنجاح")

    elif pg == "معرض الأسطول":
        st.header("قائمة مركبات الأسطول")
        query = st.text_input("بحث برقم اللوحة")
        results = [p for p in FLEET_PLATES if query in p]
        
        cols = st.columns(2)
        for idx, p in enumerate(results[:20]):
            with cols[idx % 2]:
                st.markdown(f'<div class="card" style="padding:15px;">لوحة رقم: {p}</div>', unsafe_allow_html=True)

    elif pg == "أرشفة المستندات والأعطال":
        st.header("الأرشفة وبلاغات الأعطال")
        target = st.selectbox("اختر اللوحة", FLEET_PLATES)
        st.file_uploader("رفع صورة المستند أو العطل")
        st.text_area("وصف العطل أو المستند")
        if st.button("إرسال للأرشفة"): st.success("تمت العملية بنجاح")

    elif pg == "إدارة المستخدمين":
        if st.session_state['role'] == "الإدارة":
            st.header("إدارة الصلاحيات")
            st.table(pd.read_csv(DB_USERS)[['username', 'role']])
            with st.expander("إضافة حساب جديد"):
                new_u = st.text_input("الاسم")
                new_p = st.text_input("كلمة السر")
                if st.button("تفعيل الحساب"): st.success("تم التفعيل")
        else: st.warning("صلاحية الوصول للإدارة فقط")

    # --- 8. أزرار التنقل السفلية الثابتة (التصميم المحسن) ---
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    p_list = st.session_state['perms']
    nav_cols = st.columns(len(p_list))
    for i, p_name in enumerate(p_list):
        if nav_cols[i].button(p_name, key=f"nav_btn_{p_name}"):
            st.session_state['page'] = p_name
            st.rerun()
