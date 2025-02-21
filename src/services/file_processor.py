import os
from werkzeug.utils import secure_filename
import magic
import pytesseract
from PIL import Image
import speech_recognition as sr
from pdf2image import convert_from_path
import docx
import PyPDF2
import mimetypes

ALLOWED_EXTENSIONS = {
    'text': {'txt', 'doc', 'docx', 'pdf'},
    'image': {'png', 'jpg', 'jpeg'},
    'audio': {'mp3', 'wav', 'm4a'},
    'video': {'mp4', 'avi', 'mov'}
}

def allowed_file(filename, file_type=None):
    """Check if file extension is allowed"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if file_type:
        return ext in ALLOWED_EXTENSIONS[file_type]
    return any(ext in extensions for extensions in ALLOWED_EXTENSIONS.values())

def process_file(file_path):
    """Process uploaded file based on its type"""
    filename = os.path.basename(file_path)
    if not allowed_file(filename):
        raise ValueError("File type not supported")

    # Detect file type using python-magic
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)

    if file_type.startswith('text') or filename.endswith(('.doc', '.docx', '.pdf')):
        return process_text(file_path)
    elif file_type.startswith('image'):
        return process_image(file_path)
    elif file_type.startswith('audio'):
        return process_audio(file_path)
    elif file_type.startswith('video'):
        return process_video(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def process_text(file_path):
    """Process text files"""
    ext = os.path.splitext(file_path)[1].lower()
    content = ""

    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        elif ext == '.docx':
            doc = docx.Document(file_path)
            content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif ext == '.pdf':
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                content = '\n'.join([page.extract_text() for page in pdf_reader.pages])
        
        return {
            "type": "text",
            "content": content[:1000],  # Return first 1000 chars for preview
            "length": len(content)
        }
    except Exception as e:
        raise ValueError(f"Error processing text file: {str(e)}")

def process_image(file_path):
    """Process image files using OCR"""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='eng+ron')  # Support both English and Romanian
        return {
            "type": "image",
            "text_content": text,
            "dimensions": image.size
        }
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

def process_audio(file_path):
    """Process audio files"""
    recognizer = sr.Recognizer()
    
    try:
        # Convert audio to WAV if necessary
        if not file_path.lower().endswith('.wav'):
            # TODO: Implement audio format conversion
            pass

        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            try:
                # Try both English and Romanian
                text_en = recognizer.recognize_google(audio, language='en-US')
                text_ro = recognizer.recognize_google(audio, language='ro-RO')
                
                return {
                    "type": "audio",
                    "transcription": {
                        "english": text_en,
                        "romanian": text_ro
                    }
                }
            except sr.UnknownValueError:
                return {
                    "type": "audio",
                    "error": "Could not understand audio"
                }
            except sr.RequestError:
                return {
                    "type": "audio",
                    "error": "Could not request results"
                }
    except Exception as e:
        raise ValueError(f"Error processing audio: {str(e)}")

def process_video(file_path):
    """Process video files"""
    try:
        # TODO: Implement video processing with frame extraction and audio transcription
        return {
            "type": "video",
            "status": "Video processing not yet implemented",
            "file_info": {
                "size": os.path.getsize(file_path),
                "path": os.path.basename(file_path)
            }
        }
    except Exception as e:
        raise ValueError(f"Error processing video: {str(e)}")
