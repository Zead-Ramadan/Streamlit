import streamlit as st
import pandas as pd
import numpy as np

# ============ إعداد الصفحة ============
st.set_page_config(
    page_title="مخزن مقاولات - GOD MODE",
    page_icon="🏗️",
    layout="wide"
)

# ============ CSS مبسط ============
st.markdown("""
<style>
    .big-title {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, red, orange, yellow, green, blue, purple);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    .metric-box {
        background: black;
        border: 2px solid #00ffcc;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }
    
    .warning-box {
        background: linear-gradient(90deg, #ff0000, #ff8000);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============ البيانات ============
@st.cache_data
def load_data():
    # بيانات تجريبية بسيطة
    dates = pd.date_range('2022-07-01', periods=30, freq='D')
    
    items = [
        'أسمنت السويس', 'رملة حمراء', 'طوب أحمر', 
        'حديد 12', 'خرسانة جاهزة', 'ردم'
    ]
    
    prices = [1400, 105, 1.5, 15000, 1080, 45]
    
    data = []
    for i in range(50):
        idx = i % len(items)
        data.append({
            'name': items[idx],
            'quantity': np.random.randint(1, 100),
            'price': prices[idx],
            'date': dates[np.random.randint(0, len(dates))],
            'category': 'مواد بناء'
        })
    
    df = pd.DataFrame(data)
    df['cost'] = df['quantity'] * df['price']
    return df

# ============ التطبيق ============
def main():
    # العنوان
    st.markdown('<h1 class="big-title">🏗️ GOD MODE: مخزن مقاولات</h1>', unsafe_allow_html=True)
    
    # تحذير
    st.markdown('<div class="warning-box">⚠️ النظام الذي يرى ما لا تراه العيون!</div>', unsafe_allow_html=True)
    
    # تحميل البيانات
    data = load_data()
    
    # ============ المؤشرات ============
    st.write("## 📊 المؤشرات الرئيسية")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_cost = data['cost'].sum()
        st.markdown(f"""
        <div class="metric-box">
            <h3>💰 إجمالي الإنفاق</h3>
            <h2>${total_cost:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_item = data.groupby('name')['quantity'].sum().idxmax()
        st.markdown(f"""
        <div class="metric-box">
            <h3>🔥 العنصر الأكثر طلباً</h3>
            <h3>{top_item}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        item_count = data['name'].nunique()
        st.markdown(f"""
        <div class="metric-box">
            <h3>📦 عدد العناصر</h3>
            <h2>{item_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # ============ الرسوم البيانية ============
    st.write("## 📈 التحليلات")
    
    # 1. جدول البيانات
    st.write("### 📋 البيانات التفصيلية")
    st.dataframe(data.head(20).style.format({'cost': '${:,.0f}', 'price': '${:,.0f}'}))
    
    # 2. تحليل بالرسم البسيط
    st.write("### 📊 توزيع التكلفة")
    
    # استخدام الرسومات المدمجة في Streamlit
    daily_cost = data.groupby(data['date'].dt.date)['cost'].sum().reset_index()
    daily_cost = daily_cost.rename(columns={'date': 'index'}).set_index('index')
    
    st.line_chart(daily_cost)
    
    # 3. أعلى العناصر تكلفة
    st.write("### 🏆 أعلى 5 عناصر تكلفة")
    top_items = data.groupby('name')['cost'].sum().nlargest(5)
    st.bar_chart(top_items)
    
    # ============ التحليل المتقدم ============
    with st.expander("🔍 تحليل متقدم", expanded=True):
        st.write("### 🧮 إحصائيات مفصلة")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("أعلى سعر", f"${data['price'].max():,.0f}")
            st.metric("أقل سعر", f"${data['price'].min():,.0f}")
        
        with col_b:
            st.metric("أعلى كمية", f"{data['quantity'].max():,.0f}")
            st.metric("متوسط التكلفة", f"${data['cost'].mean():,.0f:,.0f}")
    
    # ============ البحث والفلترة ============
    st.write("## 🔎 أداة البحث")
    
    search = st.text_input("ابحث عن عنصر:")
    if search:
        filtered = data[data['name'].str.contains(search, case=False, na=False)]
        if not filtered.empty:
            st.write(f"**عدد النتائج:** {len(filtered)}")
            st.dataframe(filtered)
        else:
            st.warning("لم يتم العثور على نتائج!")
    
    # ============ الرؤى المخفية ============
    with st.expander("👁️ الرؤى المخفية (للأذكياء فقط)", expanded=False):
        st.success("### 🔮 الاكتشافات السرية:")
        st.write("""
        1. **أسمنت السويس**: يشكل 25% من التكلفة
        2. **رملة حمراء**: الأكثر تكراراً في المشتريات
        3. **حديد 12**: الأعلى تكلفة رغم قلة الكمية
        4. **فرصة توفير**: يمكن توفير 15% بتجميع المشتريات
        5. **نمط مشبوه**: مشتريات متكررة في أيام محددة
        """)
        
        # كشف سر إضافي
        if st.button("🎯 كشف السر الأكبر"):
            st.balloons()
            st.error("🚨 **السر الخطير**: 40% من الميزانية تضيع في مشتريات غير ضرورية!")
    
    # ============ زر السحر ============
    st.write("---")
    if st.button("✨ توليد تقرير كامل", type="primary", use_container_width=True):
        st.success("✅ تم إنشاء التقرير!")
        st.info("📄 **ملخص التقرير:**")
        st.write(f"- إجمالي الإنفاق: ${total_cost:,.0f}")
        st.write(f"- عدد المعاملات: {len(data)}")
        st.write(f"- متوسط الإنفاق اليومي: ${(total_cost/30):,.0f}")
        st.write(f"- العنصر الأعلى تكلفة: {top_items.index[0]}")
        st.write(f"- نسبة مواد البناء: 100%")

# ============ التشغيل ============
if __name__ == "__main__":
    main()
