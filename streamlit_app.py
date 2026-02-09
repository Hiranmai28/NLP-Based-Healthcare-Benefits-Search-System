"""
Streamlit Web Interface for Healthcare Benefits Navigator
"""

import streamlit as st
from src.models.retriever import BenefitRetriever
import time

# Page config
st.set_page_config(
    page_title="NLP-Based Healthcare Benefits Search System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .plan-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
        border-left: 5px solid #1f77b4;
    }
    .benefit-text {
        font-size: 3rem;
        line-height: 1.6;
    }
    .similarity-score {
        background-color: #d4edda;
        padding: 0.5rem;
        border-radius: 5px;
        display: inline-block;
    }
    .category-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize retriever
@st.cache_resource
def load_retriever():
    """Load retriever (cached for performance)"""
    return BenefitRetriever()


def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 NLP-Based Healthcare Benefits Search System</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem; color: #666;'>
            Ask questions about your health insurance benefits!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load retriever
    try:
        retriever = load_retriever()
    except FileNotFoundError:
        st.error("❌ Search index not found! Please run `python src/models/embedding_generator.py` first.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 System Info")
        
        stats = retriever.get_statistics()
        
        st.metric("Total Plans", stats['total_plans'])
        st.metric("Benefits Indexed", stats['total_chunks'])
        st.metric("Categories", len(stats['categories']))
        
        st.divider()
        
        st.subheader("📊 Available Plans")
        for plan in stats['plans']:
            st.write(f"• {plan}")
        
        st.divider()
        
        st.subheader("⚙️ Search Settings")
        num_results = st.slider("Number of results", 1, 10, 5)
        
        plan_filter = st.selectbox(
            "Filter by plan",
            ["All Plans"] + stats['plans']
        )
        
        category_filter = st.selectbox(
            "Filter by category",
            ["All Categories"] + stats['categories']
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search box
        st.subheader("🔍 Ask Your Question")
        
        # Sample questions
        sample_questions = [
            "Does my plan cover gym membership?",
            "What's the copay for primary care visits?",
            "Is dental care covered?",
            "How much do prescription drugs cost?",
            "Does the plan cover telehealth?",
            "What's covered for emergency room visits?",
            "Is vision care included?",
            "What mental health services are covered?",
        ]
        
        selected_sample = st.selectbox(
            "Or choose a sample question:",
            [""] + sample_questions,
            key="sample_selector"
        )
        
        query = st.text_input(
            "Type your question here:",
            value=selected_sample,
            placeholder="e.g., Does this plan cover gym membership?",
            label_visibility="collapsed"
        )
        
        search_button = st.button("🔎 Search", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("💡 Tips")
        st.info("""
        **Ask naturally!** Examples:
        - "Is dental included?"
        - "Copay for specialists?"
        - "What's covered for diabetes?"
        - "Compare gym benefits"
        """)
    
    # Search results
    if search_button and query:
        with st.spinner("🔄 Searching through plans..."):
            time.sleep(0.5)  # UX: brief pause for perceived processing
            
            # Apply filters
            plan_f = None if plan_filter == "All Plans" else plan_filter
            cat_f = None if category_filter == "All Categories" else category_filter
            
            results = retriever.search(
                query, 
                top_k=num_results,
                plan_filter=plan_f,
                category_filter=cat_f
            )
        
        # Display results
        st.divider()
        st.header("📋 Search Results")
        
        if not results:
            st.warning("😕 No results found. Try rephrasing your question or adjusting filters.")
        else:
            st.success(f"✅ Found {len(results)} relevant benefits!")
            
            # Display each result
            for i, result in enumerate(results, 1):
                with st.container():
                    # Result card
                    st.markdown(f"""
                    <div class="plan-card">
                        <h3 style='color: #1f77b4; margin-bottom: 0.5rem;'>
                            {i}. {result['plan_name']}
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    
                    with col_a:
                        st.markdown(f"""
                        <div class="benefit-text">
                            {result['text']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        similarity_pct = result['similarity_score'] * 100
                        st.markdown(f"""
                        <div class="similarity-score">
                            <strong>Relevance:</strong><br>
                            {similarity_pct:.1f}%
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_c:
                        st.markdown(f"""
                        <div class="category-badge">
                            {result['category'].replace('_', ' ').title()}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.divider()
    
    # Comparison feature
    st.divider()
    st.header("⚖️ Compare Plans")
    
    st.write("Compare how different plans handle a specific benefit:")
    
    col_compare_1, col_compare_2 = st.columns([3, 1])
    
    with col_compare_1:
        compare_query = st.text_input(
            "Benefit to compare:",
            placeholder="e.g., gym membership, prescription drugs",
            label_visibility="collapsed"
        )
    
    with col_compare_2:
        compare_button = st.button("Compare Plans", use_container_width=True)
    
    if compare_button and compare_query:
        with st.spinner("🔄 Comparing plans..."):
            comparison = retriever.compare_plans(compare_query, retriever.list_plans())
        
        st.subheader(f"📊 Comparison: {compare_query}")
        
        # Create columns for each plan
        plan_cols = st.columns(len(comparison['comparison']))
        
        for idx, (plan_name, results) in enumerate(comparison['comparison'].items()):
            with plan_cols[idx]:
                st.markdown(f"**{plan_name}**")
                
                if results:
                    result = results[0]  # Top result
                    st.info(result['description'])
                    st.caption(f"Relevance: {result['similarity_score']*100:.0f}%")
                else:
                    st.warning("No information found")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🏥 Healthcare Benefits Navigator • Built with Streamlit & AI</p>
        <p style='font-size: 0.9rem;'>
            Powered by Sentence Transformers & FAISS Vector Search
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()