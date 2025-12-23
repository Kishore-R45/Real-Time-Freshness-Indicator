import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import io
import os
from datetime import date

# Import local modules
from decay import compute_all_decay
from utils import preprocess_image_from_bytes

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Real-Time Freshness Indicator",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# MODEL LOADING WITH CACHING
# ============================================
@st.cache_resource
def load_model():
    """Load the trained model with caching"""
    from tensorflow.keras.models import load_model
    model_path = os.path.join(os.path.dirname(__file__), "model.h5")
    return load_model(model_path)

# ============================================
# PREDICTION FUNCTION
# ============================================
def predict_freshness(image_bytes, fruit):
    """
    Predict freshness of fruit/vegetable from image bytes
    Returns comprehensive freshness report
    """
    try:
        # Load model
        model = load_model()
        
        # Preprocess image from bytes
        img = preprocess_image_from_bytes(image_bytes)
        
        # Predict initial freshness
        initial = model.predict(img, verbose=0)[0][0]
        initial = max(0, min(round(float(initial), 2), 100))
        
        # Compute decay for all conditions
        decay = compute_all_decay(initial, fruit.lower(), date.today())
        
        # Determine status based on room freshness
        room_freshness = decay['room_final']
        
        if room_freshness > 70:
            status = "FRESH"
            status_color = "#22c55e"
            status_icon = "✅"
            recommendation = "Safe to consume. Store properly to maintain freshness."
        elif room_freshness > 40:
            status = "CONSUME SOON"
            status_color = "#f59e0b"
            status_icon = "⚠️"
            recommendation = "Quality is declining. Consume within the next day or two."
        else:
            status = "SPOILED"
            status_color = "#ef4444"
            status_icon = "❌"
            recommendation = "Not recommended for consumption. Please discard."
        
        result = {
            "success": True,
            "fruit": fruit.capitalize(),
            "initial_freshness": initial,
            "conditions": {
                "ideal": {
                    "name": "Ideal Storage",
                    "description": "Refrigerated at optimal temperature",
                    "freshness": decay['ideal_final'],
                    "days_left": decay['ideal_days_left'],
                    "icon": "❄️"
                },
                "room": {
                    "name": "Room Temperature",
                    "description": "Normal room conditions (~25°C)",
                    "freshness": decay['room_final'],
                    "days_left": decay['room_days_left'],
                    "icon": "🏠"
                },
                "humid": {
                    "name": "High Humidity",
                    "description": "Humid environment (>80% RH)",
                    "freshness": decay['humid_final'],
                    "days_left": decay['humid_days_left'],
                    "icon": "💧"
                }
            },
            "status": status,
            "status_color": status_color,
            "status_icon": status_icon,
            "recommendation": recommendation,
            "chart_data": {
                "labels": ["Ideal Storage", "Room Temp", "High Humidity"],
                "freshness_values": [
                    decay['ideal_final'],
                    decay['room_final'],
                    decay['humid_final']
                ],
                "days_left": [
                    decay['ideal_days_left'],
                    decay['room_days_left'],
                    decay['humid_days_left']
                ]
            },
            "days_since_upload": decay['days_passed'],
            "analysis_date": str(date.today())
        }
        
        return result
        
    except Exception as e:
        return {"error": str(e)}

