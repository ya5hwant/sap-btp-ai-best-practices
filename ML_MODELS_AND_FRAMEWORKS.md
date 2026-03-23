# ML Models & Open Source Frameworks - Interview Guide

## How to Use This Document

This document is your reference for answering: **"Which ML models and frameworks would you use for this?"**

You'll be asked follow-up questions like:
- "Why that model instead of X?"
- "What's the trade-off?"
- "Why not use deep learning?"
- "Is there an open source alternative?"

This guide shows you the trade-offs and helps you defend your choices.

---

# Part 1: Model Categories & Selection Guide

## Supervised Learning (You have labeled training data)

### Classification Models

#### 1. Logistic Regression
**What it does:** Binary or multi-class classification with probability outputs

**Pros:**
- ✅ Interpretable (can explain why a prediction was made)
- ✅ Fast to train and predict
- ✅ Works well with tabular data
- ✅ Requires little training data

**Cons:**
- ❌ Assumes linear relationships
- ❌ Not great with complex patterns

**When to use:**
- Binary classification with clear decision boundaries
- When interpretability is critical (compliance, credit decisions)
- When you have limited training data (<1000 samples)

**Open Source:**
- `scikit-learn.LogisticRegression`
- `statsmodels.logit`

**Use Cases:**
- Email prioritization (urgent vs. non-urgent)
- Order approval (approve vs. deny)

---

#### 2. Random Forest
**What it does:** Ensemble of decision trees for classification/regression

**Pros:**
- ✅ Handles non-linear relationships
- ✅ Works with mixed data types (numeric + categorical)
- ✅ Built-in feature importance (explains which features matter)
- ✅ Relatively fast
- ✅ Good with unbalanced datasets

**Cons:**
- ❌ Less interpretable than logistic regression
- ❌ Can overfit if not tuned
- ❌ Memory intensive for large datasets

**When to use:**
- Tabular data with complex patterns
- When you need feature importance
- When you have balanced or slightly unbalanced data

**Open Source:**
- `scikit-learn.RandomForest`
- `xgboost.XGBClassifier` (often better than RF)
- `catboost.CatBoostClassifier` (best for categorical features)

**Use Cases:**
- Fraud detection (binary: fraud vs. legitimate)
- Customer churn prediction
- Lead scoring in sales

---

#### 3. Gradient Boosting (XGBoost, LightGBM, CatBoost)
**What it does:** Sequential ensemble of trees (each tree corrects previous errors)

**Pros:**
- ✅ State-of-the-art performance on tabular data
- ✅ Handles imbalanced data well
- ✅ Fast training
- ✅ Feature importance included
- ✅ Works with mixed data types

**Cons:**
- ❌ Hyperparameter tuning required
- ❌ More complex than Random Forest
- ❌ Black-box (less interpretable)

**When to use:**
- You're competing in Kaggle-style competitions
- You have clean tabular data and want best accuracy
- You have imbalanced datasets (fraud, rare events)

**Open Source:**
- `xgboost.XGBClassifier` (most popular)
- `lightgbm.LGBMClassifier` (faster, memory efficient)
- `catboost.CatBoostClassifier` (best with categorical features)

**Use Cases:**
- Credit risk scoring
- Sales forecasting
- Vendor scoring (multi-dimensional)

**Interview Tip:**
"I'd start with Random Forest because it's simple and interpretable. If performance isn't good enough, I'd move to XGBoost for the marginal gains."

---

#### 4. Support Vector Machine (SVM)
**What it does:** Finds optimal boundary between classes in high-dimensional space

**Pros:**
- ✅ Works well in high-dimensional spaces
- ✅ Memory efficient
- ✅ Good generalization
- ✅ Works with kernels for non-linear problems

**Cons:**
- ❌ Slow to train on large datasets (>100k samples)
- ❌ Hard to interpret
- ❌ Requires feature scaling
- ❌ Hyperparameter tuning difficult

**When to use:**
- High-dimensional text/image features
- When you have <100k training samples
- When computational efficiency matters

**Open Source:**
- `scikit-learn.SVC`
- `libsvm`

**Use Cases:**
- Text classification (e.g., email spam/ham)
- Document categorization

---

### Regression Models

#### 1. Linear Regression
**What it does:** Predicts continuous value (price, quantity, time)

**Pros:**
- ✅ Interpretable
- ✅ Fast
- ✅ Good baseline

**Cons:**
- ❌ Assumes linear relationship
- ❌ Sensitive to outliers

**When to use:**
- Simple predictions (e.g., order value based on customer history)
- Baseline model to beat

**Open Source:**
- `scikit-learn.LinearRegression`

---

#### 2. Polynomial Regression
**What it does:** Linear regression with polynomial features (x², x³, etc.)

**Pros:**
- ✅ More flexible than linear
- ✅ Still interpretable

**Cons:**
- ❌ Can overfit
- ❌ Hard to choose polynomial degree

**When to use:**
- You see curved relationships in data

