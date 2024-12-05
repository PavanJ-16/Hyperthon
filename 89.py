import streamlit as st
import requests
from huggingface_hub import InferenceClient
import base64

client = InferenceClient(api_key="API key")
# Function to query the Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer API key"}
sarvamurl = "https://api.sarvam.ai/text-to-speech"
sarvamheaders = {
    "api-subscription-key": "731bcfac-aef2-4541-88ee-1dc114b017a4",
    "Content-Type": "application/json"
}
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# Add this at the beginning of your Streamlit app
st.markdown(
    """
    <style>
    body {
        background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKtoiXZoApJeMlv4qakPnWnASeKo5a-Vq1Lw&s');
        background-size: cover;
        background-position: center;
        color: white;  /* Change text color for better visibility */
    }
    .stButton {
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .stButton:hover {
        background-color: rgba(255, 255, 255, 0.2);  /* Change button color on hover */
        transform: scale(1.05);  /* Slightly enlarge button on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
st.title("Preborn Chat bot")

# Audio input widget
audio_value = st.audio_input("Record a voice message")
prompt = st.chat_input("Type something")

if prompt:
    st.markdown("User:")
    st.markdown(prompt)
    messages = [
	{
		"role": "user",
		"content": [
			{
				"type": "text",
				"text": prompt
			}
			
		]
	},
    {
		"role": "system",
		"content": [
			{
				"type": "text",
				"text": "You are a helpful AI agent assistant. You pretend to be like a dune character who's preborn and is thus very wise. Say only what u intend to say, do not bive any buildup statemments"
			}
			
		]
	}
]
    try:
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct", 
            messages=messages, 
            max_tokens=200,
            stream=True
        )
    except Exception as e:
        st.write("Error: Unable to create chat completion.")
        st.write(str(e))
        st.stop()  # Stop the execution of the Streamlit app
    st.write("Model:")
    
    message_placeholder = st.empty()
    full_response = ""
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            # Update the placeholder with the full response so far
            message_placeholder.markdown(full_response + "▌")
    # Remove the cursor and display the final response
    message_placeholder.markdown(full_response)
    prompt = None

if audio_value:
    # Save the uploaded audio file
    with open("uploaded_audio.flac", "wb") as f:
        f.write(audio_value.getbuffer())

    # Query the Hugging Face model with the uploaded audio
    output = query("uploaded_audio.flac")
    
    # Display the output from the model
    st.write("User:")
    st.write(output["text"])
    messages = [
	{
		"role": "user",
		"content": [
			{
				"type": "text",
				"text": output["text"]
			}
			
		]
	},
    {
		"role": "system",
		"content": [
			{
				"type": "text",
				"text": "You are a helpful AI agent assistant. You pretend to be like a dune character who's preborn and is thus very wise. Say only what u intend to say, do not bive any buildup statemments"
			}
			
		]
	}
]
    try:
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct", 
            messages=messages, 
            max_tokens=200,
            stream=True
        )
    except Exception as e:
        st.write("Error: Unable to create chat completion.")
        st.write(str(e))
        st.stop()  # Stop the execution of the Streamlit app
    st.write("Model:")
    
    message_placeholder = st.empty()
    full_response = ""
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            # Update the placeholder with the full response so far
            message_placeholder.markdown(full_response + "▌")
    # Remove the cursor and display the final response
    message_placeholder.markdown(full_response)
    payload = {
    "inputs": [full_response[:490]],
    "target_language_code": "hi-IN",
    "speaker": "amartya",
    "pitch": 0.6,
    "pace": 1,
    "loudness": 1,
    "enable_preprocessing": True,
    "model": "bulbul:v1",
    "speech_sample_rate": 8000
}
    response = requests.request("POST", sarvamurl, json=payload, headers=sarvamheaders)
    #print(response.json())
    audio_data = response.json()
    if "audios" in audio_data and audio_data["audios"]:
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_data["audios"][0])
        # Play the audio in Streamlit
        st.audio(audio_bytes, format="audio/wav", autoplay=True)
    audio_value = None
    prompt=None

