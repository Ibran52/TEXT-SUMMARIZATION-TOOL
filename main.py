"""
Main Streamlit application for the Text Summarization Tool.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from text_summarization_tool.config.configuration import ConfigurationManager
from text_summarization_tool.components.summarizer import TextSummarizer
from text_summarization_tool.utils.common import (
    calculate_text_metrics, 
    extract_keywords, 
    validate_input_text
)

# Page configuration
st.set_page_config(
    page_title="Text Summarization Tool",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .summary-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #ff4444;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_summarizer():
    """Load the summarizer model (cached to avoid reloading)."""
    try:
        config = ConfigurationManager()
        config.create_directories()
        summarizer = TextSummarizer(config)
        return summarizer
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">📝 Text Summarization Tool</h1>', unsafe_allow_html=True)
    st.markdown("### Generate concise summaries from your text using advanced AI models")
    
    # Load summarizer
    summarizer = load_summarizer()
    if summarizer is None:
        st.error("Failed to load the summarization model. Please check your configuration.")
        return
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        available_models = summarizer.get_available_models()
        current_model = st.selectbox(
            "Select Model",
            available_models,
            index=available_models.index(summarizer.model_name)
        )
        
        if st.button("Change Model"):
            with st.spinner("Loading new model..."):
                try:
                    summarizer.change_model(current_model)
                    st.success(f"Model changed to {current_model}")
                except Exception as e:
                    st.error(f"Error changing model: {str(e)}")
        
        st.divider()
        
        # Custom parameters
        st.subheader("📊 Custom Parameters")
        
        max_length = st.slider(
            "Maximum Summary Length",
            min_value=30,
            max_value=200,
            value=130,
            help="Maximum number of tokens in the summary"
        )
        
        min_length = st.slider(
            "Minimum Summary Length",
            min_value=10,
            max_value=100,
            value=30,
            help="Minimum number of tokens in the summary"
        )
        
        num_beams = st.slider(
            "Number of Beams",
            min_value=1,
            max_value=8,
            value=4,
            help="Number of beams for beam search"
        )
        
        do_sample = st.checkbox(
            "Enable Sampling",
            value=False,
            help="Use sampling instead of greedy decoding"
        )
        
        # Text input method
        st.divider()
        st.subheader("📥 Input Method")
        input_method = st.radio(
            "Choose input method:",
            ["Text Input", "File Upload", "URL"]
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input Text")
        
        # Text input based on selected method
        if input_method == "Text Input":
            input_text = st.text_area(
                "Enter your text here:",
                height=300,
                placeholder="Paste your text here to generate a summary..."
            )
            
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload a text file:",
                type=['txt', 'md', 'docx'],
                help="Supported formats: .txt, .md, .docx"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.txt') or uploaded_file.name.endswith('.md'):
                        input_text = uploaded_file.getvalue().decode('utf-8')
                    else:
                        # For .docx files, you would need python-docx library
                        st.error("DOCX files are not supported yet. Please use TXT or MD files.")
                        input_text = ""
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                    input_text = ""
            else:
                input_text = ""
                
        else:  # URL method
            url = st.text_input("Enter URL:", placeholder="https://example.com/article")
            if url:
                try:
                    import requests
                    from bs4 import BeautifulSoup
                    
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract text from common article tags
                    article_text = ""
                    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                        article_text += tag.get_text() + " "
                    
                    input_text = article_text.strip()
                    st.success("Text extracted from URL successfully!")
                    
                except Exception as e:
                    st.error(f"Error extracting text from URL: {str(e)}")
                    input_text = ""
            else:
                input_text = ""
        
        # Custom parameters
        custom_params = {
            'max_length': max_length,
            'min_length': min_length,
            'num_beams': num_beams,
            'do_sample': do_sample
        }
        
        # Generate summary button
        if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
            if input_text.strip():
                with st.spinner("Generating summary..."):
                    result = summarizer.summarize_text(input_text, custom_params)
                    
                    if result['success']:
                        st.session_state.summary_result = result
                        st.session_state.input_text = input_text
                    else:
                        st.error(f"Error: {result['error']}")
            else:
                st.warning("Please enter some text to summarize.")
    
    with col2:
        st.header("📋 Summary")
        
        if 'summary_result' in st.session_state and st.session_state.summary_result['success']:
            result = st.session_state.summary_result
            
            # Display summary
            st.markdown('<div class="summary-box">', unsafe_allow_html=True)
            st.markdown("### Generated Summary:")
            st.write(result['summary'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display metadata
            metadata = result['metadata']
            st.subheader("📊 Summary Statistics")
            
            col_meta1, col_meta2 = st.columns(2)
            
            with col_meta1:
                st.metric("Original Length", f"{metadata['original_length']:,} chars")
                st.metric("Summary Length", f"{metadata['summary_length']:,} chars")
            
            with col_meta2:
                compression_ratio = metadata['compression_ratio']
                st.metric("Compression Ratio", f"{compression_ratio:.1%}")
                if 'chunks_processed' in metadata:
                    st.metric("Chunks Processed", metadata['chunks_processed'])
            
            # Model information
            st.info(f"**Model used:** {metadata['model_used']}")
            
            # Download summary
            st.download_button(
                label="💾 Download Summary",
                data=result['summary'],
                file_name="summary.txt",
                mime="text/plain"
            )
            
        else:
            st.info("Enter text and click 'Generate Summary' to see results here.")
    
    # Text analysis section
    if 'input_text' in st.session_state and st.session_state.input_text:
        st.divider()
        st.header("📈 Text Analysis")
        
        input_text = st.session_state.input_text
        
        # Calculate metrics
        metrics = calculate_text_metrics(input_text)
        keywords = extract_keywords(input_text, top_k=10)
        
        col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
        
        with col_analysis1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Word Count", metrics['word_count'])
            st.metric("Sentence Count", metrics['sentence_count'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_analysis2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Sentence Length", f"{metrics['avg_sentence_length']:.1f} words")
            st.metric("Unique Words", metrics['unique_words'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_analysis3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Lexical Diversity", f"{metrics['lexical_diversity']:.3f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Keywords
        st.subheader("🔑 Key Terms")
        if keywords:
            keyword_tags = " ".join([f"`{keyword}`" for keyword in keywords])
            st.markdown(keyword_tags)
        else:
            st.info("No significant keywords found.")

if __name__ == "__main__":
    main() 