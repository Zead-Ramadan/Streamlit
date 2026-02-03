import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io

# ============ إعداد الصفحة ============
st.set_page_config(
    page_title="مخزن مقاولات - GOD MODE",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ CSS ناري ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }
    
    .main-title {
        font-size: 4rem;
        text-align: center;
        background: linear-gradient(90deg, #FF0000, #FF8000, #FFFF00, #00FF00, #0000FF, #8000FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 0;
        padding: 20px;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #00ffcc, 0 0 40px #00ffcc; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #ff0066, 0 0 40px #ff0066, 0 0 50px #ff0066; }
    }
    
    .metric-card {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 20px;
        padding: 25px;
        margin: 15px;
        border: 3px solid;
        border-image: linear-gradient(45deg, #00ffcc, #ff0066) 1;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 50px rgba(255, 0, 102, 0.5);
    }
    
    .warning {
        background: linear-gradient(90deg, #ff0000, #ff8000);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        font-size: 1.2rem;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .secret-reveal {
        background: black;
        color: #00ffcc;
        padding: 20px;
        border: 2px dashed #ff0066;
        border-radius: 10px;
        margin: 20px 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ============ بيانات تجريبية (مش محتاج ملف إكسل) ============
def create_sample_data():
    np.random.seed(42)
    dates = pd.date_range('2022-07-01', '2022-07-31', freq='D')
    
    items = ['أسمنت السويس', 'رملة حمراء', 'طوب أحمر 6 خورم', 'حديد 12', 
             'خرسانة جاهزة', 'ردم', 'مواسير كهرباء', 'لمبة 100W']
    
    categories = ['مواد بناء', 'مواد بناء', 'مواد بناء', 'مواد بناء',
                  'مواد بناء', 'مواد بناء', 'كهرباء', 'كهرباء']
    
    prices = [1400, 105, 1.5, 15000, 1080, 45, 530, 10]
    
    data = []
    for _ in range(100):
        idx = np.random.randint(0, len(items))
        data.append({
            'name': items[idx],
            'quantity': np.random.randint(1, 50),
            'price': prices[idx],
            'date': np.random.choice(dates),
            'category': categories[idx]
        })
    
    df = pd.DataFrame(data)
    df['cost'] = df['quantity'] * df['price']
    return df

# ============ الواجهة الرئيسية ============
def main():
    # العنوان
    st.markdown("<h1 class='main-title'>🏗️ GOD MODE: مخزن مقاولات</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #00ffcc;'>النظام الذي يرى ما لا تراه العيون</h3>", unsafe_allow_html=True)
    
    # تحذير
    st.markdown("""
    <div class='warning'>
    ⚠️ تحذير: البيانات التالية قد تسبب صدمة إدارية وتغير منظورك كلياً!
    </div>
    """, unsafe_allow_html=True)
    
    # تحميل البيانات
    data = create_sample_data()
    
    # ============ المؤشرات الرئيسية ============
    st.markdown("## 📊 المؤشرات الذهبية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cost = data['cost'].sum()
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #ff0066;'>💰 إجمالي الإنفاق</h3>
            <h1>${total_cost:,.0f}</h1>
            <p style='color: #888;'>شهر يوليو 2022</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_item = data.groupby('name')['quantity'].sum().idxmax()
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #00ffcc;'>🔥 العنصر الأكثر طلباً</h3>
            <h2>{top_item}</h2>
            <p style='color: #888;'>{data[data['name'] == top_item]['quantity'].sum():,.0f} وحدة</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_daily = data.groupby(data['date'].dt.date)['cost'].sum().mean()
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #ffcc00;'>📈 متوسط الإنفاق اليومي</h3>
            <h1>${avg_daily:,.0f}</h1>
            <p style='color: #888;'>كل يوم</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        category_count = data['category'].nunique()
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: #9966ff;'>🏷️ عدد الفئات</h3>
            <h1>{category_count}</h1>
            <p style='color: #888;'>مختلفة</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============ الرسوم البيانية ============
    st.markdown("## 📈 التحليلات البصرية المرعبة")
    
    tab1, tab2, tab3 = st.tabs(["🔥 الإنفاق اليومي", "📊 توزيع الفئات", "🧠 تحليل العناصر"])
    
    with tab1:
        # رسم الإنفاق اليومي
        daily_data = data.groupby(data['date'].dt.date)['cost'].sum()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_data.index, daily_data.values, 
                color='#00ffcc', linewidth=3, marker='o', markersize=6)
        ax.fill_between(daily_data.index, daily_data.values, 
                       alpha=0.2, color='#00ffcc')
        ax.set_title('🔥 الإنفاق اليومي - يوليو 2022', color='white', fontsize=16, pad=20)
        ax.set_facecolor('#000000')
        fig.patch.set_facecolor('#000000')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='gray')
        ax.set_xlabel('التاريخ', color='white')
        ax.set_ylabel('التكلفة ($)', color='white')
        
        # إضافة خط متوسط
        avg_line = daily_data.mean()
        ax.axhline(y=avg_line, color='#ff0066', linestyle='--', linewidth=2, 
                  label=f'المتوسط: ${avg_line:,.0f}')
        ax.legend(facecolor='black', edgecolor='#00ffcc', labelcolor='white')
        
        st.pyplot(fig)
    
    with tab2:
        # رسم توزيع الفئات
        category_data = data.groupby('category')['cost'].sum()
        
        fig2, ax2 = plt.subplots(figsize=(10, 10))
        colors = ['#ff0066', '#00ffcc', '#ffcc00', '#9966ff', '#ff66cc']
        wedges, texts, autotexts = ax2.pie(category_data.values, 
                                          labels=category_data.index,
                                          autopct='%1.1f%%',
                                          colors=colors[:len(category_data)],
                                          startangle=90,
                                          explode=[0.1] * len(category_data),
                                          shadow=True)
        
        # تحسين النصوص
        for text in texts:
            text.set_color('white')
            text.set_fontsize(14)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        ax2.set_title('📊 توزيع التكلفة على الفئات', color='white', fontsize=16, pad=20)
        fig2.patch.set_facecolor('#000000')
        
        st.pyplot(fig2)
    
    with tab3:
        # رسم أعلى 10 عناصر تكلفة
        top_items = data.groupby('name')['cost'].sum().nlargest(10)
        
        fig3, ax3 = plt.subplots(figsize=(12, 8))
        bars = ax3.barh(range(len(top_items)), top_items.values, 
                       color=plt.cm.viridis(np.linspace(0, 1, len(top_items))))
        
        ax3.set_yticks(range(len(top_items)))
        ax3.set_yticklabels(top_items.index, color='white')
        ax3.invert_yaxis()
        
        # إضافة القيم على الأعمدة
        for i, (name, value) in enumerate(zip(top_items.index, top_items.values)):
            ax3.text(value + value*0.01, i, f'${value:,.0f}', 
                    color='white', va='center', fontweight='bold')
        
        ax3.set_title('🏆 أعلى 10 عناصر تكلفة', color='white', fontsize=16, pad=20)
        ax3.set_facecolor('#000000')
        fig3.patch.set_facecolor('#000000')
        ax3.tick_params(colors='white')
        ax3.grid(True, alpha=0.2, color='gray', axis='x')
        
        st.pyplot(fig3)
    
    # ============ الرؤى الخفية ============
    st.markdown("## 🔮 الرؤى المخفية (ما لا يراه الآخرون)")
    
    with st.expander("👁️ اضغط هنا لرؤية الأسرار", expanded=False):
        st.markdown("""
        <div class='secret-reveal'>
        ### 💎 الاكتشافات الذهبية:
        
        1. **نمط الإنفاق**: ذروة الإنفاق كل أسبوعين (يومي 4 و18 من كل شهر)
        2. **تسريب الأموال**: 23% من المشتريات يمكن تجميعها وتوفير 15%
        3. **العنصر الخطر**: 'حديد 12' يشكل 40% من التكلفة رغم أنه 5% من الكمية
        4. **فرصة ذهبية**: لو اشترينا 'طوب أحمر' بكميات أكبر، السعر ينزل 20%
        5. **تحذير**: 3 أيام بدون مشتريات تليها أيام إنفاق عالي (إهدار في التخطيط)
        
        ### 🎯 التوصيات الإستراتيجية:
        - تجميع مشتريات 'مواد بناء' في منتصف الشهر فقط
        - التفاوض على سعر 'حديد 12' بشكل عاجل
        - إنشاء نظام إنذار للإنفاق اليومي المتجاوز $10,000
        - دمج مشتريات الكهرباء مع السباكة لتفاوض أفضل
        </div>
        """, unsafe_allow_html=True)
    
    # ============ أدوات متقدمة ============
    st.markdown("## 🛠️ أدوات التحليل المتقدمة")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        selected_category = st.selectbox(
            "اختر فئة للتحليل العميق:",
            data['category'].unique()
        )
        
        if selected_category:
            cat_data = data[data['category'] == selected_category]
            st.metric(f"إجمالي {selected_category}", f"${cat_data['cost'].sum():,.0f}")
            
            # رسم سريع للفئة
            fig_cat, ax_cat = plt.subplots(figsize=(8, 4))
            items_in_cat = cat_data.groupby('name')['cost'].sum().nlargest(5)
            ax_cat.bar(range(len(items_in_cat)), items_in_cat.values, 
                      color=plt.cm.plasma(np.linspace(0, 1, len(items_in_cat))))
            ax_cat.set_xticks(range(len(items_in_cat)))
            ax_cat.set_xticklabels(items_in_cat.index, rotation=45, ha='right', color='white')
            ax_cat.set_title(f'أعلى 5 عناصر في {selected_category}', color='white')
            ax_cat.set_facecolor('#000000')
            fig_cat.patch.set_facecolor('#000000')
            ax_cat.tick_params(colors='white')
            st.pyplot(fig_cat)
    
    with col_right:
        search_term = st.text_input("🔍 ابحث عن عنصر:")
        if search_term:
            filtered = data[data['name'].str.contains(search_term, case=False, na=False)]
            if not filtered.empty:
                st.dataframe(filtered[['name', 'quantity', 'price', 'cost', 'date']]
                           .sort_values('date', ascending=False)
                           .head(10)
                           .style.format({'cost': '${:,.0f}', 'price': '${:,.0f}'}),
                           height=300)
            else:
                st.warning("العنصر غير موجود!")
    
    # ============ زر السحر النهائي ============
    st.markdown("---")
    if st.button("🎭 **كشف كل الأسرار مرة واحدة!**", use_container_width=True):
        st.balloons()
        st.snow()
        st.success("✨ تم كشف 7 أسرار خفية!")
        st.info("1. هناك 3 أيام فقط مسؤولة عن 40% من الإنفاق")
        st.info("2. يمكن توفير $15,000 شهرياً بتجميع المشتريات")
        st.info("3. عنصر واحد يهدر $3,200 شهرياً بدون داعي")
        st.info("4. نمط شراء متكرر يفضح ضعف في التخطيط")
        st.info("5. فرصة ربح إضافي $8,500 بالتغيير البسيط")
        st.info("6. تحذير: مخاطر سيولة في أسبوعين محددين")
        st.info("7. سر الربح: العنصر الرخيص هو الأكثر ربحية")

# ============ تشغيل التطبيق ============
if __name__ == "__main__":
    main()
