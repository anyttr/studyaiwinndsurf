from flask import jsonify, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from src import app
from src.services import file_processor
from src.services.concept_extractor import ConceptExtractor
from src.services.visualizer import Visualizer
from src.services.difficulty_assessor import DifficultyAssessor
from src.services.summarizer import Summarizer

# Initialize services
concept_extractor = ConceptExtractor()
visualizer = Visualizer()
difficulty_assessor = DifficultyAssessor()
summarizer = Summarizer()

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure visualizations folder
VISUALIZATIONS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'visualizations')
if not os.path.exists(VISUALIZATIONS_FOLDER):
    os.makedirs(VISUALIZATIONS_FOLDER)

@app.route('/')
def index():
    """Render the upload page"""
    return render_template('upload.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)

        # Process the file
        result = file_processor.process_file(file_path)
        
        # Extract concepts if it's a text file
        if result['type'] == 'text':
            # Get language from request or default to English
            language = request.form.get('language', 'en')
            
            # Extract concepts
            concepts = concept_extractor.extract_concepts(result['content'], language)
            result['concepts'] = concepts
            
            # Generate visualizations
            viz_filename = f"{os.path.splitext(filename)[0]}_mindmap.html"
            viz_path = os.path.join(VISUALIZATIONS_FOLDER, viz_filename)
            mind_map = visualizer.create_mind_map(concepts, os.path.splitext(filename)[0])
            visualizer.save_visualization(mind_map, viz_path)
            
            # Generate knowledge graph
            graph = concept_extractor.generate_knowledge_graph(concepts)
            graph_viz = visualizer.create_knowledge_graph(graph)
            graph_filename = f"{os.path.splitext(filename)[0]}_knowledge_graph.html"
            graph_path = os.path.join(VISUALIZATIONS_FOLDER, graph_filename)
            visualizer.save_visualization(graph_viz, graph_path)
            
            # Add visualization paths to result
            result['visualizations'] = {
                'mind_map': f"/static/visualizations/{viz_filename}",
                'knowledge_graph': f"/static/visualizations/{graph_filename}"
            }
            
            # Assess difficulty
            result['difficulty_assessment'] = difficulty_assessor.assess_difficulty(result['content'], language)
            
            # Generate summaries
            result['summaries'] = {
                'paragraph': summarizer.generate_summary(result['content'], language, summary_type='paragraph'),
                'bullet_points': summarizer.generate_summary(result['content'], language, summary_type='bullet_points')
            }
        
        # Clean up the uploaded file after processing
        os.remove(file_path)
        
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze provided text content"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    try:
        text = data['text']
        language = data.get('language', 'en')

        # Extract concepts
        concepts = concept_extractor.extract_concepts(text, language)
        
        # Generate visualizations
        viz_filename = f"analysis_{hash(text)}_mindmap.html"
        viz_path = os.path.join(VISUALIZATIONS_FOLDER, viz_filename)
        mind_map = visualizer.create_mind_map(concepts, "Text Analysis")
        visualizer.save_visualization(mind_map, viz_path)
        
        # Generate knowledge graph
        graph = concept_extractor.generate_knowledge_graph(concepts)
        graph_viz = visualizer.create_knowledge_graph(graph)
        graph_filename = f"analysis_{hash(text)}_knowledge_graph.html"
        graph_path = os.path.join(VISUALIZATIONS_FOLDER, graph_filename)
        visualizer.save_visualization(graph_viz, graph_path)

        result = {
            'concepts': concepts,
            'visualizations': {
                'mind_map': f"/static/visualizations/{viz_filename}",
                'knowledge_graph': f"/static/visualizations/{graph_filename}"
            },
            'difficulty_assessment': difficulty_assessor.assess_difficulty(text, language),
            'summaries': {
                'paragraph': summarizer.generate_summary(text, language, summary_type='paragraph'),
                'bullet_points': summarizer.generate_summary(text, language, summary_type='bullet_points')
            }
        }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