**Open Source:**
- `scikit-learn.preprocessing.PolynomialFeatures` + LinearRegression

---

#### 3. Gradient Boosting for Regression
**What it does:** XGBoost/LightGBM for predicting continuous values

**Pros:**
- ✅ Best accuracy on tabular data
- ✅ Handles non-linear relationships
- ✅ Built-in feature importance

**When to use:**
- Production forecasting
- Demand prediction
- Price optimization

**Open Source:**
- `xgboost.XGBRegressor`
- `lightgbm.LGBMRegressor`

**Use Cases:**
- Sales forecasting
- Delivery time prediction
- Cost estimation

---

## Unsupervised Learning (No labeled data)

### Clustering Models

#### 1. K-Means
**What it does:** Partitions data into K clusters based on similarity

**Pros:**
- ✅ Simple and fast
- ✅ Interpretable (cluster centers are actual data points)
- ✅ Works with any data type

**Cons:**
- ❌ Need to specify K (number of clusters) upfront
- ❌ Sensitive to outliers
- ❌ Assumes spherical clusters

**When to use:**
- Customer segmentation
- Document grouping
- Quick exploration of data

**Open Source:**
- `scikit-learn.KMeans`
- `sklearn.cluster.MiniBatchKMeans` (for large datasets)

**Use Cases:**
- Vendor clustering by cost/lead time
- Customer segmentation

---

#### 2. DBSCAN
**What it does:** Density-based clustering (finds clusters of arbitrary shape)

**Pros:**
- ✅ Doesn't need to specify number of clusters
- ✅ Finds outliers naturally
- ✅ Works with non-spherical clusters

**Cons:**
- ❌ Hard to tune parameters (epsilon, min_samples)
- ❌ Slower than K-Means

**When to use:**
- You expect outliers (anomalies)
- Cluster shapes are irregular
- You don't know how many clusters

**Open Source:**
- `scikit-learn.DBSCAN`

---

#### 3. Hierarchical Clustering
**What it does:** Creates tree of clusters (dendrogram)

**Pros:**
- ✅ Dendrogram shows relationships
- ✅ Flexible number of clusters

**Cons:**
- ❌ Slow (O(n³) complexity)
- ❌ Hard to interpret large dendrograms

**When to use:**
- Taxonomy exploration
- Understanding data relationships

**Open Source:**
- `scipy.cluster.hierarchy`

---

### Anomaly Detection

#### 1. Isolation Forest
**What it does:** Isolates anomalies by randomly selecting features and split values

**Pros:**
- ✅ No labeled data needed (unsupervised)
- ✅ Fast (linear complexity)
- ✅ Works with mixed data types
- ✅ Doesn't assume data distribution
- ✅ Built-in anomaly scores (not just binary classification)

**Cons:**
- ❌ Less interpretable than supervised models
- ❌ Struggles with high-dimensional data
- ❌ Needs domain expertise to set contamination parameter

**When to use:**
- Anomaly detection when you don't have labeled examples
- Fraud detection, outlier detection
- Fast, lightweight anomaly scoring

**Open Source:**
- `scikit-learn.IsolationForest`
- `pyod` (Isolation Forest, LOF, and 20+ other algorithms)

**Use Cases:**
- **Sales Order Anomalies** (fraud, unusual patterns)
- Network intrusion detection
- Sensor outliers in IoT

**Interview Tip:**
"I chose Isolation Forest because we don't have labeled training data of 'known anomalies', and Isolation Forest doesn't need it. It's also fast, which matters for real-time scoring."

---

#### 2. Local Outlier Factor (LOF)
**What it does:** Compares density around point to density of neighbors

**Pros:**
- ✅ Good at finding local anomalies
- ✅ Works in high-dimensional spaces better than IF

**Cons:**
- ❌ Slower (O(n²) complexity)
- ❌ Hard to use on new data (not a pure density model)

**When to use:**
- Anomalies that are only anomalous locally
- High-dimensional data

**Open Source:**
- `scikit-learn.LocalOutlierFactor`
- `pyod.LOF`

---

#### 3. One-Class SVM
**What it does:** Learns boundary around normal data

**Pros:**
- ✅ Good with high-dimensional data
- ✅ Kernel trick for non-linear boundaries

**Cons:**
- ❌ Slow on large datasets
- ❌ Hard to interpret
- ❌ Hyperparameter tuning difficult

**When to use:**
- High-dimensional data
- Categorical features with many categories

**Open Source:**
- `scikit-learn.OneClassSVM`

---

#### 4. Autoencoder (Deep Learning)
**What it does:** Neural network learns compressed representation of data; reconstruction error indicates anomaly

**Pros:**
- ✅ Works with high-dimensional data (images, text)
- ✅ Can learn complex patterns

**Cons:**
- ❌ Slow to train
- ❌ Needs lots of normal data
- ❌ Black-box (hard to interpret)

**When to use:**
- Image anomalies (defects in manufacturing)
- Complex time-series anomalies
- When you have GPU and large dataset

