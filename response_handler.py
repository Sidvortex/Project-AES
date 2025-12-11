def get_emotion_aware_response(self, user_input, emotion_data):
    """Generate response considering user's emotional state"""
    emotion = emotion_data.get('primary_emotion', 'neutral')
    confidence = emotion_data.get('confidence', 0.0)
    
    # Adjust tone based on emotion
    if emotion == 'sad' and confidence > 0.6:
        prefix = "I sense you might be feeling down. "
        tone = "supportive"
    elif emotion == 'angry' and confidence > 0.6:
        prefix = "I understand this might be frustrating. "
        tone = "calm"
    elif emotion == 'happy' and confidence > 0.7:
        prefix = ""
        tone = "enthusiastic"
    else:
        prefix = ""
        tone = "neutral"
    
    # Generate response with adjusted tone
    response = self.generate_response(user_input, tone=tone)
    return prefix + response