# ============================================
# CUSTOM CSS FOR ENTERPRISE PREMIUM LOOK
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --secondary-color: #8b5cf6;
        --success-color: #22c55e;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --background-dark: #0f172a;
        --background-card: #1e293b;
        --background-card-hover: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border-color: #334155;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .navbar {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(99, 102, 241, 0.3);
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 30px rgba(99, 102, 241, 0.15);
    }
    
    .navbar-title {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #6366f1 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
        letter-spacing: -0.5px;
    }
    
    .navbar-icon {
        font-size: 2rem;
        margin-right: 0.75rem;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .premium-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-title-icon {
        font-size: 1.25rem;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .status-fresh {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        animation: pulse-green 2s infinite;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        animation: pulse-orange 2s infinite;
    }
    
    .status-spoiled {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        animation: pulse-red 2s infinite;
    }
    
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
        50% { box-shadow: 0 0 0 15px rgba(34, 197, 94, 0); }
    }
    
    @keyframes pulse-orange {
        0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
        50% { box-shadow: 0 0 0 15px rgba(245, 158, 11, 0); }
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    .days-display {
        font-size: 1.8rem;
        font-weight: 800;
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 0.25rem;
    }
    
    .days-number {
        font-size: 2.5rem;
    }
    
    .days-unit {
        font-size: 1rem;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .freshness-bar {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .freshness-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
    }
    
    .condition-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .condition-card:hover {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        color: #64748b;
        font-size: 0.85rem;
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
    }
    
    .stFileUploader > div {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 2px dashed rgba(99, 102, 241, 0.4) !important;
        border-radius: 16px !important;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(99, 102, 241, 0.8) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6) !important;
    }
    
    .stCameraInput > div {
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    
    @media (max-width: 768px) {
        .navbar {
            padding: 0.75rem 1rem;
        }
        
        .navbar-title {
            font-size: 1.25rem;
        }
        
        .premium-card {
            padding: 1rem;
            border-radius: 16px;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .days-number {
            font-size: 1.8rem;
        }
        
        .status-badge {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
    }
    
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================
FRUITS_VEGETABLES = [
    "Apple", "Banana", "Tomato", "Orange",
    "Potato", "Cucumber", "Capsicum", "Okra"
]

FRUIT_ICONS = {
    "Apple": "🍎",
    "Banana": "🍌",
    "Tomato": "🍅",
    "Orange": "🍊",
    "Potato": "🥔",
    "Cucumber": "🥒",
    "Capsicum": "🫑",
    "Okra": "🥬"
}

CONDITION_COLORS = {
    "ideal": "#22c55e",
    "room": "#f59e0b",
    "humid": "#ef4444"
}

MAX_SHELF_LIFE = {
    "Apple": 35,
    "Banana": 5,
    "Tomato": 7,
    "Orange": 28,
    "Potato": 30,
    "Cucumber": 10,
    "Capsicum": 14,
    "Okra": 3
}

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_days_color(days_left, max_days=7):
    """Get color based on days left"""
    ratio = days_left / max_days if max_days > 0 else 0
    if ratio > 0.5:
        return "#22c55e"
    elif ratio > 0.2:
        return "#f59e0b"
    else:
        return "#ef4444"

def create_days_chart(data):
    """Create days remaining chart"""
    labels = data['labels']
    days = data['days_left']
    
    colors = [get_days_color(d, max(days) if max(days) > 0 else 7) for d in days]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=labels,
        y=days,
        marker_color=colors,
        marker_line_color='rgba(255,255,255,0.2)',
        marker_line_width=2,
        text=[f'{d:.1f}' for d in days],
        textposition='outside',
        textfont=dict(color='#f8fafc', size=14, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Days Left: %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter', 'color': '#94a3b8'},
        height=300,
        margin=dict(l=40, r=40, t=30, b=80),
        xaxis=dict(
            tickfont=dict(color='#94a3b8', size=11),
            showgrid=False,
            showline=True,
            linecolor='rgba(51, 65, 85, 0.5)',
        ),
        yaxis=dict(
            tickfont=dict(color='#94a3b8'),
            gridcolor='rgba(51, 65, 85, 0.3)',
            title=dict(text='Days Remaining', font=dict(size=12, color='#94a3b8')),
            showline=True,
            linecolor='rgba(51, 65, 85, 0.5)',
        ),
        showlegend=False,
        bargap=0.35
    )
    
    return fig

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    # Navbar
    st.markdown("""
    <div class="navbar">
        <span class="navbar-title">Real-Time Freshness Indicator</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'image_data' not in st.session_state:
        st.session_state.image_data = None
    if 'selected_fruit' not in st.session_state:
        st.session_state.selected_fruit = "Apple"
    
    # Main Layout
    col_left, col_right = st.columns([1, 1.5], gap="large")
    
    # ============================================
    # LEFT COLUMN - Input Section
    # ============================================
    with col_left:
        st.markdown("""
        <div class="premium-card animate-fade-in">
            <div class="card-title">
                <span class="card-title-icon">📤</span>
                Upload & Analyze
            </div>
        """, unsafe_allow_html=True)
        
        # Fruit/Vegetable Selection
        selected_item = st.selectbox(
            "Select Fruit/Vegetable",
            options=FRUITS_VEGETABLES,
            format_func=lambda x: f"{FRUIT_ICONS.get(x, '🍃')} {x}",
            help="Choose the type of produce you want to analyze"
        )
        st.session_state.selected_fruit = selected_item
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Image Input Options
        tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Camera"])
        
        with tab1:
            uploaded_file = st.file_uploader(
                "Upload an image",
                type=['jpg', 'jpeg', 'png', 'webp'],
                help="Upload a clear image of the fruit/vegetable",
                label_visibility="collapsed"
            )
            
            if uploaded_file:
                st.session_state.image_data = uploaded_file.getvalue()
        
        with tab2:
            camera_image = st.camera_input(
                "Capture image",
                help="Take a photo using your device camera",
                label_visibility="collapsed"
            )
            
            if camera_image:
                st.session_state.image_data = camera_image.getvalue()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Analyze Button
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        analyze_disabled = st.session_state.image_data is None
        
        if st.button("🔬 Analyze Freshness", use_container_width=True, disabled=analyze_disabled):
            with st.spinner("🔄 Analyzing image with AI model..."):
                result = predict_freshness(st.session_state.image_data, selected_item)
                st.session_state.result = result
        
        # Image Preview
        if st.session_state.image_data:
            st.markdown("""
            <div class="premium-card animate-fade-in" style="margin-top: 1rem;">
                <div class="card-title">
                    <span class="card-title-icon">🖼️</span>
                    Image Preview
                </div>
            """, unsafe_allow_html=True)
            
            image = Image.open(io.BytesIO(st.session_state.image_data))
            st.image(image, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ============================================
    # RIGHT COLUMN - Results Section
    # ============================================
    with col_right:
        if st.session_state.result and 'error' not in st.session_state.result:
            result = st.session_state.result
            
            fruit_name = result['fruit']
            max_shelf = MAX_SHELF_LIFE.get(fruit_name, 7)
            
            # Status Badge
            status = result['status']
            status_class = 'status-fresh' if status == 'FRESH' else 'status-warning' if status == 'CONSUME SOON' else 'status-spoiled'
            
            st.markdown(f"""
            <div class="premium-card animate-fade-in" style="text-align: center;">
                <div class="card-title" style="justify-content: center;">
                    <span class="card-title-icon">📊</span>
                    Analysis Results
                </div>
                <div style="margin: 1.5rem 0;">
                    <div class="status-badge {status_class}">
                        {result['status_icon']} {status}
                    </div>
                </div>
                <p style="color: #94a3b8; margin-top: 1rem; font-size: 0.95rem;">
                    {result['recommendation']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card animate-fade-in" style="animation-delay: 0.1s;">
                    <div class="metric-icon">{FRUIT_ICONS.get(result['fruit'], '🍃')}</div>
                    <div class="metric-value">{result['fruit']}</div>
                    <div class="metric-label">Selected Item</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card animate-fade-in" style="animation-delay: 0.2s;">
                    <div class="metric-icon">📈</div>
                    <div class="metric-value">{result['initial_freshness']}%</div>
                    <div class="metric-label">Initial Freshness</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                room_days = result['conditions']['room']['days_left']
                days_color = get_days_color(room_days, max_shelf)
                st.markdown(f"""
                <div class="metric-card animate-fade-in" style="animation-delay: 0.3s;">
                    <div class="metric-icon">🏠</div>
                    <div class="days-display">
                        <span class="days-number" style="color: {days_color};">{room_days:.1f}</span>
                        <span class="days-unit">days</span>
                    </div>
                    <div class="metric-label">Shelf Life (Room Temp)</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
            
            # Storage Conditions
            st.markdown("""
            <div class="premium-card animate-fade-in" style="animation-delay: 0.4s;">
                <div class="card-title">
                    Estimated Shelf Life by Storage Condition
                </div>
            """, unsafe_allow_html=True)
            
            ordered_conditions = ["ideal", "room", "humid"]
            max_days_value = max(
                result["conditions"][k]["days_left"] for k in ordered_conditions
            )

            for key in ordered_conditions:
                condition = result["conditions"][key]
                days_left = condition['days_left']
                bar_width = (days_left / max_days_value) * 100 if max_days_value > 0 else 0
                color = CONDITION_COLORS[key]
                
                if days_left >= 1:
                    days_display = f"{days_left:.1f} days"
                elif days_left > 0:
                    hours = days_left * 24
                    days_display = f"{hours:.0f} hours"
                else:
                    days_display = "Expired"
                
                st.markdown(f"""
                <div class="condition-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.25rem;">{condition['icon']}</span>
                            <span style="color: #f8fafc; font-weight: 600;">{condition['name']}</span>
                        </div>
                        <div class="days-display" style="font-size: 1rem;">
                            <span style="color: {color}; font-weight: 800; font-size: 1.3rem;">{days_display}</span>
                        </div>
                    </div>
                    <div class="freshness-bar">
                        <div class="freshness-bar-fill" style="width: {bar_width}%; background: linear-gradient(90deg, {color} 0%, {color}88 100%);"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span style="color: #64748b; font-size: 0.8rem;">{condition['description']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Days Remaining Chart
            st.markdown("""
            <div class="premium-card animate-fade-in" style="animation-delay: 0.5s;">
                <div class="card-title">
                    <span class="card-title-icon">📅</span>
                    Shelf Life Comparison
                </div>
            """, unsafe_allow_html=True)
            
            fig = create_days_chart(result['chart_data'])
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        elif st.session_state.result and 'error' in st.session_state.result:
            st.markdown(f"""
            <div class="premium-card" style="border-color: rgba(239, 68, 68, 0.4);">
                <div class="card-title" style="color: #ef4444;">
                    <span class="card-title-icon">⚠️</span>
                    Error
                </div>
                <p style="color: #f87171;">{st.session_state.result['error']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-card" style="min-height: 400px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="text-align: center; padding: 3rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">📊</div>
                    <h3 style="color: #94a3b8; font-weight: 600; margin-bottom: 0.5rem;">No Analysis Yet</h3>
                    <p style="color: #64748b; max-width: 300px;">
                        Upload or capture an image of a fruit or vegetable, then click "Analyze Freshness" to see detailed results.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer animate-fade-in">
        <p style="margin-bottom: 0.5rem;">
            <strong>AI-Powered Real-Time Freshness Detection Model</strong>
        </p>
        <p style="font-size: 0.8rem; color: #64748b;">
            Prediction generated using CNN‑based visual analysis combined with
            produce‑specific non‑linear decay modeling.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()