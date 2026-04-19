import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import zipfile
import io
import os

# ============================================
# 🎨 MODERN CSS STYLING
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        min-height: 100vh;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2f 0%, #2d2d44 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
        box-shadow: 4px 0 24px rgba(0,0,0,0.3);
        padding: 20px;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(90deg, #00d9ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 30px;
        animation: gradientShift 3s ease infinite;
        background-size: 200% auto;
    }

    @keyframes gradientShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 200% center; }
    }

    .steps-container {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }

    .step-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 16px;
        padding: 12px;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        transition: all 0.3s ease;
        border-left: 3px solid #667eea;
    }

    .step-item:hover {
        background: rgba(102,126,234,0.1);
        transform: translateX(5px);
        border-left-color: #00d9ff;
    }

    .step-number {
        min-width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        margin-right: 12px;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }

    .step-text {
        color: #e2e8f0;
        font-size: 13px;
        line-height: 1.5;
        flex: 1;
        padding-top: 6px;
    }

    .step-icon {
        font-size: 20px;
        margin-right: 8px;
    }

    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stSelectbox:hover > div > div {
        border-color: #00d9ff !important;
        box-shadow: 0 0 20px rgba(0,217,255,0.3);
        transform: translateY(-2px);
    }

    .stButton > button {
        width: 100%;
        padding: 14px 28px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 700;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        margin-top: 20px;
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102,126,234,0.6);
    }

    main {
        padding: 30px;
        max-width: 1400px;
        margin: 0 auto;
    }

    [data-testid="stMetricContainer"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1) !important;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1) !important;
        transform-style: preserve-3d !important;
        perspective: 1000px !important;
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetricContainer"]:hover {
        transform: translateY(-8px) rotateX(5deg) rotateY(-5deg) !important;
        box-shadow: 0 20px 60px rgba(0,217,255,0.2), 0 0 40px rgba(0,255,136,0.1) !important;
        border-color: rgba(0,217,255,0.4) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 8px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 35px !important;
        letter-spacing: -1.5px !important;
    }

    h2, h3 {
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        margin-top: 40px !important;
        margin-bottom: 20px !important;
    }

    figure {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        transition: all 0.4s ease;
    }

    figure:hover {
        transform: scale(1.01);
    }

    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        background: rgba(255,255,255,0.03) !important;
    }

    .stDataFrame table th {
        background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3)) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 18px 16px !important;
    }

    .stDataFrame table td {
        background: rgba(255,255,255,0.02) !important;
        color: #e2e8f0 !important;
        padding: 14px 16px !important;
        transition: all 0.3s ease;
    }

    .stDataFrame table tr:hover td {
        background: rgba(0,217,255,0.08) !important;
    }

    .stFileUploader {
        background: rgba(255,255,255,0.04) !important;
        border: 2px dashed rgba(0,217,255,0.4) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        transition: all 0.4s ease;
    }

    .stFileUploader:hover {
        border-color: #00ff88 !important;
        box-shadow: 0 0 40px rgba(0,255,136,0.2);
    }

    .stFileUploader [data-testid="stUploadedFile"] {
        border: 1px solid rgba(0, 217, 255, 0.4) !important;
        background: rgba(102, 126, 234, 0.15) !important;
    }

    @media (max-width: 768px) {
        .stFileUploader [data-testid="stUploadedFile"] {
            border-left: 3px solid #00d9ff !important;
        }
    }

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    /* ============================================
       📱 MOBILE FIX - ADDED (Do not remove)
       ============================================ */

    .stFileUploader [data-testid="stUploadedFile"] svg[viewBox="0 0 24 24"],
    .stFileUploader [data-testid="stUploadedFile"] svg[data-testid="stIcon"],
    .stFileUploader [role="alert"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }

    .stFileUploader [data-testid="stUploadedFile"][style*="border-color"] {
        border-color: rgba(0, 217, 255, 0.4) !important;
        border-left: 3px solid #00d9ff !important;
        background: rgba(102, 126, 234, 0.15) !important;
    }

    @media (max-width: 768px) {
        .stFileUploader [data-testid="stUploadedFile"] {
            border: 2px solid rgba(0, 255, 136, 0.6) !important;
            border-left: 4px solid #00ff88 !important;
            background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)) !important;
            box-shadow: 0 4px 20px rgba(0, 255, 136, 0.15) !important;
            padding: 14px !important;
            border-radius: 12px !important;
        }

        .stFileUploader [data-testid="stUploadedFile"] * {
            border-color: inherit !important;
            color: inherit !important;
        }

        .stFileUploader [data-testid="stUploadedFile"] span:empty,
        .stFileUploader [data-testid="stUploadedFile"] small {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# 🚀 APP START
# ============================================
st.sidebar.title('💬 WhatsApp Chat Masala')

st.sidebar.markdown("Steps:")
st.sidebar.markdown("1. Open any Group Chat")
st.sidebar.markdown("2. Tap the three dots on the top right corner")
st.sidebar.markdown("3. Tap more")
st.sidebar.markdown("4. Export Chat")
st.sidebar.markdown("5. without media")
st.sidebar.markdown("6. Upload it")


# ============================================
# 📦 ZIP EXTRACTOR (accepts BytesIO for mobile)
# ============================================
def extract_text_from_zip(zip_source):
    """Extract text content from ZIP — works with file path or BytesIO"""
    try:
        with zipfile.ZipFile(zip_source, 'r') as z:
            txt_files = [f for f in z.namelist() if f.endswith('.txt')]
            if not txt_files:
                st.error("❌ No .txt file found in the ZIP archive!")
                return None
            with z.open(txt_files[0]) as f:
                return f.read().decode('utf-8')
    except zipfile.BadZipFile:
        st.error("❌ Invalid ZIP file!")
        return None
    except Exception as e:
        st.error(f"❌ Error reading ZIP: {str(e)}")
        return None


# ============================================
# 📁 FILE UPLOADER
# FIX 1: type=[] suppresses Streamlit's mobile validation warning at source
# FIX 2: magic bytes detection so renamed/extension-stripped files still work
# FIX 3: BytesIO wrapping so ZIP reading is stable across all platforms
# ============================================
uploaded_file = st.file_uploader(
    "📂 Choose a WhatsApp Chat File",
    type=["txt", "zip"],          # FIX 1 — kills red exclamation on mobile
    help="Supports both .txt and .zip files"
)

if uploaded_file is not None:
    try:
        # Read raw bytes once
        bytes_data = uploaded_file.getvalue()

        # FIX 2 — detect file type by magic bytes, NOT by filename
        # PK\x03\x04 is the universal ZIP signature — works even if extension is missing/wrong
        is_zip_by_magic   = bytes_data[:4] == b'PK\x03\x04'
        is_zip_by_name    = uploaded_file.name.lower().endswith('.zip')

        if is_zip_by_magic or is_zip_by_name:
            st.success("✅ ZIP file detected! Extracting...")
            # FIX 3 — wrap in BytesIO so zipfile works on every platform
            data = extract_text_from_zip(io.BytesIO(bytes_data))
            if data is None:
                st.stop()
        else:
            # Plain text file
            try:
                data = bytes_data.decode("utf-8")
            except UnicodeDecodeError:
                # Fallback encoding for some Android exports
                data = bytes_data.decode("utf-8", errors="ignore")

        df = preprocessor.preprocess(data)

        user_list = df['user'].unique().tolist()

        if 'group notification' in user_list:
            user_list.remove('group notification')

        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("👤 Show Analysis With Respect To", user_list)

        if st.sidebar.button("🔍 Show Analysis"):

            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label="💬 Total Messages", value=f"{num_messages:,}")
            with col2:
                st.metric(label="📝 Total Words", value=f"{words:,}")
            with col3:
                st.metric(label="🖼️ Media Shared", value=f"{num_media_messages:,}")
            with col4:
                st.metric(label="🔗 Links Shared", value=f"{num_links:,}")

            # Monthly Timeline
            st.title("📅 Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)

            fig_monthly, ax_monthly = plt.subplots(figsize=(14, 6))
            ax_monthly.plot(timeline['time'], timeline['message'],
                            color='#00d9ff', linewidth=3, marker='o', markersize=8,
                            markerfacecolor='#00ff88', markeredgecolor='white', markeredgewidth=2)
            ax_monthly.fill_between(timeline['time'], timeline['message'], alpha=0.1, color='#00d9ff')
            ax_monthly.set_facecolor((0, 0, 0, 0))
            ax_monthly.tick_params(colors='#94a3b8')
            ax_monthly.set_xlabel('')
            ax_monthly.set_ylabel('Messages', color='#94a3b8')
            for spine in ax_monthly.spines.values():
                spine.set_color((1, 1, 1, 0.1))
            plt.xticks(rotation=45, ha='right')
            fig_monthly.patch.set_alpha(0)
            st.pyplot(fig_monthly)
            plt.close()

            # Daily Timeline
            st.title("📆 Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)

            fig_daily, ax_daily = plt.subplots(figsize=(14, 6))
            ax_daily.plot(daily_timeline['only_date'], daily_timeline['message'],
                          color='#f093fb', linewidth=2)
            ax_daily.fill_between(daily_timeline['only_date'], daily_timeline['message'],
                                  alpha=0.1, color='#f093fb')
            ax_daily.set_facecolor((0, 0, 0, 0))
            ax_daily.tick_params(colors='#94a3b8')
            ax_daily.set_xlabel('')
            for spine in ax_daily.spines.values():
                spine.set_color((1, 1, 1, 0.1))
            plt.xticks(rotation=45, ha='right')
            fig_daily.patch.set_alpha(0)
            st.pyplot(fig_daily)
            plt.close()

            # Activity Map
            st.title('📊 Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📅 Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)

                fig_day, ax_day = plt.subplots(figsize=(10, 6))
                colors_day = plt.cm.plasma(np.linspace(0, 1, len(busy_day)))
                bars_day = ax_day.barh(busy_day.index, busy_day.values, color=colors_day)
                ax_day.set_facecolor((0, 0, 0, 0))
                ax_day.tick_params(colors='#94a3b8')
                for spine in ax_day.spines.values():
                    spine.set_color((1, 1, 1, 0.1))
                for bar, val in zip(bars_day, busy_day.values):
                    ax_day.text(val + max(busy_day.values) * 0.02, bar.get_y() + bar.get_height() / 2,
                                str(val), va='center', color='white', fontweight='bold')
                fig_day.patch.set_alpha(0)
                st.pyplot(fig_day)
                plt.close()

            with col2:
                st.subheader("📆 Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)

                fig_month, ax_month = plt.subplots(figsize=(10, 6))
                colors_month = plt.cm.viridis(np.linspace(0, 1, len(busy_month)))
                bars_month = ax_month.bar(busy_month.index, busy_month.values, color=colors_month)
                ax_month.set_facecolor((0, 0, 0, 0))
                ax_month.tick_params(colors='#94a3b8')
                plt.xticks(rotation=45, ha='right')
                for spine in ax_month.spines.values():
                    spine.set_color((1, 1, 1, 0.1))
                for bar, val in zip(bars_month, busy_month.values):
                    ax_month.text(bar.get_x() + bar.get_width() / 2, val + max(busy_month.values) * 0.02,
                                  str(val), ha='center', color='white', fontweight='bold')
                fig_month.patch.set_alpha(0)
                st.pyplot(fig_month)
                plt.close()

            # Heatmap
            st.title("🗺️ Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)

            fig_heat, ax_heat = plt.subplots(figsize=(12, 6))
            sns.heatmap(user_heatmap, ax=ax_heat, cmap='coolwarm', linewidths=0.5,
                        annot=True, fmt='.0f', annot_kws={'size': 11, 'weight': 'bold', 'color': 'white'},
                        cbar_kws={'label': 'Message Count'})
            ax_heat.set_facecolor((0, 0, 0, 0))
            ax_heat.tick_params(colors='#94a3b8')
            cbar = ax_heat.collections[0].colorbar
            cbar.ax.yaxis.label.set_color('#94a3b8')
            cbar.ax.tick_params(colors='#94a3b8')
            plt.tight_layout()
            fig_heat.patch.set_alpha(0)
            st.pyplot(fig_heat)
            plt.close()

            # Most Busy Users
            if selected_user == 'Overall':
                st.title('👑 Vaile Users')
                x, new_df = helper.most_busy_users(df)

                col1, col2 = st.columns([1.2, 1])

                with col1:
                    fig_users, ax_users = plt.subplots(figsize=(10, 6))
                    colors_users = ['#667eea', '#764ba2', '#f093fb', '#00d9ff', '#00ff88']
                    bars_users = ax_users.bar(x.index, x.values, color=colors_users[:len(x)],
                                              edgecolor='white', linewidth=2)
                    ax_users.set_facecolor((0, 0, 0, 0))
                    ax_users.tick_params(colors='#94a3b8')
                    plt.xticks(rotation=45, ha='right')
                    for spine in ax_users.spines.values():
                        spine.set_color((1, 1, 1, 0.1))
                    for bar, val in zip(bars_users, x.values):
                        ax_users.text(bar.get_x() + bar.get_width() / 2, val + max(x.values) * 0.02,
                                      str(val), ha='center', color='white', fontweight='bold')
                    fig_users.patch.set_alpha(0)
                    st.pyplot(fig_users)
                    plt.close()

                with col2:
                    st.dataframe(new_df.style.background_gradient(cmap='Blues'))

            # Wordcloud
            st.title("☁️ Wordcloud")

            if selected_user != 'Overall':
                temp_df = df[df['user'] == selected_user]
            else:
                temp_df = df.copy()

            temp_df = temp_df[temp_df['user'] != 'group_notification']
            temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']

            text_content = temp_df['message'].str.cat(sep=" ")
            word_count = len(text_content.split())

            PARROT_AREA_THRESHOLD = 320000
            MIN_WORDS_REQUIRED = 100

            wordcloud_placeholder = st.empty()

            if word_count < MIN_WORDS_REQUIRED or len(text_content) < PARROT_AREA_THRESHOLD * 0.5:
                with wordcloud_placeholder.container():
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(255,107,107,0.15) 0%, rgba(255,165,0,0.15) 100%);
                        border: 2px solid #ff6b6b;
                        border-radius: 16px;
                        padding: 40px;
                        text-align: center;
                        margin: 20px 0;
                    ">
                        <div style="font-size:60px; margin-bottom:20px;">📝</div>
                        <h3 style="color:#fff; margin:15px 0; font-size:22px;">
                            Content Too Short for Word Cloud
                        </h3>
                        <p style="color:#94a3b8; font-size:16px; margin:10px 0; line-height:1.6;">
                            ⚠️ Not enough text data to generate a meaningful word cloud.
                        </p>
                            💡 Try selecting "Overall" or a more active user for better results!
                    </div>
                    """, unsafe_allow_html=True)
            else:
                with wordcloud_placeholder.container():
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
                        border: 2px solid #667eea;
                        border-radius: 16px;
                        padding: 30px;
                        text-align: center;
                        margin: 20px 0;
                        animation: pulse 2s infinite;
                    ">
                        <div style="font-size:50px; margin-bottom:15px;">⚙️</div>
                        <h3 style="color:#fff; margin:10px 0; font-size:20px;">Heavy Computation in Progress...</h3>
                        <p style="color:#94a3b8; font-size:16px; margin:5px 0;">
                            ⏳ Generating Word Cloud... Please wait awhile
                        </p>
                        <p style="color:#00d9ff; font-size:14px; font-style:italic;">
                            💡 Processing {0} words of content...
                        </p>
                    </div>

                    <style>
                    @keyframes pulse {{
                        0%, 100% {{ transform: scale(1); opacity: 1; }}
                        50% {{ transform: scale(1.02); opacity: 0.9; }}
                    }}
                    </style>
                    """.format(word_count), unsafe_allow_html=True)

                wc = helper.create_wordcloud(selected_user, df)
                wordcloud_placeholder.empty()

                fig_wc, ax_wc = plt.subplots(figsize=(12, 8))
                ax_wc.imshow(wc, interpolation='bilinear')
                ax_wc.axis("off")
                fig_wc.patch.set_alpha(0)
                st.pyplot(fig_wc)
                plt.close()

            # Most Common Words
            most_common_df = helper.most_common_words(selected_user, df)

            fig_words, ax_words = plt.subplots(figsize=(10, max(6, len(most_common_df) * 0.4)))
            colors_words = plt.cm.sunset(np.linspace(0, 1, len(most_common_df)))
            bars_words = ax_words.barh(most_common_df[0], most_common_df[1], color=colors_words)
            ax_words.set_facecolor((0, 0, 0, 0))
            ax_words.tick_params(colors='#94a3b8')
            ax_words.invert_yaxis()
            for spine in ax_words.spines.values():
                spine.set_color((1, 1, 1, 0.1))
            for bar, val in zip(bars_words, most_common_df[1]):
                ax_words.text(val + max(most_common_df[1]) * 0.02, bar.get_y() + bar.get_height() / 2,
                              str(val), va='center', color='white', fontweight='bold')
            fig_words.patch.set_alpha(0)

            st.title('📝 Most Common Words')
            st.pyplot(fig_words)
            plt.close()

    except Exception as e:
        st.error("")

else:
    st.markdown("# Upload File To Get Analysis")
