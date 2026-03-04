import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات النظام والمجلدات ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"
CARS_DIR = "assets/cars"
DOCS_DIR = "assets/docs"
EXTRA_DIR = "assets/extra_fleet_docs" # مجلد المستندات الإضافية للسيارات

def init_system():
    for folder in [CARS_DIR, DOCS_DIR, EXTRA_DIR]:
        if not os.path.exists(folder): os.makedirs(folder)
    
    # إصلاح ملف التقارير
    cols = ["التاريخ", "من", "إلى", "اللوحة", "النوع", "التفاصيل", "الحالة"]
    if os.path.exists(DB_REPORTS):
        try:
            df = pd.read_csv(DB_REPORTS)
            for c in cols:
                if c not in df.columns: df[c] = "مقروء" if c == "الحالة" else "-"
            df.to_csv(DB_REPORTS, index=False)
        except: pd.DataFrame(columns=cols).to_csv(DB_REPORTS, index=False)
    else:
        pd.DataFrame(columns=cols).to_csv(DB_REPORTS, index=False)

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

    div.stButton > button {
        width: 100% !important; height: 2.6em !important; 
        border-radius: 8px !important; background-color: #002e63 !important;
        color: white !important; font-size: 14px !important; font-weight: bold !important;
        margin-bottom: 6px !important; border: none !important;
    }
    .nav-box button { background-color: #475569 !important; height: 2.3em !important; }
    .alert-btn button { background-color: #dc2626 !important; border: 1px solid white !important; }
    .metric-card {
        background: white; padding: 12px; border-radius: 10px;
        border-right: 5px solid #002e63; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة والتنقل ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"
if 'sub_view' not in st.session_state: st.session_state['sub_view'] = None

FLEET_PLATES = [str(p) for p in [1140, 1527, 1644, 1716, 1811, 1994, 2070, 2430, 2672, 2700, 3010, 3228, 3462, 3515, 3516, 3547, 3597, 3599, 3606, 3634, 3635, 3636, 3656, 3830, 3838, 3850, 4179, 4383, 4669, 5471, 5645, 5786, 5826, 6123, 6264, 6265, 6388, 6472, 6785, 6787, 6800, 6901, 6922, 6972, 6995, 7123, 7233, 7353, 7455, 7646, 7668, 7906, 8116, 8465, 8484, 8674, 8795, 8796, 8797, 8827, 8834, 8940, 9109]]

# --- 4. شاشة الدخول ---
if not st.session_state['auth']:
    st.markdown('<h3 style="color: #002e63; text-align: center; margin-top: 20px;">نظام أسطول الخليج</h3>', unsafe_allow_html=True)
    u_df = pd.read_csv(DB_USERS)
    u_in = st.selectbox("المستخدم", u_df['username'].tolist())
    p_in = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        v = u_df[(u_df['username'] == u_in) & (u_df['password'] == p_in)]
        if not v.empty:
            st.session_state.update({'auth': True, 'username': u_in, 'role': v.iloc[0]['role'], 'perms': v.iloc[0]['perms'].split(",")})
            st.rerun()
        else: st.error("خطأ")

# --- 5. الواجهة الداخلية ---
else:
    # أزرار التنقل العلوي
    c_r, c_s, c_l = st.columns([0.3, 0.4, 0.3])
    with c_r:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-box">', unsafe_allow_html=True)
            if st.button("⬅️ رجوع"):
                if st.session_state['sub_view']: st.session_state['sub_view'] = None
                else: st.session_state['view'] = "الرئيسية"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c_l:
        st.markdown('<div class="nav-box">', unsafe_allow_html=True)
        if st.button("🔄 تحديث"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    reps_df = pd.read_csv(DB_REPORTS)
    # التنبيهات: تشمل ما أرسل للمستخدم مباشرة + ما أرسل للقناة العامة وهو "جديد"
    unread = len(reps_df[((reps_df['إلى'] == st.session_state['username']) | (reps_df['إلى'] == "القناة العامة")) & (reps_df['الحالة'] == "جديد")])

    if st.session_state['view'] == "الرئيسية":
        st.markdown(f'<h4 style="color: #002e63; text-align: center;">لوحة التحكم</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.markdown(f'<div class="metric-card"><h6>المركبات</h6><h5>{len(FLEET_PLATES)}</h5></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h6>تنبيهات</h6><h5>{unread}</h5></div>', unsafe_allow_html=True)
        
        st.write("---")
        for cat in st.session_state['perms']:
            if st.button(cat):
                st.session_state['sub_view'] = cat; st.session_state['view'] = "الفرعية"; st.rerun()
        
        st.write("---")
        if unread > 0:
            st.markdown('<div class="alert-btn">', unsafe_allow_html=True)
            if st.button(f"📊 مركز التقارير ({unread} جديد)"):
                st.session_state['view'] = "التقارير"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button("📊 مركز التقارير"):
                st.session_state['view'] = "التقارير"; st.rerun()
        
        if st.button("🚪 خروج"):
            st.session_state['auth'] = False; st.rerun()

    elif st.session_state['view'] == "التقارير":
        st.markdown('<h4 style="text-align: center;">قائمة التقارير</h4>', unsafe_allow_html=True)
        # العرض: الإدارة ترى الكل | الموظف يرى (ما له، ما أرسله، وما في القناة العامة)
        if st.session_state['role'] == "الإدارة":
            disp = reps_df
        else:
            disp = reps_df[(reps_df['إلى'] == st.session_state['username']) | 
                           (reps_df['من'] == st.session_state['username']) | 
                           (reps_df['إلى'] == "القناة العامة")]
        
        st.dataframe(disp.sort_values(by="التاريخ", ascending=False), use_container_width=True)
        
        # تحديث الحالة
        if unread > 0:
            reps_df.loc[((reps_df['إلى'] == st.session_state['username']) | (reps_df['إلى'] == "القناة العامة")) & (reps_df['الحالة'] == "جديد"), "الحالة"] = "مقروء"
            reps_df.to_csv(DB_REPORTS, index=False)

    elif st.session_state['view'] == "الفرعية":
        cat = st.session_state['sub_view']
        
        if cat == "العمليات الميدانية":
            t1, t2 = st.tabs(["إرسال تقرير", "معرض الأسطول المطور"])
            with t1:
                plate = st.selectbox("رقم اللوحة", FLEET_PLATES)
                # إضافة "القناة العامة" لقائمة المرسلين إليهم
                user_list = ["القناة العامة"] + pd.read_csv(DB_USERS)['username'].tolist()
                target = st.selectbox("توجيه التقرير إلى", user_list)
                st.camera_input("التقاط صورة ميدانية")
                note = st.text_area("الملاحظات")
                if st.button("إرسال التقرير"):
                    new = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state['username'], target, plate, "ميداني", note, "جديد"]], columns=reps_df.columns)
                    new.to_csv(DB_REPORTS, mode='a', header=False, index=False)
                    st.success(f"تم الإرسال إلى {target}")

            with t2:
                sel_p = st.selectbox("استعراض بيانات المركبة رقم", FLEET_PLATES)
                p_car, p_doc = os.path.join(CARS_DIR, f"{sel_p}.jpg"), os.path.join(DOCS_DIR, f"{sel_p}_reg.jpg")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("📸 صورة السيارة")
                    if os.path.exists(p_car): 
                        st.image(p_car)
                        with open(p_car, "rb") as file:
                            st.download_button("تحميل الصورة", file, file_name=f"car_{sel_p}.jpg", key="dl_c"+sel_p)
                    else: 
                        up_c = st.file_uploader("رفع صورة الأساس", key="up_c"+sel_p)
                        if up_c:
                            with open(p_car, "wb") as f: f.write(up_c.getbuffer())
                            st.rerun()

                with col_b:
                    st.write("📄 الاستمارة الرسمية")
                    if os.path.exists(p_doc): 
                        st.image(p_doc)
                        with open(p_doc, "rb") as file:
                            st.download_button("تحميل الاستمارة", file, file_name=f"doc_{sel_p}.jpg", key="dl_d"+sel_p)
                    else:
                        up_d = st.file_uploader("رفع الاستمارة", key="up_d"+sel_p)
                        if up_d:
                            with open(p_doc, "wb") as f: f.write(up_d.getbuffer())
                            st.rerun()

                st.divider()
                st.markdown("📂 **مستندات إضافية لهذه المركبة**")
                specific_extra_dir = os.path.join(EXTRA_DIR, sel_p)
                if not os.path.exists(specific_extra_dir): os.makedirs(specific_extra_dir)
                
                new_extra = st.file_uploader(f"إضافة مستند جديد للمركبة {sel_p}", key="extra_up"+sel_p)
                if new_extra:
                    with open(os.path.join(specific_extra_dir, new_extra.name), "wb") as f:
                        f.write(new_extra.getbuffer())
                    st.success("تمت الإضافة"); st.rerun()
                
                extra_files = os.listdir(specific_extra_dir)
                if extra_files:
                    for f_name in extra_files:
                        with open(os.path.join(specific_extra_dir, f_name), "rb") as f:
                            st.download_button(f"📥 تحميل: {f_name}", f, file_name=f_name, key="extra_"+f_name)
                else: st.info("لا توجد مستندات إضافية لهذه اللوحة")

        elif cat == "الأرشفة والوثائق":
            up = st.file_uploader("رفع مستند للأرشيف العام")
            if up:
                with open(os.path.join(DOCS_DIR, up.name), "wb") as f: f.write(up.getbuffer())
                st.success("تمت الأرشفة")
            st.divider()
            for f in os.listdir(DOCS_DIR):
                if not f.endswith("_reg.jpg"): # تجنب عرض الاستمارات هنا
                    with open(os.path.join(DOCS_DIR, f), "rb") as file:
                        st.download_button(f"📥 تحميل {f}", file, file_name=f)

        elif cat == "إدارة النظام":
            if st.session_state['role'] == "الإدارة":
                st.dataframe(pd.read_csv(DB_USERS))
