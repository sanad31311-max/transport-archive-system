import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. تأسيس وقواعد البيانات ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"

def init_databases():
    if not os.path.exists(DB_REPORTS):
        pd.DataFrame(columns=["التاريخ", "المستخدم", "اللوحة", "النوع", "التفاصيل"]).to_csv(DB_REPORTS, index=False)
    if not os.path.exists(DB_USERS):
        # المستخدم الأساسي
        initial_users = pd.DataFrame([
            ["Jassim", "Jassim2026", "الإدارة", "العمليات الميدانية,الأرشفة والوثائق,إدارة النظام"]
        ], columns=["username", "password", "role", "perms"])
        initial_users.to_csv(DB_USERS, index=False)

init_databases()

# --- 2. التنسيق الرسمي الصارم (CSS) ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    
    /* إخفاء القوائم العلوية والجانبية نهائياً لمنع الكربكة */
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] {visibility: hidden !important;}
    .block-container {padding: 2rem 1rem 5rem 1rem !important;}

    /* تصميم الأزرار المركزية الضخمة */
    div.stButton > button {
        width: 100% !important;
        height: 5em !important;
        border-radius: 15px !important;
        background-color: #002e63 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        margin-bottom: 30px !important;
        border: none !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }

    /* زر الرجوع والتحديث */
    .control-btn button { background-color: #64748b !important; height: 3.5em !important; }

    /* البطاقات التعريفية */
    .info-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid #002e63;
        margin-bottom: 35px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الحالة (Navigation Logic) ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية" # الرئيسية، الخدمات، الفرعية

FLEET_PLATES = [str(p) for p in [1140, 1527, 1644, 1716, 1811, 1994, 2070, 2430, 2672, 2700, 3010, 3228, 3462, 3515, 3516, 3547, 3597, 3599, 3606, 3634, 3635, 3636, 3656, 3830, 3838, 3850, 4179, 4383, 4669, 5471, 5645, 5786, 5826, 6123, 6264, 6265, 6388, 6472, 6785, 6787, 6800, 6901, 6922, 6972, 6995, 7123, 7233, 7353, 7455, 7646, 7668, 7906, 8116, 8465, 8484, 8674, 8795, 8796, 8797, 8827, 8834, 8940, 9109]]

# --- 4. واجهة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<h1 style="color: #002e63; text-align: center; margin-top: 50px;">مؤسسة أسطول الخليج</h1>', unsafe_allow_html=True)
    with st.container():
        u_list = pd.read_csv(DB_USERS)['username'].tolist()
        u_in = st.selectbox("المستخدم", u_list)
        p_in = st.text_input("كلمة المرور", type="password")
        if st.button("حفظ وإرسال بيانات الدخول"):
            users = pd.read_csv(DB_USERS)
            valid = users[(users['username'] == u_in) & (users['password'] == p_in)]
            if not valid.empty:
                st.session_state.update({'auth': True, 'username': u_in, 'role': valid.iloc[0]['role'], 'perms': valid.iloc[0]['perms'].split(",")})
                st.rerun()
            else: st.error("البيانات غير صحيحة")

# --- 5. نظام التشغيل المركزي (بعد الدخول) ---
else:
    # أزرار التحكم الثابتة (رجوع وتحديث)
    c_up1, c_up2 = st.columns([0.8, 0.2])
    with c_up2:
        if st.button("تحديث"): st.rerun()
    with c_up1:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if st.button("رجوع للخلف"):
                if st.session_state['view'] == "الفرعية": st.session_state['view'] = "الخدمات"
                elif st.session_state['view'] == "الخدمات": st.session_state['view'] = "الرئيسية"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    view = st.session_state['view']

    # --- أ: الصفحة الرئيسية (الرئيسية) ---
    if view == "الرئيسية":
        st.markdown(f'<h2 style="text-align: center; color: #002e63;">مرحباً {st.session_state["username"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-card">عدد المركبات المسجلة: 63</div>', unsafe_allow_html=True)
        
        # الزر المركزي الضخم
        if st.button("قائمة الخدمات المركزية"):
            st.session_state['view'] = "الخدمات"
            st.rerun()
        
        if st.button("خروج"):
            st.session_state['auth'] = False
            st.rerun()

    # --- ب: صفحة التصنيفات الأساسية (الخدمات) ---
    elif view == "الخدمات":
        st.markdown('<h2 style="text-align: center;">التصنيفات الأساسية للخدمات</h2>', unsafe_allow_html=True)
        
        # استعراض التصنيفات بناءً على صلاحيات المستخدم
        for cat in st.session_state['perms']:
            if st.button(cat):
                st.session_state['current_cat'] = cat
                st.session_state['view'] = "الفرعية"
                st.rerun()

    # --- ج: صفحة الخدمات الفرعية (الفرعية) ---
    elif view == "الفرعية":
        cat = st.session_state['current_cat']
        st.markdown(f'<h2 style="text-align: center;">{cat}</h2>', unsafe_allow_html=True)

        if cat == "العمليات الميدانية":
            if st.button("المتابعة اليومية"): 
                st.info("تم تفعيل نموذج المتابعة")
                plate = st.selectbox("اللوحة", FLEET_PLATES)
                st.camera_input("الكاميرا")
                if st.button("إرسال التقرير"): st.success("تم الحفظ")
            
            if st.button("معرض الأسطول"):
                st.info("قائمة المركبات الـ 63")
                for p in FLEET_PLATES[:5]: st.write(f"مركبة: {p}")

        elif cat == "الأرشفة والوثائق":
            if st.button("أرشفة مستندات"): st.file_uploader("رفع ملف")
            if st.button("بلاغات الأعطال"): st.text_area("وصف العطل")

        elif cat == "إدارة النظام":
            if st.session_state['role'] == "الإدارة":
                if st.button("إضافة مستخدم جديد"):
                    with st.container():
                        new_u = st.text_input("الاسم")
                        new_p = st.text_input("كلمة المرور")
                        pms = st.multiselect("التصنيفات المتاحة له", ["العمليات الميدانية", "الأرشفة والوثائق"])
                        if st.button("تفعيل المستخدم"):
                            new_data = pd.DataFrame([[new_u, new_p, "موظف", ",".join(pms)]], columns=["username", "password", "role", "perms"])
                            new_data.to_csv(DB_USERS, mode='a', header=False, index=False)
                            st.success("تم الإضافة بنجاح")
                
                if st.button("عرض سجل المستخدمين"):
                    st.dataframe(pd.read_csv(DB_USERS), use_container_width=True)
            else:
                st.warning("صلاحية الإدارة فقط")
