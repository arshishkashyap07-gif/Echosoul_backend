from emotion.bert_model import predict_emotion

def analyze_text(text: str):
    emotion, confidence = predict_emotion(text)
    return {
        "emotion": emotion,
        "confidence": confidence
    }