**Open Source:**
- `tensorflow.keras.Model` with Autoencoder architecture
- `pytorch` for custom autoencoders

---

## Time Series Models

### 1. ARIMA/SARIMA
**What it does:** Auto-Regressive Integrated Moving Average for time series forecasting

**Pros:**
- ✅ Interpretable
- ✅ Works well for simple trends
- ✅ Fast
- ✅ Statistical foundations

**Cons:**
- ❌ Assumes stationarity (trend/seasonality must be removed)
- ❌ Not great with complex patterns
- ❌ Hyperparameter tuning difficult

**When to use:**
- Simple time series (e.g., monthly sales)
- When you have clean historical data
- Baseline model

**Open Source:**
- `statsmodels.ARIMA`
- `pmdarima.auto_arima` (auto-tune parameters)

**Use Cases:**
- Sales forecasting
- Inventory demand prediction
- Server load forecasting

---

### 2. Prophet (Facebook)
**What it does:** Time series forecasting with trend, seasonality, and holiday effects

**Pros:**
- ✅ Handles seasonality well
- ✅ Robust to missing data
- ✅ Captures holiday effects
- ✅ Built-in uncertainty intervals

**Cons:**
- ❌ Black-box (Bayesian model)
- ❌ Slower than ARIMA
- ❌ Less suitable for very short term

**When to use:**
- Business metrics with strong seasonality (retail, SaaS)
- When you have holidays/events affecting data
- When you want confidence intervals

**Open Source:**
- `fbprophet.Prophet`

**Use Cases:**
- Revenue forecasting
- Staffing demand prediction
- Seasonal inventory planning

---

### 3. LSTM (Long Short-Term Memory) / RNN
**What it does:** Deep learning model for sequential data

**Pros:**
- ✅ Captures long-term dependencies
- ✅ Works with complex patterns
- ✅ Handles variable-length sequences

**Cons:**
- ❌ Slow to train
- ❌ Needs lots of data
- ❌ Black-box
- ❌ Requires GPU

**When to use:**
- Complex time series (stock prices, sensor data)
- When you have 1000s of historical points
- When simpler models underperform

**Open Source:**
- `tensorflow.keras.LSTM`
- `pytorch.nn.LSTM`

**Use Cases:**
- Stock price prediction
- Sensor anomaly detection
- Network traffic prediction

---

### 4. Transformer / Attention Models
**What it does:** Neural network with attention mechanism (parallel processing, better for long sequences)

**Pros:**
- ✅ Better than LSTM for long sequences
- ✅ Parallelizable (faster training)
- ✅ State-of-the-art results

**Cons:**
- ❌ Very slow to train
- ❌ Needs massive amounts of data
- ❌ Requires GPU/TPU
- ❌ Black-box

**When to use:**
- Only if simpler models fail and you have resources
- Large-scale time series (1M+ data points)

**Open Source:**
- `huggingface.transformers`
- `pytorch.nn.Transformer`

---

## Embedding & Semantic Models

### 1. Word2Vec / GloVe (Text Embeddings)
**What it does:** Converts words to dense vectors capturing semantic meaning

**Pros:**
- ✅ Fast
- ✅ Works well for simple text tasks
- ✅ Pre-trained models available

**Cons:**
- ❌ Doesn't understand context (same word always same embedding)
- ❌ Outdated (replaced by BERT/GPT)

**When to use:**
- Simple text clustering
- Fast similarity matching
- Baseline model

**Open Source:**
- `gensim.Word2Vec`
- Pre-trained: `gensim-data`

---

### 2. BERT (Bidirectional Encoder Representations from Transformers)
**What it does:** Deep transformer model understanding bidirectional context

**Pros:**
- ✅ Excellent text understanding
- ✅ Pre-trained on 100M+ documents
- ✅ Works for transfer learning (fine-tune for your task)
- ✅ Interpretable attention weights

**Cons:**
- ❌ Slow (2-3x slower than Word2Vec)
- ❌ Large model size (400MB+)
- ❌ Needs GPU for fine-tuning

**When to use:**
- Text classification (spam/ham, sentiment)
- Semantic similarity (find similar documents)
- Named entity recognition

**Open Source:**
- `huggingface.transformers.BertModel`
- Pre-trained: `huggingface.co/models?model_type=bert`

**Use Cases:**
- Email categorization
- Document clustering
- Semantic search

---

### 3. GPT-based Embeddings (OpenAI, Open Source Alternatives)
**What it does:** Modern embedding model from GPT

**Pros:**
- ✅ Best semantic understanding
- ✅ Handles nuance and context

**Cons:**
- ❌ Closed source (OpenAI API only for best models)
- ❌ Cost per API call
- ❌ Latency

**When to use:**
- Semantic search at scale
- Complex similarity matching
- When accuracy matters most

**Open Source:**
- `sentence-transformers` (many pre-trained models)
- `huggingface.co/sentence-transformers` (free alternatives)

