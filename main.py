import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إصلاح وتهيئة قواعد البيانات (منع الشاشة البيضاء) ---
DB_FILES = {
    "personnel_db.csv": ["اسم الفرد", "الهوية", "اللوحة المرتبطة", "القيمة الشهرية", "الحالة"],
    "finance_db.csv": ["التاريخ", "الفرد", "الفئة", "النوع", "الوصف", "المبلغ"],
    "installments_db.csv": ["التاريخ", "العميل", "المركبة", "إجمالي المبلغ", "الدفعة المقدمة", "القسط الشهري", "المدة", "المتبقي"],
    "reports_db.csv": ["التاريخ", "من", "إلى", "اللوحة", "النوع", "التفاصيل", "الحالة"]
}

def repair_and_init():
    if not os.path.exists("assets"): os.makedirs("assets")
    for file, cols in DB_FILES.items():
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                # إضافة الأعمدة الناقصة فوراً لمنع الـ KeyError
                for col in cols:
                    if col not in df.columns:
                        df[col] = "0" if "المبلغ" in col else "-"
                df.to_csv(file, index=False)
            except:
                pd.DataFrame(columns=cols).to_csv(file, index=False)
        else:
            pd.DataFrame(columns=cols).to_csv(file, index=False)

repair_and_init()

# --- 2. التنسيق الرسمي المطور (CSS) ---
st.set_page_config(page_title="مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] {visibility: hidden !important;}
    .block-container {padding: 0.5rem 1rem !important;}
    div.stButton > button {
        width: 100% !important; height: 3.2em !important; 
        border-radius: 6px !important; background-color: #002e63 !important;
        color: white !important; font-size: 15px !important; font-weight: bold !important;
    }
    .nav-btn button { background-color: #475569 !important; height: 2.6em !important; }
    .metric-card {
        background: white; padding: 15px; border-radius: 8px;
        border-right: 6px solid #002e63; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"

# --- 4. الدخول ---
if not st.session_state['auth']:
    st.markdown('<h3 style="color: #002e63; text-align: center; margin-top: 50px;">نظام مؤسسة أسطول الخليج المركزي</h3>', unsafe_allow_html=True)
    u_in = st.text_input("اسم المستخدم")
    p_in = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        if u_in == "Jassim" and p_in == "Jassim2026":
            st.session_state['auth'] = True; st.rerun()
        else: st.error("بيانات الدخول غير صحيحة")

# --- 5. الواجهة الأساسية ---
else:
    # شريط التحكم (توزيع يمين/يسار حسب مخططك)
    c_r, c_s, c_l = st.columns([0.3, 0.4, 0.3])
    with c_r:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("الرجوع للقائمة"): st.session_state['view'] = "الرئيسية"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c_l:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("تحديث النظام"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state['view'] == "الرئيسية":
        st.markdown("<h4 style='text-align: center; color: #002e63;'>لوحة تحكم المؤسسة</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("إدارة الأفراد والسيارات"): st.session_state['view'] = "الأفراد"; st.rerun()
            if st.button("العمليات المالية"): st.session_state['view'] = "المالية"; st.rerun()
        with col2:
            if st.button("إدارة مبيعات التقسيط"): st.session_state['view'] = "التقسيط"; st.rerun()
            if st.button("مركز كشوفات الحسابات"): st.session_state['view'] = "الكشوفات"; st.rerun()
        st.divider()
        if st.button("نظام إدارة الأسطول الميداني"): st.session_state['view'] = "الأسطول"; st.rerun()
        if st.button("خروج"): st.session_state['auth'] = False; st.rerun()

    # قسم كشف الحساب المتخصص (تطبيق المخطط اليدوي)
    elif st.session_state['view'] == "الكشوفات":
        st.markdown("<h4 style='text-align: center;'>مركز كشوفات الحسابات</h4>", unsafe_allow_html=True)
        p_df = pd.read_csv("personnel_db.csv")
        f_df = pd.read_csv("finance_db.csv")
        if not p_df.empty:
            sel_p = st.selectbox("اختر الفرد", p_df['اسم الفرد'].tolist())
            f_cat = st.selectbox("نوع الكشف", ["موحد", "الخدمات", "المستحقات", "التقسيط"])
            
            data = f_df[f_df['الفرد'] == sel_p] if f_cat == "موحد" else f_df[(f_df['الفرد'] == sel_p) & (f_df['الفئة'] == f_cat)]
            
            deb = data[data['النوع'] == "مدين"]['المبلغ'].sum()
            cre = data[data['النوع'] == "دائن"]['المبلغ'].sum()
            
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f'<div class="metric-card"><h6>مدين</h6><h5>{deb}</h5></div>', unsafe_allow_html=True)
            with m2: st.markdown(f'<div class="metric-card"><h6>دائن</h6><h5>{cre}</h5></div>', unsafe_allow_html=True)
            with m3: st.markdown(f'<div class="metric-card"><h6>الصافي</h6><h5>{deb - cre}</h5></div>', unsafe_allow_html=True)
            
            st.dataframe(data.sort_values(by="التاريخ", ascending=False), use_container_width=True)
            st.download_button("تصدير الكشف", data.to_csv(index=False).encode('utf-8-sig'), f"statement_{sel_p}.csv")

    # قسم العمليات المالية (إدارة CRUD كاملة)
    elif st.session_state['view'] == "الالمالية":
        st.markdown("<h4 style='text-align: center;'>إدارة العمليات المالية</h4>", unsafe_allow_html=True)
        # كود الإضافة والتعديل والحذف هنا...
