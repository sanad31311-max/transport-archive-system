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
            ["User1", "1122", "موظف", "الرئيسية,المتابعة اليومية"],
            ["User2", "3344", "موظف", "الرئيسية,معرض الأسطول"],
            ["User3", "5566", "موظف", "الرئيسية,أرشفة المستندات والأعطال"]
        ], columns=["username", "password", "role", "perms"])
        initial_users.to_csv(DB_USERS, index=False)

init_databases()

# --- 2. إعدادات الصفحة والتنسيق الفني (CSS) ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    /* ضبط الخط والاتجاه العام */
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* إخفاء الهيدر وفوتر ستريمليت */
    [data-testid="stHeader"], footer {visibility: hidden;}
    .block-container {padding: 1rem 1rem 7rem 1rem !important;}

    /* البطاقات الموحدة */
    .card-fixed {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid #002e63;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        text-align: center;
        width: 100%;
    }
    
    /* الأزرار الرسمية العريضة */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        background-color: #002e63 !important;
        color: white !important;
        font-weight: bold !important;
        height: 4em !important;
        border: none !important;
        margin-bottom: 10px !important;
    }
    
    /* شريط التنقل السفلي */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #002e63;
        padding: 15px 0;
        z-index: 1000;
        border-top: 3px solid #64748b;
        display: flex;
        justify-content: space-around;
    }
    
    /* تنسيق القوائم المنسدلة والمدخلات */
    .stSelectbox, .stTextInput {
        margin-bottom: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'page' not in st.session_state: st.session_state['page'] = "الرئيسية"

FLEET_PLATES = ['1140', '1527', '1644', '1716', '1811', '1994', '2070', '2430', '2672', '2700', '3010', '3228', '3462', '3515', '3516', '3547', '3597', '3599', '3606', '3634', '3635', '3636', '3656', '3830', '3838', '3850', '4179', '4383', '4669', '5471', '5645', '5786', '5826', '6123', '6264', '6265', '6388', '6472', '6785', '6787', '6800', '6901', '6922', '6972', '6995', '7123', '7233', '7353', '7455', '7646', '7668', '7906', '8116', '8465', '8484', '8674', '8795', '8796', '8797', '8827', '8834', '8940', '9109']

# --- 4. واجهة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: #002e63;">مؤسسة أسطول الخليج</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b;">تسجيل الدخول للنظام المركزي</p>', unsafe_allow_html=True)
    
    with st.container():
        col_l, col_m, col_r = st.columns([0.1, 0.8, 0.1])
        with col_m:
            st.markdown('<div class="card-fixed">', unsafe_allow_html=True)
            u_df = pd.read_csv(DB_USERS)
            user_select = st.selectbox("اسم المستخدم", u_df['username'].tolist())
            pass_input = st.text_input("كلمة المرور", type="password")
            if st.button("حفظ وإرسال بيانات الدخول"):
                match = u_df[(u_df['username'] == user_select) & (u_df['password'] == pass_input)]
                if not match.empty:
                    st.session_state.update({'auth': True, 'username': user_select, 'role': match.iloc[0]['role'], 'perms': match.iloc[0]['perms'].split(",")})
                    st.rerun()
                else: st.error("عذراً، البيانات غير صحيحة")
            st.markdown('</div>', unsafe_allow_html=True)

# --- 5. واجهة النظام الداخلية ---
else:
    # شريط التحكم العلوي
    t_col1, t_col2 = st.columns([0.8, 0.2])
    with t_col2:
        if st.button("تحديث"): st.rerun()
    with t_col1:
        if st.session_state['page'] != "الرئيسية":
            if st.button("رجوع"):
                st.session_state['page'] = "الرئيسية"
                st.rerun()

    pg = st.session_state['page']
    
    if pg == "الرئيسية":
        st.markdown(f'<h2 style="text-align: center; color: #002e63;">مرحباً {st.session_state["username"]}</h2>', unsafe_allow_html=True)
        r_df = pd.read_csv(DB_REPORTS)
        
        st.markdown(f'<div class="card-fixed"><h2>63</h2>مركبة مسجلة</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-fixed"><h2>{len(r_df)}</h2>تقرير محفوظ</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-fixed">حالة النظام: متصل</div>', unsafe_allow_html=True)

    elif pg == "المتابعة اليومية":
        st.markdown('<h2 style="text-align: center;">المتابعة اليومية</h2>', unsafe_allow_html=True)
        plate = st.selectbox("اختر رقم اللوحة", FLEET_PLATES)
        st.camera_input("تصوير الحالة الميدانية")
        details = st.text_area("تفاصيل التقرير")
        if st.button("حفظ وإرسال التقرير"):
            new_row = pd.DataFrame([[datetime.now(), st.session_state['username'], plate, "يومي", details]], columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"])
            new_row.to_csv(DB_REPORTS, mode='a', header=False, index=False)
            st.success("تم الحفظ بنجاح")

    elif pg == "معرض الأسطول":
        st.markdown('<h2 style="text-align: center;">معرض الأسطول</h2>', unsafe_allow_html=True)
        query = st.text_input("بحث برقم اللوحة")
        results = [p for p in FLEET_PLATES if query in p]
        for p in results[:15]:
            st.markdown(f'<div class="card-fixed">لوحة رقم: {p}</div>', unsafe_allow_html=True)

    elif pg == "أرشفة المستندات والأعطال":
        st.markdown('<h2 style="text-align: center;">الأرشفة والأعطال</h2>', unsafe_allow_html=True)
        st.selectbox("رقم اللوحة", FLEET_PLATES)
        st.file_uploader("رفع المستند")
        if st.button("تأكيد الأرشفة"): st.success("تم الحفظ")

    elif pg == "إدارة المستخدمين":
        if st.session_state['role'] == "الإدارة":
            st.markdown('<h2 style="text-align: center;">إدارة النظام</h2>', unsafe_allow_html=True)
            st.table(pd.read_csv(DB_USERS)[['username', 'role']])
        else: st.warning("صلاحية الوصول للإدارة فقط")

    # --- 6. شريط التنقل السفلي المطور ---
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    p_list = st.session_state['perms']
    nav_cols = st.columns(len(p_list))
    for i, p_name in enumerate(p_list):
        if nav_cols[i].button(p_name, key=f"nav_{p_name}"):
            st.session_state['page'] = p_name
            st.rerun()
