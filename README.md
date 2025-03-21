# EmpathAI

EmpathAI is an advanced AI system that combines visual emotion recognition, voice tone analysis, and natural language processing to provide personalized therapeutic support. The system leverages multimodal inputs to detect emotional states, retrieves relevant therapeutic techniques from a knowledge graph, and generates empathetic responses tailored to the user's emotional context.

## Key Features

- **Multimodal Emotion Recognition**
  - Visual analysis of facial expressions using computer vision
  - Audio analysis of voice tone and speech patterns
  - Text analysis of language content and sentiment

- **Therapeutic Knowledge Graph**
  - Structured database of evidence-based therapeutic techniques
  - Emotion-technique mappings based on psychological research
  - Contextual retrieval of relevant interventions

- **Personalized AI Responses**
  - Emotion-aware conversation generation
  - Adaptive response based on detected emotional states
  - Contextual therapeutic suggestions

- **Intuitive User Interface**
  - Real-time emotion visualization
  - Seamless integration of webcam and microphone
  - Beautiful and responsive design

- **Session Management**
  - Unique session IDs for each therapy conversation
  - Persistent sessions with sharable/bookmarkable URLs
  - Dynamic routing with clean URL structure (/session/{uuid})
  - Automatic session creation

## Technical Architecture

EmpathAI is built using a modern tech stack with clear separation of concerns:

### Frontend (Next.js/React)
- **UI Components**: Built with React and TypeScript
- **Styling**: TailwindCSS for responsive design
- **Animation**: Framer Motion for fluid transitions
- **Media Capture**: react-webcam and react-mic for camera/audio input
- **State Management**: React hooks and context for local state
- **Routing**: Next.js dynamic routes for session management
- **Markdown Support**: Rich text formatting in AI responses

### Backend (Python/FastAPI)
- **API Layer**: FastAPI for high-performance endpoints
- **Emotion Detection**:
  - Visual: TensorFlow/OpenCV for facial emotion recognition
  - Audio: Librosa/Wav2Vec for voice tone analysis
  - Text: Transformer models for sentiment analysis
- **Knowledge Graph**: Structured data of therapeutic techniques
- **Response Generation**: Contextual AI responses based on emotional inputs
- **Session Handling**: Support for session persistence and retrieval

### System Architecture Diagram

```
┌─────────────────┐     ┌─────────────────────────────────────┐
│                 │     │              Backend                │
│    Frontend     │     │                                     │
│  (Next.js/React)│     │  ┌─────────────┐  ┌──────────────┐  │
│                 │     │  │   Emotion   │  │  Knowledge   │  │
│  ┌───────────┐  │     │  │  Detection  │  │    Graph     │  │
│  │  Webcam   │  │     │  │  Pipeline   │  │              │  │
│  └───────────┘  │     │  │ ┌─────────┐ │  │ ┌──────────┐ │  │
│  ┌───────────┐  │     │  │ │ Visual  │ │  │ │Techniques│ │  │
│  │ Microphone│  │◄────┼──┼─│ Model   │ │  │ │Database  │ │  │
│  └───────────┘  │     │  │ └─────────┘ │  │ └──────────┘ │  │
│  ┌───────────┐  │     │  │ ┌─────────┐ │  │ ┌──────────┐ │  │
│  │ Text Input│  │     │  │ │ Audio   │ │  │ │ Emotion  │ │  │
│  └───────────┘  │     │  │ │ Model   │ │  │ │ Mapping  │ │  │
│  ┌───────────┐  │     │  │ └─────────┘ │  │ └──────────┘ │  │
│  │  Emotion  │  │     │  │ ┌─────────┐ │  └──────────────┘  │
│  │ Visualizer│  │     │  │ │ Text    │ │  ┌──────────────┐  │
│  └───────────┘  │     │  │ │ Model   │ │  │   Response   │  │
│  ┌───────────┐  │     │  │ └─────────┘ │  │  Generator   │  │
│  │  Therapy  │  │     │  └─────────────┘  │              │  │
│  │  Session  │  │     │                   │              │  │
│  └───────────┘  │     │                   │              │  │
│                 │     │                   │              │  │
└────────┬────────┘     └───────────────────┬──────────────┘  │
         │                                  │                 │
         └──────────────┬──────────────────┘                 │
                        │                                    │
                ┌───────▼────────┐                           │
                │  REST API      │                           │
                │                │                           │
                └────────────────┘                           │
                                                            │
                                                            │
                                                            │
                                                            │
┌───────────────────────────────────────────────────────────┘
│
│       ┌─────────────────────────────────────────┐
└───────►       Production Deployment             │
        │  (Docker + AWS/GCP + CI/CD Pipeline)    │
        └─────────────────────────────────────────┘
```

## Installation and Setup

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- npm or yarn
- pip

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Implementation Highlights

### Emotion Detection

The system integrates three types of emotion detection:

1. **Visual Emotion Recognition**
   - Uses a CNN model trained on facial expression datasets
   - Processes webcam frames in real-time to detect emotions
   - Maps facial features to 7 core emotional states

2. **Voice Tone Analysis**
   - Extracts acoustic features like MFCC, chroma, and pitch
   - Analyzes speaking patterns, rhythm, and intonation
   - Detects emotional undertones in speech

3. **Text Analysis**
   - Utilizes transformer-based models for semantic understanding
   - Performs sentiment analysis and emotion classification
   - Extracts emotional context from user messages

### Knowledge Graph

The therapeutic knowledge graph connects:
- Emotional states (nodes)
- Therapeutic techniques (nodes)
- Effectiveness relationships (edges)
- Contextual factors (properties)

This structured approach allows the system to recommend appropriate interventions based on detected emotional states.

### Response Generation

The response generation system combines:
- Detected emotions from all three modalities
- Relevant therapeutic techniques from the knowledge graph
- Contextual information from the conversation history

The result is personalized, empathetic responses that address the user's emotional needs.

### Session Management

The system implements a RESTful approach to therapy sessions:
- Each therapy session is assigned a unique UUID
- Sessions are accessible via clean URLs (/session/{uuid})
- The homepage redirects to new sessions when "Start Therapy Session" is clicked
- Session IDs are included in API requests to enable future persistence
- Session URLs can be bookmarked or shared for continuity of care

## Ethical Considerations

EmpathAI is designed with strong ethical principles:

- **Privacy**: All processing happens locally where possible; data is not stored longer than necessary
- **Transparency**: Users are informed about how their data is used and what the system can/cannot do
- **Boundaries**: Clear disclaimer that this is a supportive tool, not a replacement for professional therapy
- **Inclusivity**: Designed to work across diverse demographics and emotional expressions

## Project Status

This project is under active development.

## License

This project is licensed under the MIT License - see the LICENSE file for details.