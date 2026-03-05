import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات النظام وقواعد البيانات (إصلاح تلقائي للأعمدة) ---
DB_REPORTS = "reports_db.csv"
DB_USERS = "users_db.csv"
DB_FINANCE = "finance_db.csv"
DB_PERSONNEL = "personnel_db.csv"
CARS_DIR = "assets/cars"
DOCS_DIR = "assets/docs"
EXTRA_DIR = "assets/extra_fleet_docs"

def init_system():
    for folder in [CARS_DIR, DOCS_DIR, EXTRA_DIR]:
        if not os.path.exists(folder): os.makedirs(folder)
    
    # إصلاح ملف التقارير (منع KeyError)
    cols_reports = ["التاريخ", "من", "إلى", "اللوحة", "النوع", "التفاصيل", "الحالة"]
    if os.path.exists(DB_REPORTS):
        df = pd.read_csv(DB_REPORTS)
        for c in cols_reports:
            if c not in df.columns: df[c] = "مقروء" if c == "الحالة" else "-"
        df.to_csv(DB_REPORTS, index=False)
    else:
        pd.DataFrame(columns=cols_reports).to_csv(DB_REPORTS, index=False)
    
    # تهيئة ملف الأفراد (حسب المخطط اليدوي)
    if not os.path.exists(DB_PERSONNEL):
        pd.DataFrame(columns=["اسم الفرد", "رقم الهوية", "اللوحة المرتبطة", "القيمة الشهرية", "معلومات"]).to_csv(DB_PERSONNEL, index=False)
    
    # تهيئة ملف الحسابات (مدين / دائن)
    if not os.path.exists(DB_FINANCE):
        pd.DataFrame(columns=["التاريخ", "الفرد", "العملية", "الوصف", "المبلغ", "النوع"]).to_csv(DB_FINANCE, index=False)

    # حساب الإدارة الأساسي
    if not os.path.exists(DB_USERS):
        pd.DataFrame([["Jassim", "Jassim2026", "الإدارة", "النظام الأساسي,العمليات الميدانية,الأرشفة والوثائق,إدارة النظام,الحسابات والأفراد"]], 
                     columns=["username", "password", "role", "perms"]).to_csv(DB_USERS, index=False)

init_system()

# --- 2. التنسيق الرسمي المطور (CSS) ---
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
        border-right: 5px solid #002e63; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"
if 'sub_view' not in st.session_state: st.session_state['sub_view'] = None

FLEET_PLATES = [str(p) for p in [1140, 1527, 1644, 1716, 1811, 1994, 2070, 2430, 2672, 2700, 3010, 3228, 3462, 3515, 3516, 3547, 3597, 3599, 3606, 3634, 3635, 3636, 3656, 3830, 3838, 3850, 4179, 4383, 4669, 5471, 5645, 5786, 5826, 6123, 6264, 6265, 6388, 6472, 6785, 6787, 6800, 6901, 6922, 6972, 6995, 7123, 7233, 7353, 7455, 7646, 7668, 7906, 8116, 8465, 8484, 8674, 8795, 8796, 8797, 8827, 8834, 8940, 9109]]

# --- 4. شاشة الدخول ---
if not st.session_state['auth']:
    st.markdown('<h3 style="color: #002e63; text-align: center; margin-top: 20px;">نظام مؤسسة أسطول الخليج المركزي</h3>', unsafe_allow_html=True)
    users_df = pd.read_csv(DB_USERS)
    user_in = st.selectbox("المستخدم", users_df['username'].tolist())
    pass_in = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        valid = users_df[(users_df['username'] == user_in) & (users_df['password'] == pass_in)]
        if not valid.empty:
            st.session_state.update({'auth': True, 'username': user_in, 'role': valid.iloc[0]['role'], 'perms': valid.iloc[0]['perms'].split(",")})
            st.rerun()
        else: st.error("خطأ في بيانات الدخول")

