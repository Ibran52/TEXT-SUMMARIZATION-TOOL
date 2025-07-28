# Text Summarization Tool 📝

A powerful and user-friendly text summarization tool built with Streamlit and advanced transformer models. Generate concise, high-quality summaries from your text using state-of-the-art AI models.

## ✨ Features

- **Multiple AI Models**: Support for various transformer models (BART, T5, Pegasus)
- **Flexible Input Methods**: Text input, file upload, and URL extraction
- **Customizable Parameters**: Adjust summary length, beam search, and other settings
- **Text Analysis**: Comprehensive text metrics and keyword extraction
- **Modern UI**: Beautiful and intuitive Streamlit interface
- **Long Text Support**: Automatic chunking for processing large documents
- **Download Results**: Save summaries as text files

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd text-summarization-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

## 📋 Requirements

The tool requires the following main dependencies:

- **Streamlit**: Web application framework
- **Transformers**: Hugging Face transformer models
- **PyTorch**: Deep learning framework
- **NLTK**: Natural language processing
- **BeautifulSoup4**: Web scraping for URL input
- **Other utilities**: See `requirements.txt` for complete list

## 🎯 Usage

### Basic Usage

1. **Select Input Method**:
   - **Text Input**: Paste your text directly
   - **File Upload**: Upload TXT or MD files
   - **URL**: Extract text from web articles

2. **Configure Settings** (optional):
   - Choose your preferred AI model
   - Adjust summary length parameters
   - Modify beam search settings

3. **Generate Summary**:
   - Click the "Generate Summary" button
   - View results in the summary panel

4. **Analyze Results**:
   - Review summary statistics
   - Check text metrics
   - Extract key terms
   - Download the summary

### Advanced Features

#### Model Selection
Choose from various pre-trained models:
- `facebook/bart-large-cnn`: Best for news articles
- `facebook/bart-base`: Good balance of speed and quality
- `t5-base`: Versatile model for various text types
- `google/pegasus-xsum`: Optimized for extreme summarization

#### Custom Parameters
- **Maximum Length**: Control summary length (30-200 tokens)
- **Minimum Length**: Ensure minimum summary size
- **Number of Beams**: Adjust beam search for better quality
- **Sampling**: Enable for more diverse outputs

## 📊 Text Analysis Features

The tool provides comprehensive text analysis:

- **Word Count**: Total number of words
- **Sentence Count**: Number of sentences
- **Average Sentence Length**: Mean words per sentence
- **Unique Words**: Vocabulary size
- **Lexical Diversity**: Vocabulary richness measure
- **Key Terms**: Most important keywords

## 🏗️ Project Structure

```
text-summarization-tool/
├── src/
│   └── text_summarization_tool/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── configuration.py
│       ├── components/
│       │   ├── __init__.py
│       │   └── summarizer.py
│       └── utils/
│           ├── __init__.py
│           └── common.py
├── config/
│   └── config.yaml
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Configuration

The application uses a YAML configuration file (`config/config.yaml`) for:

- Model settings and parameters
- Text processing options
- UI configuration
- Directory paths

You can modify these settings to customize the tool's behavior.

## 🔧 Customization

### Adding New Models

To add support for new models:

1. Update the `get_available_models()` method in `summarizer.py`
2. Ensure the model supports summarization tasks
3. Test with your specific use case

### Modifying Text Processing

Edit the utility functions in `utils/common.py` to:
- Change text cleaning rules
- Modify chunking strategies
- Adjust keyword extraction algorithms

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Errors**:
   - Ensure stable internet connection for model download
   - Check available disk space
   - Verify PyTorch installation

2. **Memory Issues**:
   - Use smaller models for limited RAM
   - Reduce chunk size in configuration
   - Close other applications

3. **Performance Issues**:
   - Use GPU if available
   - Select faster models (e.g., `t5-small`)
   - Reduce beam search parameters

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure you have sufficient system resources

## 📈 Performance Tips

- **GPU Usage**: The tool automatically uses GPU if available
- **Model Selection**: Choose smaller models for faster processing
- **Text Length**: Very long texts are automatically chunked
- **Caching**: Models are cached to avoid reloading

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- Streamlit for the web framework
- NLTK for text processing utilities
- The open-source community for various libraries

---

**Happy Summarizing! 📝✨** 