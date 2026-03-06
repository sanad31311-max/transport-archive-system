import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. إعدادات النظام وقواعد البيانات ---
DB_PERSONNEL = "personnel_db.csv"
DB_FINANCE = "finance_db.csv"
DB_INSTALLMENTS = "installments_db.csv"
CARS_DIR = "assets/cars"

def init_system():
    if not os.path.exists(CARS_DIR): os.makedirs(CARS_DIR)
    
    # سجل الأفراد والمركبات المرتبطة
    if not os.path.exists(DB_PERSONNEL):
        pd.DataFrame(columns=["اسم الفرد", "الهوية", "اللوحة المرتبطة", "القيمة الشهرية", "الحالة"]).to_csv(DB_PERSONNEL, index=False)
    
    # سجل الحسابات الموحد (خدمات، مستحقات، تقسيط)
    if not os.path.exists(DB_FINANCE):
        pd.DataFrame(columns=["التاريخ", "الفرد", "الفئة", "النوع", "الوصف", "المبلغ"]).to_csv(DB_FINANCE, index=False)
        
    # سجل مبيعات التقسيط
    if not os.path.exists(DB_INSTALLMENTS):
        pd.DataFrame(columns=["التاريخ", "العميل", "المركبة", "إجمالي المبلغ", "الدفعة المقدمة", "القسط الشهري", "المدة", "المتبقي"]).to_csv(DB_INSTALLMENTS, index=False)

init_system()