# --- 5. الواجهة الداخلية الموحدة ---
else:
    # شريط التحكم (رجوع يمين | تحديث يسار)
    c_right, c_spacer, c_left = st.columns([0.25, 0.5, 0.25])
    with c_right:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-box">', unsafe_allow_html=True)
            if st.button("رجوع"):
                if st.session_state['sub_view']: st.session_state['sub_view'] = None
                else: st.session_state['view'] = "الرئيسية"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c_left:
        st.markdown('<div class="nav-box">', unsafe_allow_html=True)
        if st.button("تحديث"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    all_reps = pd.read_csv(DB_REPORTS)
    unread_count = len(all_reps[((all_reps['إلى'] == st.session_state['username']) | (all_reps['إلى'] == "القناة العامة")) & (all_reps['الحالة'] == "جديد")])

    # الصفحة الرئيسية (البوابة)
    if st.session_state['view'] == "الرئيسية":
        st.markdown(f'<h4 style="color: #002e63; text-align: center;">لوحة تحكم المؤسسة</h4>', unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)
        with col_m1: st.markdown(f'<div class="metric-card"><h6>المركبات</h6><h5>{len(FLEET_PLATES)}</h5></div>', unsafe_allow_html=True)
        with col_m2: st.markdown(f'<div class="metric-card"><h6>تنبيهات جديدة</h6><h5>{unread_count}</h5></div>', unsafe_allow_html=True)
        
        st.write("---")
        for cat in st.session_state['perms']:
            if st.button(cat):
                st.session_state['sub_view'] = cat; st.session_state['view'] = "الفرعية"; st.rerun()
        
        st.write("---")
        if unread_count > 0:
            st.markdown('<div class="alert-btn">', unsafe_allow_html=True)
            if st.button(f"مركز التقارير - {unread_count} جديد"):
                st.session_state['view'] = "التقارير"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button("مركز التقارير"):
                st.session_state['view'] = "التقارير"; st.rerun()
        
        if st.button("خروج"):
            st.session_state['auth'] = False; st.rerun()

    # نظام الحسابات والأفراد (المخطط اليدوي)
    elif st.session_state['view'] == "الفرعية" and st.session_state['sub_view'] == "الحسابات والأفراد":
        st.markdown('<h4 style="text-align: center;">إدارة الأفراد والسيارات والحسابات</h4>', unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["بيانات الأفراد", "العمليات المالية", "كشف الحساب"])
        
        with t1:
            st.markdown("##### تسجيل وربط فرد بمركبة")
            p_name = st.text_input("اسم الفرد الكامل")
            p_id = st.text_input("رقم الهوية / الإقامة")
            p_plate = st.selectbox("رقم اللوحة المرتبطة", FLEET_PLATES)
            p_val = st.number_input("القيمة المالية الشهرية", min_value=0)
            if st.button("حفظ بيانات الفرد والربط"):
                pd.DataFrame([[p_name, p_id, p_plate, p_val, ""]], columns=["اسم الفرد", "رقم الهوية", "اللوحة المرتبطة", "القيمة الشهرية", "معلومات"]).to_csv(DB_PERSONNEL, mode='a', header=False, index=False)
                st.success(f"تم تسجيل {p_name} وربطه بالمركبة {p_plate}")

        with t2:
            st.markdown("##### إضافة عملية (مدين / دائن)")
            p_list = pd.read_csv(DB_PERSONNEL)['اسم الفرد'].tolist()
            if p_list:
                sel_p = st.selectbox("اختر الفرد", p_list)
                c_type = st.radio("نوع العملية", ["خدمات", "مستحقات"])
                c_side = st.radio("الجانب المالي", ["مدين", "دائن"])
                c_desc = st.text_input("وصف العملية (حسب المخطط)")
                c_amt = st.number_input("المبلغ", min_value=0)
                if st.button("ترحيل العملية المالية"):
                    pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), sel_p, c_type, c_desc, c_amt, c_side]], columns=["التاريخ", "الفرد", "العملية", "الوصف", "المبلغ", "النوع"]).to_csv(DB_FINANCE, mode='a', header=False, index=False)
                    st.success("تم الترحيل المالي")
            else: st.info("يرجى تسجيل الأفراد أولاً")

        with t3:
            st.markdown("##### جدول البيانات المالي التفصيلي")
            st.dataframe(pd.read_csv(DB_FINANCE), use_container_width=True)

    # نظام العمليات الميدانية ومعرض الأسطول
    elif st.session_state['view'] == "الفرعية" and st.session_state['sub_view'] == "العمليات الميدانية":
        t_m1, t_m2 = st.tabs(["إرسال تقرير (كاميرا)", "معرض الأسطول والمستندات"])
        
        with t_m1:
            plate = st.selectbox("رقم اللوحة", FLEET_PLATES)
            target = st.selectbox("توجيه إلى", ["القناة العامة"] + pd.read_csv(DB_USERS)['username'].tolist())
            st.camera_input("التقاط صورة الحالة الميدانية")
            note = st.text_area("تفاصيل البلاغ")
            if st.button("إرسال التقرير"):
                pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), st.session_state['username'], target, plate, "ميداني", note, "جديد"]], columns=all_reps.columns).to_csv(DB_REPORTS, mode='a', header=False, index=False)
                st.success("تم الإرسال بنجاح")

        with t_m2:
            sel_p = st.selectbox("استعراض بيانات اللوحة", FLEET_PLATES)
            c1, c2 = st.columns(2)
            p_car, p_doc = os.path.join(CARS_DIR, f"{sel_p}.jpg"), os.path.join(DOCS_DIR, f"{sel_p}_reg.jpg")
            with c1:
                st.write("صورة السيارة")
                if os.path.exists(p_car):
                    st.image(p_car)
                    with open(p_car, "rb") as f: st.download_button("تحميل الصورة", f, file_name=f"car_{sel_p}.jpg", key="c"+sel_p)
                else:
                    up_c = st.file_uploader("رفع صورة", key="up_c"+sel_p)
                    if up_c:
                        with open(p_car, "wb") as f: f.write(up_c.getbuffer())
                        st.rerun()
            with c2:
                st.write("الاستمارة")
                if os.path.exists(p_doc):
                    st.image(p_doc)
                    with open(p_doc, "rb") as f: st.download_button("تحميل الاستمارة", f, file_name=f"doc_{sel_p}.jpg", key="d"+sel_p)
                else:
                    up_d = st.file_uploader("رفع استمارة", key="up_d"+sel_p)
                    if up_d:
                        with open(p_doc, "wb") as f: f.write(up_d.getbuffer())
                        st.rerun()

    # مركز التقارير
    elif st.session_state['view'] == "التقارير":
        st.markdown('<h4 style="text-align: center;">مركز التقارير الموحد</h4>', unsafe_allow_html=True)
        disp = all_reps if st.session_state['role'] == "الإدارة" else all_reps[(all_reps['إلى'] == st.session_state['username']) | (all_reps['إلى'] == "القناة العامة") | (all_reps['من'] == st.session_state['username'])]
        st.dataframe(disp.sort_values(by="التاريخ", ascending=False), use_container_width=True)
        if unread_count > 0:
            all_reps.loc[((all_reps['إلى'] == st.session_state['username']) | (all_reps['إلى'] == "القناة العامة")) & (all_reps['الحالة'] == "جديد"), "الحالة"] = "مقروء"
            all_reps.to_csv(DB_REPORTS, index=False)
