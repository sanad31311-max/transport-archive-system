import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات النظام وتصحيح قواعد البيانات ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"
CARS_DIR = "assets/cars"
DOCS_DIR = "assets/docs"

def init_system():
    # إنشاء المجلدات أولاً
    for folder in [CARS_DIR, DOCS_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    # إصلاح وتجهيز قاعدة بيانات التقارير (لحماية النظام من KeyError)
    required_cols = ["التاريخ", "من", "إلى", "اللوحة", "النوع", "التفاصيل", "الحالة"]
    if os.path.exists(DB_REPORTS):
        try:
            df = pd.read_csv(DB_REPORTS)
            modified = False
            for col in required_cols:
                if col not in df.columns:
                    df[col] = "مقروء" if col == "الحالة" else "غير متوفر"
                    modified = True
            if modified:
                df.to_csv(DB_REPORTS, index=False)
        except:
            pd.DataFrame(columns=required_cols).to_csv(DB_REPORTS, index=False)
    else:
        pd.DataFrame(columns=required_cols).to_csv(DB_REPORTS, index=False)

    # تجهيز قاعدة بيانات المستخدمين
    if not os.path.exists(DB_USERS):
        pd.DataFrame([["Jassim", "Jassim2026", "الإدارة", "العمليات الميدانية,الأرشفة والوثائق,إدارة النظام"]], 
                     columns=["username", "password", "role", "perms"]).to_csv(DB_USERS, index=False)

init_system()

# --- 2. التنسيق الرسمي المطور للجوال ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] {visibility: hidden !important;}
    .block-container {padding: 0.5rem 1rem !important;}

    /* تصغير الأزرار وضبطها */
    div.stButton > button {
        width: 100% !important; height: 2.5em !important; 
        border-radius: 8px !important; background-color: #002e63 !important;
        color: white !important; font-size: 14px !important; font-weight: bold !important;
        margin-bottom: 5px !important; border: none !important;
    }
    
    .nav-box button { background-color: #475569 !important; height: 2.2em !important; }
    .alert-btn button { background-color: #dc2626 !important; border: 1px solid white !important; }

    .metric-card {
        background: white; padding: 10px; border-radius: 8px;
        border-right: 4px solid #002e63; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 8px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة التنقل ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"
if 'sub_view' not in st.session_state: st.session_state['sub_view'] = None

FLEET_PLATES = [str(p) for p in [1140, 1527, 1644, 1716, 1811, 1994, 2070, 2430, 2672, 2700, 3010, 3228, 3462, 3515, 3516, 3547, 3597, 3599, 3606, 3634, 3635, 3636, 3656, 3830, 3838, 3850, 4179, 4383, 4669, 5471, 5645, 5786, 5826, 6123, 6264, 6265, 6388, 6472, 6785, 6787, 6800, 6901, 6922, 6972, 6995, 7123, 7233, 7353, 7455, 7646, 7668, 7906, 8116, 8465, 8484, 8674, 8795, 8796, 8797, 8827, 8834, 8940, 9109]]

# --- 4. شاشة الدخول ---
if not st.session_state['auth']:
    st.markdown('<h3 style="color: #002e63; text-align: center; margin-top: 20px;">نظام أسطول الخليج</h3>', unsafe_allow_html=True)
    users_df = pd.read_csv(DB_USERS)
    user_in = st.selectbox("المستخدم", users_df['username'].tolist())
    pass_in = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        valid = users_df[(users_df['username'] == user_in) & (users_df['password'] == pass_in)]
        if not valid.empty:
            st.session_state.update({'auth': True, 'username': user_in, 'role': valid.iloc[0]['role'], 'perms': valid.iloc[0]['perms'].split(",")})
            st.rerun()
        else: st.error("خطأ في البيانات")

# --- 5. الواجهة الداخلية ---
else:
    # شريط التحكم العلوي
    c_right, c_spacer, c_left = st.columns([0.3, 0.4, 0.3])
    with c_right:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-box">', unsafe_allow_html=True)
            if st.button("⬅️ رجوع"):
                if st.session_state['sub_view']: st.session_state['sub_view'] = None
                else: st.session_state['view'] = "الرئيسية"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c_left:
        st.markdown('<div class="nav-box">', unsafe_allow_html=True)
        if st.button("🔄 تحديث"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # جلب التقارير وحساب التنبيهات
    try:
        all_reps = pd.read_csv(DB_REPORTS)
        unread_count = len(all_reps[(all_reps['إلى'] == st.session_state['username']) & (all_reps['الحالة'] == "جديد")])
    except:
        unread_count = 0

    if st.session_state['view'] == "الرئيسية":
        st.markdown(f'<h4 style="color: #002e63; text-align: center;">لوحة التحكم</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.markdown(f'<div class="metric-card"><h6>المركبات</h6><h5>{len(FLEET_PLATES)}</h5></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h6>تنبيهات</h6><h5>{unread_count}</h5></div>', unsafe_allow_html=True)
        
        st.write("---")
        # عرض التصنيفات المعتمدة للمستخدم
        for cat in st.session_state['perms']:
            if st.button(cat):
                st.session_state['sub_view'] = cat; st.session_state['view'] = "الفرعية"; st.rerun()
        
        st.write("---")
        # زر التقارير في الأسفل
        if unread_count > 0:
            st.markdown('<div class="alert-btn">', unsafe_allow_html=True)
            if st.button(f"📊 مركز التقارير ({unread_count} جديد)"):
                st.session_state['view'] = "التقارير"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button("📊 مركز التقارير"):
                st.session_state['view'] = "التقارير"; st.rerun()
        
        if st.button("🚪 خروج"):
            st.session_state['auth'] = False; st.rerun()

    elif st.session_state['view'] == "التقارير":
        st.markdown('<h4 style="text-align: center;">استعراض التقارير</h4>', unsafe_allow_html=True)
        reps = pd.read_csv(DB_REPORTS)
        display = reps if st.session_state['role'] == "الإدارة" else reps[(reps['إلى'] == st.session_state['username']) | (reps['من'] == st.session_state['username'])]
        st.dataframe(display.sort_values(by="التاريخ", ascending=False), use_container_width=True)
        
        if unread_count > 0:
            reps.loc[(reps['إلى'] == st.session_state['username']) & (reps['الحالة'] == "جديد"), "الحالة"] = "مقروء"
            reps.to_csv(DB_REPORTS, index=False)

    elif st.session_state['view'] == "الفرعية":
        cat = st.session_state['sub_view']
        
        if cat == "العمليات الميدانية":
            t1, t2 = st.tabs(["إرسال تقرير", "معرض الأسطول"])
            with t1:
                plate = st.selectbox("رقم اللوحة", FLEET_PLATES)
                target = st.selectbox("توجيه التقرير إلى", pd.read_csv(DB_USERS)['username'].tolist())
                note = st.text_area("الملاحظات")
                if st.button("إرسال التقرير"):
                    new_data = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state['username'], target, plate, "ميداني", note, "جديد"]], 
                                           columns=["التاريخ", "من", "إلى", "اللوحة", "النوع", "التفاصيل", "الحالة"])
                    new_data.to_csv(DB_REPORTS, mode='a', header=False, index=False)
                    st.success("تم الإرسال")
            with t2:
                sel_p = st.selectbox("اختر اللوحة للاستعراض", FLEET_PLATES)
                c1, c2 = st.columns(2)
                p_car = os.path.join(CARS_DIR, f"{sel_p}.jpg")
                p_doc = os.path.join(DOCS_DIR, f"{sel_p}_reg.jpg")
                with c1:
                    st.write("صورة السيارة")
                    if os.path.exists(p_car): st.image(p_car)
                    else: 
                        up_c = st.file_uploader("رفع صورة", key="c"+sel_p)
                        if up_c:
                            with open(p_car, "wb") as f: f.write(up_c.getbuffer())
                            st.rerun()
                with c2:
                    st.write("الاستمارة")
                    if os.path.exists(p_doc): st.image(p_doc)
                    else:
                        up_d = st.file_uploader("رفع استمارة", key="d"+sel_p)
                        if up_d:
                            with open(p_doc, "wb") as f: f.write(up_d.getbuffer())
                            st.rerun()

        elif cat == "الأرشفة والوثائق":
            st.markdown("#### الأرشفة الإلكترونية")
            up_file = st.file_uploader("رفع مستند (صورة/PDF)")
            if up_file:
                with open(os.path.join(DOCS_DIR, up_file.name), "wb") as f:
                    f.write(up_file.getbuffer())
                st.success("تم الحفظ في الأرشيف")
            
            st.divider()
            st.write("المستندات المؤرشفة:")
            for f_name in os.listdir(DOCS_DIR):
                with open(os.path.join(DOCS_DIR, f_name), "rb") as f:
                    st.download_button(f"📥 {f_name}", f, file_name=f_name)

        elif cat == "إدارة النظام":
            if st.session_state['role'] == "الإدارة":
                st.write("إدارة الحسابات...")
                st.dataframe(pd.read_csv(DB_USERS))