# --- 2. التنسيق الرسمي المطور (CSS) ---
st.set_page_config(page_title="نظام مؤسسة أسطول الخليج", layout="wide", initial_sidebar_state="collapsed")
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
        border: none !important;
    }
    .nav-btn button { background-color: #475569 !important; height: 2.6em !important; }
    .alert-card {
        background-color: #fef2f2; padding: 15px; border-radius: 8px;
        border-right: 6px solid #dc2626; margin-bottom: 10px;
    }
    .metric-card {
        background: white; padding: 15px; border-radius: 8px;
        border-right: 6px solid #002e63; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'view' not in st.session_state: st.session_state['view'] = "الرئيسية"

# --- 4. شاشة تسجيل الدخول ---
if not st.session_state['auth']:
    st.markdown('<h2 style="color: #002e63; text-align: center; margin-top: 50px;">بوابة الإدارة المركزية</h2>', unsafe_allow_html=True)
    u_in = st.text_input("اسم المستخدم")
    p_in = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        if u_in == "Jassim" and p_in == "Jassim2026":
            st.session_state['auth'] = True; st.rerun()
        else: st.error("بيانات الدخول غير صحيحة")

# --- 5. الواجهة المركزية ---
else:
    # شريط التحكم (رجوع يمين | تحديث يسار)
    c_r, c_s, c_l = st.columns([0.25, 0.5, 0.25])
    with c_r:
        if st.session_state['view'] != "الرئيسية":
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("الرجوع للقائمة"): st.session_state['view'] = "الرئيسية"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c_l:
        st.markdown('<div class="nav-box">', unsafe_allow_html=True)
        if st.button("تحديث النظام"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state['view'] == "الرئيسية":
        st.markdown("<h4 style='text-align: center; color: #002e63;'>لوحة تحكم مؤسسة أسطول الخليج</h4>", unsafe_allow_html=True)
        
        # --- نظام التنبيهات الآلي ---
        p_df = pd.read_csv(DB_PERSONNEL)
        f_df = pd.read_csv(DB_FINANCE)
        current_month = datetime.now().strftime("%Y-%m")
        
        alerts = []
        if not p_df.empty:
            for _, row in p_df.iterrows():
                name = row['اسم الفرد']
                monthly_req = float(row['القيمة الشهرية'])
                # حساب المدفوع هذا الشهر لفئة المستحقات أو التقسيط (دائن)
                paid = f_df[(f_df['الفرد'] == name) & 
                            (f_df['التاريخ'].str.startswith(current_month)) & 
                            (f_df['النوع'] == "دائن")]['المبلغ'].sum()
                
                if paid < monthly_req:
                    alerts.append({"الأسم": name, "المطلوب": monthly_req, "المدفوع": paid, "المتبقي": monthly_req - paid})

        if alerts:
            st.markdown("##### تنبيهات المتأخرات للشهر الحالي")
            for alert in alerts:
                st.markdown(f"""
                <div class="alert-card">
                    <b>{alert['الأسم']}</b>: متبقي عليه مبلغ <b>{alert['المتبقي']}</b> ريال من القيمة الشهرية المطلوبة.
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("إدارة الأفراد والسيارات"): st.session_state['view'] = "الأفراد"; st.rerun()
            if st.button("العمليات المالية"): st.session_state['view'] = "المالية"; st.rerun()
        with col2:
            if st.button("إدارة مبيعات التقسيط"): st.session_state['view'] = "التقسيط"; st.rerun()
            if st.button("مركز كشوفات الحسابات"): st.session_state['view'] = "الكشوفات"; st.rerun()
        
        st.write("---")
        if st.button("نظام إدارة الأسطول (الميداني)"): st.session_state['view'] = "الأسطول"; st.rerun()
        if st.button("خروج"): st.session_state['auth'] = False; st.rerun()

    # أ: مركز الكشوفات المتخصصة (تحميل CSV)
    elif st.session_state['view'] == "الكشوفات":
        st.markdown("<h4>مركز كشوفات الحسابات</h4>")
        p_df = pd.read_csv(DB_PERSONNEL)
        f_df = pd.read_csv(DB_FINANCE)
        if not p_df.empty:
            sel_p = st.selectbox("اختر الفرد", p_df['اسم الفرد'].tolist())
            f_type = st.selectbox("الفئة", ["كشف حساب موحد", "الخدمات", "المستحقات", "التقسيط"])
            
            filtered = f_df[f_df['الفرد'] == sel_p] if f_type == "كشف حساب موحد" else f_df[(f_df['الفرد'] == sel_p) & (f_df['الفئة'] == f_type)]
            
            debit = filtered[filtered['النوع'] == "مدين"]['المبلغ'].sum()
            credit = filtered[filtered['النوع'] == "دائن"]['المبلغ'].sum()
            
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f'<div class="metric-card"><h6>مدين</h6><h5>{debit}</h5></div>', unsafe_allow_html=True)
            with m2: st.markdown(f'<div class="metric-card"><h6>دائن</h6><h5>{credit}</h5></div>', unsafe_allow_html=True)
            with m3: st.markdown(f'<div class="metric-card"><h6>الصافي</h6><h5>{debit - credit}</h5></div>', unsafe_allow_html=True)
            
            st.dataframe(filtered.sort_values(by="التاريخ", ascending=False), use_container_width=True)
            st.download_button("تصدير الكشف", filtered.to_csv(index=False).encode('utf-8-sig'), f"statement_{sel_p}.csv")

    # ب: العمليات المالية (إدارة CRUD كاملة)
    elif st.session_state['view'] == "المالية":
        st.markdown("<h4>إدارة العمليات المالية</h4>")
        df_f = pd.read_csv(DB_FINANCE)
        p_list = pd.read_csv(DB_PERSONNEL)['اسم الفرد'].tolist()
        
        tab_add, tab_edit = st.tabs(["إضافة حركة", "تعديل وحذف"])
        with tab_add:
            if p_list:
                with st.form("add_fin"):
                    f_p = st.selectbox("الفرد", p_list)
                    f_c = st.selectbox("الفئة", ["الخدمات", "المستحقات", "التقسيط"])
                    f_t = st.radio("النوع", ["مدين", "دائن"], horizontal=True)
                    f_d = st.text_input("الوصف")
                    f_a = st.number_input("المبلغ", min_value=0.0)
                    if st.form_submit_button("حفظ العملية"):
                        pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), f_p, f_c, f_t, f_d, f_a]], columns=df_f.columns).to_csv(DB_FINANCE, mode='a', header=False, index=False)
                        st.success("تم الحفظ"); st.rerun()
            else: st.warning("سجل الأفراد أولاً")
        
        with tab_edit:
            if not df_f.empty:
                idx = st.selectbox("اختر العملية", df_f.index)
                curr = df_f.loc[idx]
                n_amt = st.number_input("المبلغ", value=float(curr['المبلغ']))
                n_desc = st.text_input("الوصف", value=curr['الوصف'])
                if st.button("حفظ التعديل"):
                    df_f.at[idx, 'المبلغ'] = n_amt
                    df_f.at[idx, 'الوصف'] = n_desc
                    df_f.to_csv(DB_FINANCE, index=False); st.success("تم التحديث"); st.rerun()
                if st.button("حذف السجل"):
                    df_f.drop(idx).to_csv(DB_FINANCE, index=False); st.warning("تم الحذف"); st.rerun()

    # ج: نظام الأسطول (الميداني)
    elif st.session_state['view'] == "الأسطول":
        st.markdown("<h4>نظام إدارة الأسطول الميداني</h4>")
        st.info("استعراض اللوحات، الكاميرا الميدانية، ومعرض المستندات")