**Use Cases:**
- **AI Capability Matcher** (semantic product matching)
- Vector search applications

**Interview Tip:**
"For embeddings, I'd use `sentence-transformers` for open source (free, works offline) or OpenAI embeddings for production (best quality, but costs scale)."

---

### 4. Vision Transformers / Image Embeddings
**What it does:** Converts images to vectors

**Pros:**
- ✅ Understands visual concepts
- ✅ Pre-trained on ImageNet/COCO

**Cons:**
- ❌ Computationally expensive
- ❌ Needs GPU

**When to use:**
- Image similarity
- Product recommendation by image

**Open Source:**
- `timm` (PyTorch Image Models)
- `torchvision.models`
- `huggingface.transformers.ViT`

---

## Explainability & Interpretability Models

### 1. SHAP (SHapley Additive exPlanations)
**What it does:** Explains prediction by calculating feature contributions

**Pros:**
- ✅ Works with ANY model
- ✅ Theoretically sound (game theory)
- ✅ Local explanations (per prediction)
- ✅ Global explanations (overall feature importance)

**Cons:**
- ❌ Computationally expensive (exponential in features)
- ❌ Can be hard to interpret for non-technical users

**When to use:**
- Financial decisions (credit scoring, fraud)
- Compliance/audit requirements
- Building stakeholder trust

**Open Source:**
- `shap.Explainer`
- Works with: XGBoost, LightGBM, Random Forest, deep learning

**Use Cases:**
- **Anomaly Detection** (why is this order anomalous?)
- **Credit Scoring** (why was credit approved/denied?)
- **Fraud Detection** (why flagged as fraud?)

---

### 2. LIME (Local Interpretable Model-agnostic Explanations)
**What it does:** Explains prediction by fitting local linear model

**Pros:**
- ✅ Works with any model
- ✅ Fast
- ✅ Easy to understand (local linear model)

