import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات النظام وقواعد البيانات ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"

def init_databases():
    if not os.path.exists(DB_REPORTS):
        pd.DataFrame(columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"]).to_csv(DB_REPORTS, index=False)
    if not os.path.exists(DB_USERS):
        initial_users = pd.DataFrame([
            ["Jassim", "Jassim2026", "الإدارة", "العمليات الميدانية,الأرشفة والوثائق,إدارة النظام"]
        ], columns=["username", "password", "role", "perms"])
        initial_users.to_csv(DB_USERS, index=False)

init_databases()

# --- 2. التنسيق الرسمي المطور (CSS) لنسخة التدشين ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] {visibility: hidden !important;}
    .block-container {padding: 1rem 1rem 5rem 1rem !important;}

    /* ضبط حجم الأزرار ليكون رسمياً وليس ضخماً */
    div.stButton > button {
        width: 100% !important;
        height: 3.5em !important; /* حجم قياسي مريح */
        border-radius: 10px !important;
        background-color: #002e63 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    /* زر الرجوع والتحديث (لون مميز وموقع ثابت) */
    .nav-btn button { background-color: #64748b !important; height: 3em !important; }

    /* البطاقات التعريفية (Dashboard Cards) */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #002e63;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة التنقل (Navigation) ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"
if 'sub_view' not in st.session_state: st.session_state['sub_view'] = None

FLEET_PLATES = [str(p) for p in [1140, 1527, 1644, 1716, 1811, 1994, 2070, 2430, 2672, 2700, 3010, 3228, 3462, 3515, 3516, 3547, 3597, 3599, 3606, 3634, 3635, 3636, 3656, 3830, 3838, 3850, 4179, 4383, 4669, 5471, 5645, 5786, 5826, 6123, 6264, 6265, 6388, 6472, 6785, 6787, 6800, 6901, 6922, 6972, 6995, 7123, 7233, 7353, 7455, 7646, 7668, 7906, 8116, 8465, 8484, 8674, 8795, 8796, 8797, 8827, 8834, 8940, 9109]]

# --- 4. شاشة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<h2 style="color: #002e63; text-align: center; margin-top: 50px;">مؤسسة أسطول الخليج</h2>', unsafe_allow_html=True)
    with st.container():
        u_list = pd.read_csv(DB_USERS)['username'].tolist()
        user_in = st.selectbox("المستخدم", u_list)
        pass_in = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول للنظام المركزي"):
            users = pd.read_csv(DB_USERS)
            valid = users[(users['username'] == user_in) & (users['password'] == pass_in)]
            if not valid.empty:
                st.session_state.update({'auth': True, 'username': user_in, 'role': valid.iloc[0]['role'], 'perms': valid.iloc[0]['perms'].split(",")})
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")

# --- 5. الواجهة الداخلية للنظام ---
else:
    # شريط التحكم العلوي (ثابت)
    c_up1, c_up2 = st.columns([0.8, 0.2])
    with c_up2:
        if st.button("تحديث"): st.rerun()
    with c_up1:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("رجوع"):
                if st.session_state['sub_view']: st.session_state['sub_view'] = None
                else: st.session_state['view'] = "الرئيسية"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # أ: الصفحة الرئيسية (البيانات السريعة)
    if st.session_state['view'] == "الرئيسية":
        st.markdown(f'<h3 style="color: #002e63; text-align: center;">مرحبا، {st.session_state["username"]}</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.markdown('<div class="metric-card"><h4>63</h4>مركبة مسجلة</div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h4>{len(pd.read_csv(DB_REPORTS))}</h4>تقارير محفوظة</div>', unsafe_allow_html=True)
        
        st.write("---")
        if st.button("قائمة الخدمات المركزية"):
            st.session_state['view'] = "التصنيفات"
            st.rerun()
        
        if st.button("تسجيل الخروج"):
            st.session_state['auth'] = False
            st.rerun()

    # ب: صفحة التصنيفات الأساسية
    elif st.session_state['view'] == "التصنيفات":
        st.markdown('<h3 style="text-align: center;">التصنيفات الأساسية</h3>', unsafe_allow_html=True)
        for cat in st.session_state['perms']:
            if st.button(cat):
                st.session_state['sub_view'] = cat
                st.session_state['view'] = "الفرعية"
                st.rerun()

    # ج: الخدمات الفرعية (التنفيذ المباشر)
    elif st.session_state['view'] == "الفرعية":
        cat = st.session_state['sub_view']
        st.markdown(f'<h3 style="text-align: center; color: #002e63;">{cat}</h3>', unsafe_allow_html=True)

        if cat == "العمليات الميدانية":
            t1, t2 = st.tabs(["المتابعة اليومية", "معرض الأسطول"])
            with t1:
                plate = st.selectbox("رقم اللوحة", FLEET_PLATES)
                st.camera_input("تصوير حالة المركبة")
                note = st.text_area("ملاحظات الفحص")
                if st.button("حفظ وإرسال التقرير الميداني"):
                    data = pd.DataFrame([[datetime.now(), st.session_state['username'], plate, "يومي", note]], columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"])
                    data.to_csv(DB_REPORTS, mode='a', header=False, index=False)
                    st.success("تم الحفظ بنجاح")
            with t2:
                for p in FLEET_PLATES[:10]: st.markdown(f'<div class="metric-card">مركبة رقم: {p}</div>', unsafe_allow_html=True)

        elif cat == "الأرشفة والوثائق":
            st.file_uploader("رفع مستند رسمي")
            st.text_area("بلاغ عن عطل فني")
            if st.button("تأكيد الأرشفة"): st.success("تم الحفظ")

        elif cat == "إدارة النظام":
            if st.session_state['role'] == "الإدارة":
                with st.expander("إضافة مستخدم جديد"):
                    nu = st.text_input("اسم المستخدم")
                    np = st.text_input("كلمة المرور", type="password")
                    pms = st.multiselect("تحديد الصلاحيات", ["العمليات الميدانية", "الأرشفة والوثائق", "إدارة النظام"])
                    if st.button("تفعيل الحساب"):
                        new_data = pd.DataFrame([[nu, np, "موظف", ",".join(pms)]], columns=["username", "password", "role", "perms"])
                        new_data.to_csv(DB_USERS, mode='a', header=False, index=False)
                        st.success(f"تم إنشاء حساب {nu}")
                st.dataframe(pd.read_csv(DB_USERS)[['username', 'role', 'perms']], use_container_width=True)
            else: st.warning("صلاحية الإدارة فقط")
