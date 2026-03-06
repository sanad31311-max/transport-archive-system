import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. تهيئة النظام وإصلاح البيانات تلقائياً ---
DB_FILES = {
    "personnel_db.csv": ["اسم الفرد", "الهوية", "اللوحة المرتبطة", "القيمة الشهرية", "الحالة"],
    "finance_db.csv": ["التاريخ", "الفرد", "الفئة", "النوع", "الوصف", "المبلغ"],
    "installments_db.csv": ["التاريخ", "العميل", "المركبة", "إجمالي المبلغ", "الدفعة المقدمة", "القسط الشهري", "المدة", "المتبقي"]
}

def init_system():
    if not os.path.exists("assets"): os.makedirs("assets")
    for file, cols in DB_FILES.items():
        if not os.path.exists(file):
            pd.DataFrame(columns=cols).to_csv(file, index=False)
        else:
            try:
                # التأكد من سلامة الأعمدة لمنع الشاشة البيضاء
                df = pd.read_csv(file)
                for col in cols:
                    if col not in df.columns:
                        df[col] = 0 if "المبلغ" in col else "-"
                df.to_csv(file, index=False)
            except:
                pd.DataFrame(columns=cols).to_csv(file, index=False)

init_system()

# --- 2. التنسيق الرسمي (CSS) المحاكي للتطبيقات الحكومية ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] {visibility: hidden !important;}
    .block-container {padding: 1rem !important;}
    div.stButton > button {
        width: 100% !important; height: 3.5em !important; 
        border-radius: 8px !important; background-color: #002e63 !important;
        color: white !important; font-size: 16px !important; font-weight: bold !important;
        border: none !important; margin-bottom: 10px;
    }
    .nav-btn button { background-color: #475569 !important; height: 2.8em !important; }
    .metric-card {
        background: white; padding: 15px; border-radius: 10px;
        border-right: 6px solid #002e63; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"

# --- 4. شاشة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<h2 style="color: #002e63; text-align: center;">نظام مؤسسة أسطول الخليج المركزي</h2>', unsafe_allow_html=True)
    with st.container():
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام"):
            if u == "Jassim" and p == "Jassim2026":
                st.session_state['auth'] = True; st.rerun()
            else: st.error("خطأ في البيانات")

# --- 5. الواجهة الأساسية ---
else:
    # شريط التنقل (توزيع يمين/يسار حسب مخططك)
    c_r, c_s, c_l = st.columns([0.3, 0.4, 0.3])
    with c_r:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("الرجوع"): st.session_state['view'] = "الرئيسية"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c_l:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("تحديث"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state['view'] == "الرئيسية":
        st.markdown("<h3 style='text-align: center; color: #002e63;'>لوحة تحكم الإدارة</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("سجل الأفراد والسيارات"): st.session_state['view'] = "الأفراد"; st.rerun()
            if st.button("إدارة مبيعات التقسيط"): st.session_state['view'] = "التقسيط"; st.rerun()
        with col2:
            if st.button("العمليات المالية"): st.session_state['view'] = "المالية"; st.rerun()
            if st.button("مركز الكشوفات"): st.session_state['view'] = "الكشوفات"; st.rerun()
        
        st.divider()
        if st.button("نظام إدارة الأسطول الميداني"): st.session_state['view'] = "الأسطول"; st.rerun()
        if st.button("تسجيل الخروج"): st.session_state['auth'] = False; st.rerun()

    # أ: كشوفات الحسابات (تطبيق المخطط اليدوي)
    elif st.session_state['view'] == "الكشوفات":
        st.markdown("<h4 style='text-align: center; color: #002e63;'>مركز كشوفات الحسابات</h4>", unsafe_allow_html=True)
        p_df = pd.read_csv("personnel_db.csv")
        f_df = pd.read_csv("finance_db.csv")
        
        if not p_df.empty:
            sel_p = st.selectbox("اختر الفرد", p_df['اسم الفرد'].tolist())
            f_cat = st.selectbox("نوع الكشف", ["موحد", "الخدمات", "المستحقات", "التقسيط"])
            
            # تصفية البيانات حسب الفئة
            data = f_df[f_df['الفرد'] == sel_p] if f_cat == "موحد" else f_df[(f_df['الفرد'] == sel_p) & (f_df['الفئة'] == f_cat)]
            
            deb = data[data['النوع'] == "مدين"]['المبلغ'].sum()
            cre = data[data['النوع'] == "دائن"]['المبلغ'].sum()
            
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f'<div class="metric-card"><h6>مدين</h6><h5>{deb}</h5></div>', unsafe_allow_html=True)
            with m2: st.markdown(f'<div class="metric-card"><h6>دائن</h6><h5>{cre}</h5></div>', unsafe_allow_html=True)
            with m3: st.markdown(f'<div class="metric-card"><h6>الصافي</h6><h5>{deb - cre}</h5></div>', unsafe_allow_html=True)
            
            st.dataframe(data.sort_values(by="التاريخ", ascending=False), use_container_width=True)
        else: st.warning("لا توجد بيانات مسجلة")

    # ب: العمليات المالية (إدارة شاملة CRUD)
    elif st.session_state['view'] == "المالية":
        st.markdown("<h4 style='text-align: center; color: #002e63;'>إدارة العمليات المالية</h4>", unsafe_allow_html=True)
        df_f = pd.read_csv("finance_db.csv")
        p_list = pd.read_csv("personnel_db.csv")['اسم الفرد'].tolist()
        
        t1, t2 = st.tabs(["إضافة عملية", "تعديل وحذف"])
        with t1:
            if p_list:
                with st.form("add_fin"):
                    f_p = st.selectbox("اسم الفرد", p_list)
                    f_c = st.selectbox("الفئة", ["الخدمات", "المستحقات", "التقسيط"])
                    f_t = st.radio("نوع العملية", ["مدين", "دائن"], horizontal=True)
                    f_d = st.text_input("وصف العملية (مثال: دفعة مقدمة، صيانة..)")
                    f_a = st.number_input("المبلغ", min_value=0.0)
                    if st.form_submit_button("حفظ العملية"):
                        new_row = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), f_p, f_c, f_t, f_d, f_a]], columns=df_f.columns)
                        new_row.to_csv("finance_db.csv", mode='a', header=False, index=False)
                        st.success("تم الحفظ"); st.rerun()
            else: st.info("سجل الأفراد أولاً")
        
        with t2:
            if not df_f.empty:
                idx = st.selectbox("اختر العملية للتعديل أو الحذف", df_f.index)
                if st.button("حذف السجل المالي"):
                    df_f.drop(idx).to_csv("finance_db.csv", index=False)
                    st.warning("تم الحذف"); st.rerun()

    # ج: نظام الأسطول (النظام الفرعي)
    elif st.session_state['view'] == "الأسطول":
        st.markdown("<h4 style='text-align: center; color: #002e63;'>نظام إدارة الأسطول الميداني</h4>", unsafe_allow_html=True)
        st.info("خدمات الكاميرا ومعرض المستندات والـ 63 لوحة تعمل هنا.")