**Cons:**
- ❌ Local only (doesn't explain global patterns)
- ❌ Less theoretically sound than SHAP
- ❌ Can be unstable

**When to use:**
- Quick explanations
- When SHAP is too slow
- Prototype/MVP stage

**Open Source:**
- `lime.LimeTabularExplainer`

---

### 3. Feature Importance
**What it does:** Shows which features matter most

**Pros:**
- ✅ Very fast
- ✅ Built-in for tree models

**Cons:**
- ❌ Global only (doesn't explain per-prediction)
- ❌ Doesn't show direction (positive/negative)

**When to use:**
- Quick baseline understanding
- Tree-based models (RF, XGBoost)

**Open Source:**
- `.feature_importances_` in scikit-learn models
- `xgboost.plot_importance`

---

## Open Source ML Frameworks & Libraries

### Core ML Libraries

| Library | Use Cases | Pros | Cons |
|---------|-----------|------|------|
| **scikit-learn** | Classification, regression, clustering | Easy to use, well-documented, fast | Limited to tabular data, not for deep learning |
| **XGBoost** | Best tabular classification/regression | State-of-the-art performance, fast, interpretable | Hyperparameter tuning required |
| **LightGBM** | Large-scale tabular data | Faster than XGBoost, memory efficient | Fewer tutorials than XGBoost |
| **CatBoost** | Categorical features | Handles categories natively, stable | Slower training than XGBoost |
| **TensorFlow** | Deep learning (any domain) | Ecosystem (Keras, TFLite, etc.), production-ready | Steeper learning curve |
| **PyTorch** | Research, computer vision, NLP | Intuitive, dynamic graphs, large community | Less production-ready than TensorFlow |
| **Transformers** | NLP, embeddings, LLM | SOTA models, pre-trained, transfer learning | Computational requirements, model size |
| **Prophet** | Time series forecasting | Seasonality handling, built-in uncertainty | Black-box, slower |
| **SHAP** | Model explainability | Works with any model, theoretically sound | Computationally expensive |
| **LIME** | Model explainability | Fast, any model | Local-only, less stable |

---

### Specialized Libraries

| Library | Purpose | Use Case |
|---------|---------|----------|
| **spaCy** | NLP (tokenization, NER, POS) | Email processing, document analysis |
| **NLTK** | NLP toolkit | Text preprocessing, simple NLP |
| **Gensim** | Topic modeling, word embeddings | Document clustering, semantic search |
| **PyMuPDF (fitz)** | PDF processing | Extract text from PDFs |
| **python-docx** | DOCX processing | Extract text from Word documents |
| **Tesseract** | Optical Character Recognition (OCR) | Extract text from scanned images |
| **OpenCV** | Computer vision | Image preprocessing, object detection |
| **Pillow** | Image processing | Resize, format conversion, basic transforms |
| **statsmodels** | Statistical modeling | ARIMA, regression, time series |
| **pmdarima** | Auto ARIMA | Automatic parameter tuning for ARIMA |
| **Plotly** | Interactive visualizations | Dashboards, exploratory analysis |
| **Streamlit** | Rapid UI development | Build ML dashboards quickly |
| **FastAPI** | REST API framework | Deploy models as APIs |
| **Pydantic** | Data validation | Ensure data quality in APIs |
| **SQLAlchemy** | ORM (database abstraction) | Work with HANA, PostgreSQL, MySQL |
| **pandas** | Data manipulation | ETL, data exploration |
| **NumPy** | Numerical computing | Matrix operations, fast math |
| **SciPy** | Scientific computing | Statistics, optimization, clustering |
| **scikit-image** | Image processing | Image analysis, preprocessing |

---

# Part 2: Use Case → Model Mapping

## Use Case 1: Post-Sales Chatbot
**Primary Model:** LLM (OpenAI GPT-4o or Claude via SAP GenAI Hub)

**Supporting ML:**
- Not really an ML problem (it's NLP + orchestration)
- Could add intent classification if needed: `scikit-learn.LogisticRegression` or BERT

**Why:**
"This is a conversational AI problem, not a traditional ML problem. We're using an LLM for multi-turn reasoning and tool orchestration."

---

## Use Case 2: Anomaly Detection in Sales Orders
**Primary Model:** Isolation Forest

**Why:**
- No labeled training data (unsupervised)
- Fast (real-time scoring needed)
- Works with mixed data types
- Interpretable via SHAP

**Alternatives & When to Use Them:**
- One-Class SVM: If high-dimensional features (>1000)
- LOF: If anomalies are locally dense
- Autoencoder: If features are images/complex (rare for sales orders)
- Supervised (RF/XGBoost): If you have labeled anomalies

**Supporting:**
- SHAP: Explain predictions ("why is this order anomalous?")
- LLM: Generate business-friendly explanations
- Feature Engineering: Critical for success (domain expertise needed)

**Open Source Stack:**
```python
from sklearn.ensemble import IsolationForest
import shap

model = IsolationForest(contamination=0.05)
predictions = model.predict(X_features)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_features)
```

---

## Use Case 3: Customer Credit Check
**Primary Model:** Rule Engine (Not ML!)

**Why:**
- Compliance requires explainability
- Policy changes frequently
- Auditable decision-making needed

**If You Need Scoring:**
- Logistic Regression: Interpretable credit scoring
- Random Forest: Feature importance for credit factors
- XGBoost: If you have historical credit decisions

**Supporting:**
- Document AI (extraction): SAP Document AI, not ML
- NLP for text documents: spaCy, Transformers
- No models for this specific use case—it's structured rules + data extraction

**Interview Tip:**
"Credit decisions are ruled-based for compliance. However, we could add ML for:
1. Scoring: Which features predict default risk?
2. Policy optimization: Are our thresholds optimal?
But the final decision is rules-based for audit trail."

---

## Use Case 4: Diagram-to-BPMN Converter
**Primary Model:** Vision LLM (Claude, GPT-4o, Gemini 2.5)

**Why:**
- Vision models excellent at understanding diagrams
- LLM generates structured BPMN XML
- No traditional ML model needed

**If You Want to Fine-Tune:**
- Vision Transformer: Limited benefit (pre-trained models already great)
- Custom CNN: Not worth the effort

**Open Source Alternatives:**
- No direct open source alternative for diagram understanding
- Could use ViT + custom training but not practical

**Interview Tip:**
"This is LLM-powered, not traditional ML. We're using vision capabilities, not training a model."

---

## Use Case 5: AI Log Analyzer
**Primary Model:** LLM (for intelligent analysis)

**Supporting ML:**
- Log clustering: K-Means or DBSCAN
- Anomaly detection: Isolation Forest (detect log spikes)
- Classification: BERT for error categorization

**Why LLM:**
- Understands SAP context
- Generates natural language explanations
- Provides remediation steps

**Open Source Stack:**
```python
# Error clustering
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5)
clusters = kmeans.fit_predict(log_embeddings)

# Anomaly detection for log spikes
from sklearn.ensemble import IsolationForest
spike_detector = IsolationForest(contamination=0.01)
anomalies = spike_detector.fit_predict(error_counts_timeseries)

# Classification
from transformers import pipeline
classifier = pipeline("zero-shot-classification")
category = classifier(log_message, ["database", "network", "application"])
```

---

## Use Case 6: Video Incident & Safety Monitoring
**Primary Model:** Vision LLM (Gemini 2.5 Pro)

**Supporting ML:**
- Frame extraction: OpenCV
- If you wanted to train custom model: YOLO for object detection
- Confidence scoring: Calibration curve

**Why:**
"This uses vision LLM for understanding complex scenes. We're not training models—we're using foundation models."

---

## Use Case 7: Intelligent Procurement Assistant
**Primary Model:** Pattern Matching (Regex) + Optional LLM

**Why:**
- Patterns: Fast, cheap, deterministic (80% of cases)
- LLM: For ambiguous cases (20% of cases)

**Supporting:**
- NLP: spaCy for text preprocessing
- Fuzzy matching: `fuzzywuzzy` for approximate string matching

**Open Source Stack:**
```python
import re
from fuzzywuzzy import fuzz

# Pattern matching
UNSPSC_PATTERN = r'\b([0-9]{8})\b'
codes = re.findall(UNSPSC_PATTERN, text)

# Fuzzy matching for validation
match_score = fuzz.token_set_ratio('ABC123', 'abc 123')

# Only use LLM for ambiguous cases
if match_score < 0.8:
    llm_result = llm.extract_commodity_code(text)
```

---

## Use Case 8: Purchase Order Extractor
**Primary Model:** Document AI (SAP Document AI - Not Open Source)

**Supporting ML:**
- Material mapping: LLM or if you have training data, use XGBoost
- Confidence scoring: Calibration curve

**If Open Source Alternative Needed:**
- LayoutLM: Document understanding transformer
- Donut: Document OCR and understanding
- PaddleOCR: OCR engine

**Open Source Stack (Alternative):**
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Use LayoutLM for document understanding
tokenizer = AutoTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
model = AutoModelForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")

# Or use Donut for end-to-end document processing
from transformers import DonutProcessor, VisionEncoderDecoderModel
processor = DonutProcessor.from_pretrained("naver-clova-ocr/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ocr/donut-base")
```

---

## Use Case 9: AI Capability Matcher (Vector Search)
**Primary Model:** Embedding Model + Vector Database

**Embedding Models:**
- Sentence-Transformers: Open source SOTA embeddings
- BERT: Good baseline
- OpenAI Embeddings: Best quality, costs money
- Custom LLM embeddings: Via SAP GenAI Hub

**Vector Database:**
- SAP HANA Vector: Integrated with SAP ecosystem
- Weaviate: Open source, fast vector search
- Milvus: Open source, scalable
- Pinecone: Cloud-based (paid)

**Optional Re-ranking:**
- LLM for business context

**Open Source Stack:**
```python
from sentence_transformers import SentenceTransformer

# Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')  # Free, fast, good quality
embeddings = model.encode(texts)

# Store and search in HANA vector tables
# OR use open source alternatives:
# from weaviate import Client  # Weaviate
# from milvus import connections  # Milvus
```

---

## Use Case 10: Email Agent
**Primary Model:** LLM (OpenAI GPT-4o or Claude)

**Supporting ML:**
- Intent classification: Could use BERT or simple Logistic Regression
- Entity extraction: spaCy Named Entity Recognition

**Why:**
"Multi-turn reasoning requires LLM. We might add NLP for entity extraction (order numbers, customer names) but primary model is LLM."

---

## Use Case 11: Vendor Selection Optimization
**Primary Model:** Scoring Algorithm (Not ML, but sometimes XGBoost for scoring)

**Why:**
- Business logic: Cost, lead time, quality, risk
- Multi-dimensional optimization: Weighted scoring
- Could use ML for: Historical decision patterns if available

**If Using ML:**
- XGBoost: Predict vendor performance based on features
- Random Forest: Feature importance for vendor evaluation

**Supporting:**
- Optimization libraries: `scipy.optimize`
- Linear programming: `pulp`, `cvxpy`

**Open Source Stack:**
```python
from scipy.optimize import minimize

# Multi-dimensional scoring
def vendor_score(vendor, weights):
    score = (weights['cost'] * vendor_cost_score +
             weights['lead_time'] * vendor_leadtime_score +
             weights['quality'] * vendor_quality_score)
    return score

# Optimize vendor selection
result = minimize(lambda x: -vendor_score(x, weights), 
                  x0=initial_vendor, 
                  method='SLSQP')
```

---

## Use Case 12: Touchless Transactions (GR & Invoice Bot)
**Primary Model:** None—This is Rule-Based Logic!

**Why:**
- Classification: 7 scenarios based on rules (tolerance thresholds)
- No ML needed—deterministic algorithm

**If You Had Historical Data:**
- XGBoost: Could predict approval likelihood
- But rules are simpler and more interpretable

**Open Source Stack:**
```python
# Pure rule-based classification
def classify_line(ir, po, gr):
    diff = ir - po
    pct_threshold = 0.05 * max(po, 0)
    amt_threshold = 250.0
    
    if ir <= po and gr == 0:
        return "SCENARIO_1"  # Full receipt confirmation
    elif ir > po and diff <= pct_threshold and diff <= amt_threshold:
        return "SCENARIO_2"  # Within tolerance
    else:
        return "SCENARIO_3"  # Needs investigation
    # ... more scenarios
```

---

# Part 3: Open Source Framework Comparisons

## When Asked: "What Open Source Framework Would You Use?"

### For Tabular Data Classification/Regression
**Answer:** "I'd use scikit-learn for baseline, then XGBoost if performance matters."

**Reasoning:**
```
Start: Logistic Regression (scikit-learn) - Simple, interpretable
      ↓ (if underperforms)
Try: Random Forest (scikit-learn) - Better accuracy, feature importance
      ↓ (if still underperforms)
Try: XGBoost - SOTA performance, built-in feature importance, handles imbalanced data
```

---

### For Explainability
**Answer:** "SHAP for production (theoretically sound), LIME for quick prototypes."

**Reasoning:**
- SHAP: Shapley values, game theory basis, works with any model
- LIME: Local explanations, fast, approximation-based
- Feature importance: Fast baseline (built-in to tree models)

---

### For NLP / Text
**Answer:** "spaCy for preprocessing, Transformers (BERT/GPT) for understanding."

**Reasoning:**
```
Simple tasks: spaCy (tokenization, NER, POS tagging)
           ↓
Complex tasks: Transformers (BERT for classification, GPT for generation)
           ↓
State-of-art: Large LLMs (via APIs or self-hosted)
```

---

### For Time Series
**Answer:** "Prophet for business metrics (seasonality, holidays), ARIMA for simple trends."

**Reasoning:**
- Prophet: Handles seasonality, built-in uncertainty, robust
- ARIMA: Statistical foundation, interpretable, fast
- LSTM: Only if complex patterns and lots of data

---

### For Anomaly Detection
**Answer:** "Isolation Forest—no labeled data needed, fast, interpretable."

**Alternative:** "If you have labeled anomalies, use XGBoost classifier."

---

### For Embeddings / Semantic Search
**Answer:** "sentence-transformers for open source, OpenAI for best quality."

**Reasoning:**
```
Cost-free: sentence-transformers (all-MiniLM-L6-v2 is good baseline)
        ↓ (if accuracy not sufficient)
Quality: OpenAI embeddings (costs $0.10 per million tokens)
        ↓ (if you want to self-host)
Self-hosted: Fine-tune BERT on your domain
```

---

## Interview Questions & Answers

### Q: "What's your experience with open source ML frameworks?"

**Answer:**
"I regularly use:
- **scikit-learn**: Classification, regression, clustering (mature, production-ready)
- **XGBoost**: Best tabular data performance, interpretable via feature importance
- **Transformers (HuggingFace)**: NLP and embeddings (state-of-art pre-trained models)
- **TensorFlow/PyTorch**: Deep learning when needed (not default choice for tabular)
- **SHAP**: Model explainability (critical for compliance)
- **spaCy**: NLP preprocessing (fast, clean API)

I prefer mature, widely-adopted frameworks over cutting-edge because they're battle-tested and have large communities."

---

### Q: "Why would you choose XGBoost over Random Forest?"

**Answer:**
"Random Forest is my default for interpretability and speed. I'd move to XGBoost if:

1. **Accuracy matters**: XGBoost is 5-10% better on tabular data
2. **Imbalanced data**: XGBoost handles better
3. **Feature interactions**: XGBoost captures them better
4. **Training time acceptable**: XGBoost is slower (but parallelizable)

Trade-off: XGBoost needs hyperparameter tuning; Random Forest is easier. So I'd use:
- MVP: Random Forest (fast, interpretable)
- Production: XGBoost (marginal accuracy gain if ROI justifies)
"

---

### Q: "Why not deep learning for this?"

**Answer:**
"Deep learning is overkill for tabular data. I'd use deep learning only if:

1. **Images/video**: CNN or Vision Transformer
2. **Text/NLP**: Transformers (BERT/GPT)
3. **Time series (complex)**: LSTM/Attention
4. **Massive dataset**: (1M+ samples) where deep learning amortizes training cost
5. **Simpler models underperform**: Last resort

For sales order anomaly detection:
- Tabular features (order amount, customer history, discount)
- Unsupervised (no labeled data)
→ Isolation Forest is perfect. Deep learning would be slower and harder to interpret."

---

### Q: "Should I use TensorFlow or PyTorch?"

**Answer:**
"For production: TensorFlow (Keras API is simpler, TFLite for mobile, ecosystem)
For research: PyTorch (more Pythonic, dynamic graphs, researchers prefer it)

My choice: TensorFlow for production, PyTorch for experimentation.

But honestly: Try to avoid deep learning unless absolutely necessary. Simpler models are faster to train, easier to deploy, and easier to explain."

---

### Q: "How would you explain a model to non-technical stakeholders?"

**Answer:**
"SHAP + visualizations + natural language:

1. **SHAP summary plot**: Show top factors influencing predictions
2. **Force plot**: For specific prediction, show factor contributions
3. **Natural language**: 'Model recommended approval because: Customer has 5+ year history (important), Good payment record (important), Order amount reasonable (low importance).'

Example:
- SHAP says: Feature importance [0.45, 0.30, 0.15, 0.10]
- I translate: 'Credit approved because 45% due to payment history, 30% due to company age, 15% due to revenue, 10% other factors.'

This builds trust and enables stakeholders to challenge the model ('Why is payment history weighted 45%?')."

---

### Q: "How do you handle class imbalance?"

**Answer:**
"Depends on the scenario:

1. **Fraud detection (95% normal, 5% fraud)**:
   - Use XGBoost with `scale_pos_weight` parameter
   - Or Isolation Forest (unsupervised, doesn't care about imbalance)
   - Or SMOTE for synthetic oversampling

2. **Rare disease (99% healthy, 1% disease)**:
   - Threshold tuning: Instead of 0.5 cutoff, use 0.3 (prioritize recall)
   - Class weights in model
   - Anomaly detection approach (treat disease as anomaly)

3. **Which I'd recommend**:
   - First try: Isolation Forest (no tuning needed)
   - If not working: XGBoost with class weights
   - Last resort: SMOTE + oversampling

Code:
```python
from sklearn.ensemble import IsolationForest
model = IsolationForest(contamination=0.05)  # Expect 5% anomalies

# OR
from xgboost import XGBClassifier
model = XGBClassifier(scale_pos_weight=19)  # 1 fraud : 19 normal

# OR
from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy=0.5)
X_resampled, y_resampled = smote.fit_resample(X, y)
```"

---

### Q: "How do you know if your model is good?"

**Answer:**
"Three levels of evaluation:

1. **Metrics** (depends on problem):
   - Classification: Precision, Recall, F1 (not just accuracy!)
   - Regression: MAE, RMSE, R²
   - Ranking: NDCG, AUC
   - Anomaly: Precision-Recall curve (not ROC with imbalanced data)

2. **Business validation**:
   - Does model decision align with business logic?
   - Financial impact: Cost of false positive vs. false negative
   - Stakeholder review: Does recommendation make sense?

3. **Production monitoring**:
   - Model drift: Are inputs still similar to training?
   - Performance decay: Is accuracy still 95%?
   - User feedback: Are users overriding model decisions?

Example (Anomaly Detection):
```python
from sklearn.metrics import precision_recall_curve, auc

precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)
pr_auc = auc(recall, precision)

# Set threshold to get 80% recall (catch 80% of anomalies)
# Check false positive rate at that threshold
idx = np.argmax(recall >= 0.8)
threshold = thresholds[idx]
fpr = 1 - precision[idx]

# Accept only if fpr < 5% (we're okay with 5% false positives)
```"

---

# Part 4: Quick Reference Cheat Sheet

## "Which Model Should I Use?" Decision Tree

```
Do you have labeled training data?
├─ NO → Anomaly Detection
│   ├─ Isolation Forest (fast, default)
│   ├─ LOF (local anomalies)
│   └─ Autoencoder (images/complex data)
│
└─ YES → Supervised Learning
    │
    ├─ Problem is Classification?
    │  ├─ Binary? → Logistic Regression (fast) or XGBoost (best)
    │  └─ Multi-class? → Random Forest or XGBoost
    │
    ├─ Problem is Regression?
    │  ├─ Simple relationship? → Linear Regression
    │  └─ Complex pattern? → XGBoost or Random Forest
    │
    └─ Problem is Time Series?
       ├─ Simple trend? → ARIMA or Prophet
       └─ Complex pattern? → LSTM or Transformer
```

---

## Open Source Stack by Use Case

| Use Case | Recommended Stack | Why |
|----------|-------------------|-----|
| Fraud Detection | XGBoost + SHAP | Best performance + explainability |
| Log Analysis | K-Means (clustering) + LLM | Cluster errors + LLM for insights |
| Sales Forecast | Prophet or ARIMA | Handles seasonality, business metrics |
| Product Search | sentence-transformers + HANA vector search | Semantic matching, scalable |
| Text Classification | Transformers (BERT/RoBERTa) | SOTA for text understanding |
| Document Extraction | spaCy (NER) + custom rules | Fast extraction, domain-specific |
| Anomaly Detection | Isolation Forest + SHAP | Fast, interpretable, no labeled data |
| Recommendation | Collaborative filtering or embedding similarity | Industry standard |
| Customer Segmentation | K-Means or DBSCAN + PCA | Simple, interpretable clusters |
| Demand Forecast | XGBoost + feature engineering | Captures complex patterns |

---

## Cost vs. Performance Trade-off

```
Accuracy
   ^
   |     Neural Networks
   |    /
   |   / XGBoost
   |  /
   | / Random Forest
   |/___________
Logistic Regression
        Complexity →

Choose by:
- Simplicity: Logistic Regression
- Speed: Random Forest
- Accuracy: XGBoost
- Interpretability: Logistic Regression or Random Forest
- No labeled data: Isolation Forest
```

---

## Interview Closing Statement

**"When choosing a model, I optimize for:**
1. **Interpretability** - Can I explain why the model made this decision?
2. **Simplicity** - Is it the simplest model that works?
3. **Performance** - Does it solve the business problem?
4. **Scalability** - Can it handle production data volumes?
5. **Maintainability** - Can my team support it long-term?

I generally start with simple models (Logistic Regression, Random Forest) and move to complex models only if business value justifies it. Most production problems are solved by simple models with good feature engineering."

---

**You're now ready to discuss ML models and frameworks with confidence! 🚀**
