import streamlit as st
import json
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config
from typing import Dict, List, Optional, Union, Tuple
import os
from gtts import gTTS
import os
from io import BytesIO

# Helper Functions
def display_shloka_content(shloka, chapter_num):
    """Helper function to display shloka content with audio controls"""
    # Sanskrit Text Section
    shloka_text = shloka.get('sanskrit_text', '')
    if shloka_text:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔊 Sanskrit", 
                       key=f"sanskrit_theme_{chapter_num}_{shloka['shloka_number']}"):
                audio_file = generate_audio(
                    shloka_text,
                    filename=f"sanskrit_{chapter_num}_{shloka['shloka_number']}.mp3",
                    lang='hi'
                )
                st.audio(audio_file, format="audio/mp3")
        with col2:
            st.markdown("**Sanskrit Text:**")
            st.text(shloka_text)
    
    # English sections
    if 'transliteration' in shloka:
        # Create English text without transliteration
        english_text = f"Meaning: {shloka.get('meaning', '')}\n\n"
        if 'interpretation' in shloka:
            english_text += f"Interpretation: {shloka['interpretation']}\n\n"
        if 'life_application' in shloka:
            english_text += f"Life Application: {shloka['life_application']}"
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔊 Explanation", 
                       key=f"english_theme_{chapter_num}_{shloka['shloka_number']}"):
                audio_file = generate_audio(
                    english_text,
                    filename=f"english_{chapter_num}_{shloka['shloka_number']}.mp3",
                    lang='en'
                )
                st.audio(audio_file, format="audio/mp3")
        
        # Display text sections
        with col2:
            if 'transliteration' in shloka:
                st.markdown("**Transliteration:**")
                st.write(shloka['transliteration'])
            
            st.markdown("**Meaning:**")
            st.write(shloka.get('meaning', ''))
            
            if 'interpretation' in shloka:
                st.markdown("**Interpretation:**")
                st.write(shloka['interpretation'])
            
            if 'life_application' in shloka:
                st.markdown("**Life Application:**")
                st.write(shloka['life_application'])

def generate_audio(text: str, filename: str = "shloka.mp3", lang: str = 'hi'):
    """Generate audio from text with language support and loading spinner"""
    with st.spinner('Generating audio, please wait...'):
        if lang == 'en':
            lang = 'en-IN'  # Use Indian English accent
        
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang=lang)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes

def create_node(id: str, label: str, node_type: str) -> Node:
    """Helper function to create nodes with consistent styling"""
    type_to_style = {
        'problem': {'color': '#FFD700', 'size': 30, 'shape': 'dot'},
        'chapter': {'color': '#87CEEB', 'size': 25, 'shape': 'dot'},
        'shloka': {'color': '#F08080', 'size': 20, 'shape': 'dot'},
        'theme': {'color': '#90EE90', 'size': 35, 'shape': 'dot'},
        'character': {'color': '#FFD700', 'size': 30, 'shape': 'dot'},
        'event': {'color': '#87CEEB', 'size': 25, 'shape': 'dot'}
    }
    
    style = type_to_style.get(node_type, {'color': '#FFFFFF', 'size': 25, 'shape': 'dot'})
    
    return Node(
        id=id,
        label=label,
        size=style['size'],
        shape=style['shape'],
        color=style['color']
    )

def create_edge(source: str, target: str, label: str = "") -> Edge:
    """Helper function to create edges with consistent styling"""
    return Edge(
        source=source,
        target=target,
        label=label,
        color="#666666",
        smooth={'type': 'curvedCW', 'roundness': 0.2}
    )

def create_agraph_config() -> Config:
    """Create consistent agraph configuration for graph visualization"""
    config = Config(
        width="100%",
        height=600,
        directed=True,
        physics={
            'enabled': True,
            'solver': 'forceAtlas2Based',
            'forceAtlas2Based': {
                'gravitationalConstant': -2000,
                'centralGravity': 0.5,
                'springLength': 200,
                'springConstant': 0.05,
                'damping': 0.4,
                'avoidOverlap': 0.5
            },
            'stabilization': {
                'enabled': True,
                'iterations': 2000,
                'updateInterval': 25,
                'onlyDynamicEdges': False,
                'fit': True,
                'initialSteps': 1000
            },
            'minVelocity': 0.75,
            'maxVelocity': 30,
        },
        hierarchical=False,
        nodeHighlightBehavior=True,
        node={
            'labelProperty': 'label',
            'size': 500,
            'highlightStrokeColor': 'black',
            'scaling': {
                'min': 10,
                'max': 30
            }
        },
        link={
            'labelProperty': 'label',
            'renderLabel': True,
            'strokeWidth': 1.5,
            'smooth': {
                'enabled': True,
                'type': 'curvedCW'
            }
        },
        highlightColor="#F7A7A6",
        collapsible=True,
        layout={
            'hierarchical': False,
            'improvedLayout': True,
            'randomSeed': 42,
            'clusterThreshold': 150,
        },
        style={
            'border': '2px solid #ddd',
            'border-radius': '8px',
            'background': '#f8f9fa',
            'margin': '10px 0',
            'padding': '10px'
        }
    )
    return config

def show_about_section():
    """Display the enhanced About Project section with emojis and better styling"""
    st.sidebar.markdown("---")
    
    # Project Header with Emoji
    st.sidebar.markdown("""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;margin-bottom:20px;">
        <h2 style="color:#2c3e50;text-align:center;">🕉️ Bhagavad Gita Explorer</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    with st.sidebar.expander("✨ Key Features", expanded=True):
        st.markdown("""
        - 📖 **Chapter Topology**  
        - 🧠 **Wisdom Pathways**  
        - 🧘 **Philosophical Themes**  
        - 👥 **Character Relationships**  
        - 🔊 **Audio Recitation**  
        - 🌐 **Interactive Visualizations**
        """)
    
    # Technology Stack
    with st.sidebar.expander("🛠️ Built With", expanded=True):
        st.markdown("""
        - Python 🐍
        - Streamlit 🎈
        - NetworkX 📊
        - Graph Visualization 🕸️
        - gTTS 🔊
        """)
    
    # GitHub Link
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center;">
        <a href="https://github.com/divyaraj-vihol" target="_blank">
            <button style="background-color:#6e48aa;color:white;padding:10px 15px;border:none;border-radius:5px;cursor:pointer;">
                👨‍💻 View Code on GitHub
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Made by section
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center;font-size:14px;color:#666;">
        Made with ❤️ by <strong>Divyaraj Vihol</strong>
    </div>
    """, unsafe_allow_html=True)

class GitaGraphRAG:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.current_dir, 'data', 'bhagavad_gita_complete.json')
        self.data = self._load_data()
        self.G = nx.Graph()
        self.build_knowledge_graph()
        
    def _load_data(self) -> Optional[Dict]:
        """Load the Bhagavad Gita JSON data"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None
            
    def build_knowledge_graph(self) -> None:
        """Build the knowledge graph from the loaded data"""
        if not self.data:
            return
            
        # Add problem nodes first
        if 'problem_solutions_map' in self.data:
            for problem, details in self.data['problem_solutions_map'].items():
                problem_id = f"Problem_{problem}"
                self.G.add_node(problem_id,
                              type='problem',
                              name=problem,
                              description=details['description'])
                
                # Add references as edges to chapters/shlokas
                for ref in details['references']:
                    shloka_id = f"Shloka_{ref['chapter']}_{ref['shloka']}"
                    chapter_id = f"Chapter_{ref['chapter']}"
                    
                    # Add edges to both chapter and shloka
                    self.G.add_edge(problem_id, chapter_id)
                    self.G.add_edge(problem_id, shloka_id)
        
        # Add chapter nodes
        if 'chapters' in self.data:
            for chapter in self.data['chapters']:
                chapter_id = f"Chapter_{chapter['number']}"
                node_attrs = {
                    'type': 'chapter',
                    'name': chapter.get('name', ''),
                    'number': chapter.get('number', 0),
                    'summary': chapter.get('summary', ''),
                    'main_theme': chapter.get('main_theme', '')
                }
                self.G.add_node(chapter_id, **node_attrs)
                
                # Add shloka nodes
                for shloka in chapter.get('shlokas', []):
                    shloka_id = f"Shloka_{chapter['number']}_{shloka['shloka_number']}"
                    self.G.add_node(shloka_id,
                                  type='shloka',
                                  sanskrit_text=shloka.get('sanskrit_text', ''),
                                  meaning=shloka.get('meaning', ''),
                                  interpretation=shloka.get('interpretation', ''))
                    self.G.add_edge(chapter_id, shloka_id)

    def get_problem_solutions(self, problem: str) -> Optional[Dict]:
        """Get solutions for a specific problem"""
        if 'problem_solutions_map' in self.data:
            return self.data['problem_solutions_map'].get(problem)
        return None

    def get_shloka_by_reference(self, chapter: int, shloka: int) -> Optional[Dict]:
        """Get shloka details by chapter and shloka number"""
        if 'chapters' in self.data:
            chapter_data = next((ch for ch in self.data['chapters'] 
                               if ch['number'] == chapter), None)
            if chapter_data:
                return next((sh for sh in chapter_data.get('shlokas', [])
                           if sh['shloka_number'] == shloka), None)
        return None

    def visualize_chapter_graph(self, node_id: str) -> Tuple[List[Node], List[Edge]]:
        """Create agraph visualization of the graph for a specific node"""
        nodes = []
        edges = []
        seen_nodes = set()
        
        # Create subgraph for the selected node
        subgraph = nx.ego_graph(self.G, node_id, radius=1)
        
        # Add nodes
        for node in subgraph.nodes():
            if node not in seen_nodes:
                node_data = self.G.nodes[node]
                node_type = node_data['type']
                label = f"{node_data.get('name', '')} {node.split('_')[-1]}"
                
                nodes.append(create_node(node, label, node_type))
                seen_nodes.add(node)
        
        # Add edges
        for source, target in subgraph.edges():
            edges.append(create_edge(source, target))
        
        return nodes, edges

    def visualize_theme_relationships(self, selected_theme: str, related_chapters: list) -> Tuple[List[Node], List[Edge]]:
        """Create agraph visualization showing relationships between theme, chapters, and shlokas"""
        nodes = []
        edges = []
        seen_nodes = set()
        
        # Add theme node
        theme_id = f"Theme_{selected_theme}"
        nodes.append(create_node(theme_id, selected_theme, 'theme'))
        seen_nodes.add(theme_id)
        
        # Add related chapters and shlokas
        for chapter in related_chapters:
            chapter_id = f"Chapter_{chapter['number']}"
            if chapter_id not in seen_nodes:
                nodes.append(create_node(
                    chapter_id,
                    f"Chapter {chapter['number']}: {chapter['name']}",
                    'chapter'
                ))
                seen_nodes.add(chapter_id)
                edges.append(create_edge(theme_id, chapter_id, "contains"))
            
            # Add relevant shlokas
            for shloka in chapter.get('shlokas', []):
                if any(kw.lower() in selected_theme.lower() for kw in shloka.get('keywords', [])):
                    shloka_id = f"Shloka_{chapter['number']}_{shloka['shloka_number']}"
                    if shloka_id not in seen_nodes:
                        nodes.append(create_node(
                            shloka_id,
                            f"Shloka {shloka['shloka_number']}",
                            'shloka'
                        ))
                        seen_nodes.add(shloka_id)
                        edges.append(create_edge(chapter_id, shloka_id, "contains"))
                        edges.append(create_edge(theme_id, shloka_id, "references"))
        
        return nodes, edges

    def display_chapter_insights(self):
        """Display chapter insights with character-centric relationships."""
        st.header("Ontology of Characters")

        chapters = self.data.get("chapters", [])
        if not chapters:
            st.error("No chapters found in the data.")
            return

        selected_chapter_num = st.radio(
            "Select Chapter",
            [chapter["number"] for chapter in chapters],
            format_func=lambda x: f"Chapter {x}",
            horizontal=True
        )

        selected_chapter = next(
            (chapter for chapter in chapters if chapter["number"] == selected_chapter_num), 
            None
        )
        if not selected_chapter:
            st.error("Invalid chapter selected.")
            return

        with st.expander(f"Chapter {selected_chapter['number']}: {selected_chapter['name']}"):
            st.markdown("### Summary")
            st.write(selected_chapter.get("summary", "No summary available."))

        st.markdown("### Character Relationship Graph")
        
        nodes = []
        edges = []
        seen_nodes = set()
        
        key_events = selected_chapter.get("key_events", [])
        for event in key_events:
            event_id = f"Event_{event['event']}"
            if event_id not in seen_nodes:
                nodes.append(create_node(event_id, event['event'], 'event'))
                seen_nodes.add(event_id)
            
            for char in event['characters']:
                char_id = f"Character_{char}"
                if char_id not in seen_nodes:
                    nodes.append(create_node(char_id, char, 'character'))
                    seen_nodes.add(char_id)
                edges.append(create_edge(char_id, event_id))
            
            for shloka_num in event['shlokas']:
                shloka_id = f"Shloka_{selected_chapter_num}_{shloka_num}"
                if shloka_id not in seen_nodes:
                    nodes.append(create_node(shloka_id, f"Shloka {shloka_num}", 'shloka'))
                    seen_nodes.add(shloka_id)
                edges.append(create_edge(event_id, shloka_id))

        st.markdown("### Character Details")
        
        unique_characters = set()
        for event in key_events:
            unique_characters.update(event['characters'])
        
        for char in unique_characters:
            with st.expander(f"{char}", expanded=False):
                char_info = next((c for c in selected_chapter.get('characters', []) 
                                if c['name'] == char), None)
                if char_info:
                    st.markdown("**Description:**")
                    st.write(char_info['description'])
                
                char_events = [event for event in key_events if char in event['characters']]
                
                if char_events:
                    st.markdown("**Associated Events and Teachings:**")
                    for event_index, event in enumerate(char_events):
                        st.markdown(f"### {event['event']}")
                        
                        for shloka_index, shloka_num in enumerate(event['shlokas']):
                            shloka = next((s for s in selected_chapter['shlokas'] 
                                        if s['shloka_number'] == shloka_num), None)
                            
                            if shloka:
                                st.markdown(f"#### Shloka {shloka_num}")
                                
                                shloka_text = shloka.get('sanskrit_text', '')
                                if shloka_text:
                                    col1, col2 = st.columns([1, 4])
                                    with col1:
                                        if st.button("🔊 Sanskrit", 
                                                   key=f"sanskrit_{selected_chapter_num}_{char}_{event_index}_{shloka_index}"):
                                            audio_file = generate_audio(
                                                shloka_text,
                                                filename=f"sanskrit_{selected_chapter_num}_{shloka_num}.mp3",
                                                lang='hi'
                                            )
                                            st.audio(audio_file, format="audio/mp3")
                                    with col2:
                                        st.markdown("**Sanskrit Text:**")
                                        st.text(shloka_text)
                                
                                if 'transliteration' in shloka:
                                    english_text = f"Meaning: {shloka.get('meaning', '')}\n\n"
                                    if 'interpretation' in shloka:
                                        english_text += f"Interpretation: {shloka['interpretation']}\n\n"
                                    if 'life_application' in shloka:
                                        english_text += f"Life Application: {shloka['life_application']}"
                                    
                                    col1, col2 = st.columns([1, 4])
                                    with col1:
                                        if st.button("🔊 Explanation", 
                                                   key=f"english_{selected_chapter_num}_{char}_{event_index}_{shloka_index}"):
                                            audio_file = generate_audio(
                                                english_text,
                                                filename=f"english_{selected_chapter_num}_{shloka_num}.mp3",
                                                lang='en'
                                            )
                                            st.audio(audio_file, format="audio/mp3")
                                    
                                    with col2:
                                        if 'transliteration' in shloka:
                                            st.markdown("**Transliteration:**")
                                            st.write(shloka['transliteration'])
                                        
                                        st.markdown("**Meaning:**")
                                        st.write(shloka['meaning'])
                                        
                                        if 'interpretation' in shloka:
                                            st.markdown("**Interpretation:**")
                                            st.write(shloka['interpretation'])
                                        
                                        if 'life_application' in shloka:
                                            st.markdown("**Life Application:**")
                                            st.write(shloka['life_application'])

                char_relationships = [
                    rel for rel in selected_chapter.get('character_relationships', [])
                    if char in rel['from'] or char in rel['to']
                ]
                
                if char_relationships:
                    st.markdown("**Character Relationships:**")
                    for rel in char_relationships:
                        st.markdown(f"- {rel['description']}")

        config = create_agraph_config()
        agraph(nodes=nodes, edges=edges, config=config)

def get_themes_from_chapters(data):
    """Extract all unique themes from chapters with their shloka counts"""
    theme_counts = {}
    for chapter in data['chapters']:
        themes = set()
        if 'main_theme' in chapter:
            themes.add(chapter['main_theme'])
        if 'philosophical_aspects' in chapter:
            themes.update(chapter['philosophical_aspects'])
        
        for theme in themes:
            if theme not in theme_counts:
                theme_counts[theme] = 0
            
            theme_counts[theme] += len([
                shloka for shloka in chapter.get('shlokas', [])
                if any(kw.lower() in theme.lower() for kw in shloka.get('keywords', []))
            ])
    
    sorted_themes = sorted(
        theme_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_themes

def find_chapters_by_theme(data, theme):
    """Find all chapters that contain a specific theme"""
    matching_chapters = []
    for chapter in data['chapters']:
        if ('main_theme' in chapter and theme in chapter['main_theme']) or \
        ('philosophical_aspects' in chapter and theme in chapter['philosophical_aspects']):
            matching_chapters.append(chapter)
    return matching_chapters

def main():
    st.set_page_config(page_title="Bhagavad Gita Knowledge Graph", layout="wide")
    
    # Custom CSS for sidebar
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
            background-image: linear-gradient(to bottom, #ffffff, #f8f9fa);
        }
        .sidebar .sidebar-content .block-container {
            padding-top: 2rem;
        }
        .sidebar .sidebar-content .st-expander {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 10px;
            margin-bottom: 15px;
        }
        .sidebar .sidebar-content .st-expander .stMarkdown {
            color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title with emoji
    st.title("🕉️ Bhagavad Gita Knowledge Graph")
    
    # Initialize the RAG system
    rag = GitaGraphRAG()
    
    if not rag.data:
        st.error("Failed to load Bhagavad Gita data.")
        return
    
    # Enhanced Sidebar for navigation
    with st.sidebar:
        st.markdown("""
        <div style="background-color:#6e48aa;padding:15px;border-radius:10px;margin-bottom:20px;">
            <h2 style="color:white;text-align:center;">🧭 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        view_option = st.selectbox(
            "Choose your exploration path:",
            ["Chapter Topology", "Ontologies of Wisdom", "Philosophical Themes Triples", "Ontology of Characters"],
            format_func=lambda x: f"📌 {x}"  # Add emoji prefix
        )
    
    # Show About section in sidebar
    show_about_section()
    
    if view_option == "Chapter Topology":
        st.header("📚 Chapter Topology")
        
        chapter_numbers = [ch['number'] for ch in rag.data['chapters']]
        selected_chapter_num = st.radio(
            "Select Chapter",
            sorted(chapter_numbers),
            format_func=lambda x: f"📖 Chapter {x}",
            horizontal=True
        )
        
        chapter_data = next((ch for ch in rag.data['chapters'] 
                        if ch['number'] == selected_chapter_num), None)
        
        if chapter_data:
            st.subheader(f"📜 Chapter {selected_chapter_num}: {chapter_data['name']}")
            
            content_tab, graph_tab = st.tabs(["📝 Chapter Content", "🕸️ Knowledge Graph"])
            
            with content_tab:
                st.markdown("### 📋 Summary")
                st.write(chapter_data['summary'])
                
                st.markdown("### 🕉️ Shlokas")
                for shloka in chapter_data.get('shlokas', []):
                    with st.expander(f"🪶 Shloka {shloka['shloka_number']}"):
                        shloka_text = shloka.get('sanskrit_text', '')
                        
                        if shloka_text:
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if st.button("🔊 Sanskrit", 
                                           key=f"sanskrit_ch_{selected_chapter_num}_{shloka['shloka_number']}"):
                                    audio_file = generate_audio(
                                        shloka_text,
                                        filename=f"sanskrit_{selected_chapter_num}_{shloka['shloka_number']}.mp3",
                                        lang='hi'
                                    )
                                    st.audio(audio_file, format="audio/mp3")
                            with col2:
                                st.markdown("**Sanskrit Text:**")
                                st.text(shloka_text)
                        
                        if 'transliteration' in shloka:
                            english_text = f"Meaning: {shloka.get('meaning', '')}\n\n"
                            if 'interpretation' in shloka:
                                english_text += f"Interpretation: {shloka['interpretation']}\n\n"
                            if 'life_application' in shloka:
                                english_text += f"Life Application: {shloka['life_application']}"
                            
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if st.button("🔊 Explanation", 
                                           key=f"english_ch_{selected_chapter_num}_{shloka['shloka_number']}"):
                                    audio_file = generate_audio(
                                        english_text,
                                        filename=f"english_{selected_chapter_num}_{shloka['shloka_number']}.mp3",
                                        lang='en'
                                    )
                                    st.audio(audio_file, format="audio/mp3")
                            
                            with col2:
                                if 'transliteration' in shloka:
                                    st.markdown("**Transliteration:**")
                                    st.write(shloka['transliteration'])
                                
                                st.markdown("**Meaning:**")
                                st.write(shloka['meaning'])
                                
                                if 'interpretation' in shloka:
                                    st.markdown("**Interpretation:**")
                                    st.write(shloka['interpretation'])
                                
                                if 'life_application' in shloka:
                                    st.markdown("**Life Application:**")
                                    st.write(shloka['life_application'])
            
            with graph_tab:
                st.markdown("### 🕸️ Chapter Knowledge Graph")
                
                if 'first_render' not in st.session_state:
                    st.session_state.first_render = True
                    st.rerun()
                
                nodes, edges = rag.visualize_chapter_graph(f"Chapter_{selected_chapter_num}")
                config = create_agraph_config()
                agraph(nodes=nodes, edges=edges, config=config)
                
                if st.session_state.first_render:
                    st.session_state.first_render = False

    elif view_option == "Ontologies of Wisdom":
        st.header("🧠 Knowledge Pathways from Bhagavad Gita")
        
        problems = list(rag.data['problem_solutions_map'].keys())
        selected_problem = st.radio(
            "Select a life challenge to explore solutions:",
            problems,
            format_func=lambda x: f"🤔 {x.replace('_', ' ').title()}",
            horizontal=True
        )
        
        if selected_problem:
            problem_data = rag.data['problem_solutions_map'][selected_problem]
            
            st.subheader("📝 Description")
            st.write(problem_data['description'])
            
            st.subheader("🕉️ Relevant Shlokas")
            for ref in problem_data['references']:
                shloka = rag.get_shloka_by_reference(ref['chapter'], ref['shloka'])
                if shloka:
                    with st.expander(f"📜 Chapter {ref['chapter']}, Shloka {ref['shloka']}"):
                        shloka_text = shloka.get('sanskrit_text', '')
                        
                        if shloka_text:
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if st.button("🔊 Sanskrit", 
                                           key=f"sanskrit_wisdom_{ref['chapter']}_{ref['shloka']}"):
                                    audio_file = generate_audio(
                                        shloka_text,
                                        filename=f"sanskrit_{ref['chapter']}_{ref['shloka']}.mp3",
                                        lang='hi'
                                    )
                                    st.audio(audio_file, format="audio/mp3")
                            with col2:
                                st.markdown("**Sanskrit Text:**")
                                st.text(shloka_text)
                        
                        if 'transliteration' in shloka:
                            english_text = f"Meaning: {shloka.get('meaning', '')}\n\n"
                            if 'interpretation' in shloka:
                                english_text += f"Interpretation: {shloka['interpretation']}\n\n"
                            if 'life_application' in shloka:
                                english_text += f"Life Application: {shloka['life_application']}"
                            
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if st.button("🔊 Explanation", 
                                           key=f"english_wisdom_{ref['chapter']}_{ref['shloka']}"):
                                    audio_file = generate_audio(
                                        english_text,
                                        filename=f"english_{ref['chapter']}_{ref['shloka']}.mp3",
                                        lang='en'
                                    )
                                    st.audio(audio_file, format="audio/mp3")
                            
                            with col2:
                                if 'transliteration' in shloka:
                                    st.markdown("**Transliteration:**")
                                    st.write(shloka['transliteration'])
                                
                                st.markdown("**Meaning:**")
                                st.write(shloka['meaning'])
                                
                                if 'interpretation' in shloka:
                                    st.markdown("**Interpretation:**")
                                    st.write(shloka['interpretation'])
                                
                                if 'life_application' in shloka:
                                    st.markdown("**Life Application:**")
                                    st.write(shloka['life_application'])

            st.markdown("---")
            st.subheader("🕸️ Problem-Solution Graph")
            problem_id = f"Problem_{selected_problem}"
            nodes, edges = rag.visualize_chapter_graph(problem_id)
            config = create_agraph_config()
            agraph(nodes=nodes, edges=edges, config=config)
    
    elif view_option == "Philosophical Themes Triples":
        st.header("🧘 Philosophical Themes Navigator")
        
        theme_data = get_themes_from_chapters(rag.data)
        theme_options = [theme for theme, _ in theme_data]
        theme_format = {theme: f"📌 {theme} ({count} shlokas)" 
                       for theme, count in theme_data}
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_theme = st.selectbox(
                "Select a philosophical theme to explore:",
                theme_options,
                format_func=lambda x: theme_format[x],
                key="theme_selector"
            )
        
        if selected_theme:
            st.subheader(f"🔍 Exploring: {selected_theme}")
            
            related_chapters = find_chapters_by_theme(rag.data, selected_theme)
            total_shlokas = sum(len([s for s in ch.get('shlokas', []) 
                                if any(kw.lower() in selected_theme.lower() 
                                      for kw in s.get('keywords', []))]) 
                              for ch in related_chapters)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="📚 Related Chapters",
                    value=len(related_chapters))
            with col2:
                st.metric(
                    label="🕉️ Relevant Shlokas",
                    value=total_shlokas)
            
            chapters_tab, relationships_tab = st.tabs(["📖 Related Chapters", "🕸️ Theme Relationships"])
            
            with chapters_tab:
                if related_chapters:
                    for chapter in related_chapters:
                        st.markdown(f"### 📜 Chapter {chapter['number']}: {chapter['name']}")
                        
                        with st.expander("📋 Chapter Summary & Themes", expanded=False):
                            st.markdown("#### 📝 Summary")
                            st.write(chapter['summary'])
                            
                            st.markdown("#### 🎯 Main Theme")
                            st.markdown(f"✨ ***{chapter['main_theme']}***")
                            
                            if 'philosophical_aspects' in chapter:
                                st.markdown("#### 💡 Philosophical Aspects")
                                for aspect in chapter['philosophical_aspects']:
                                    st.markdown(f"- 🌟 {aspect}")
                        
                        if 'shlokas' in chapter:
                            relevant_shlokas = [
                                shloka for shloka in chapter['shlokas']
                                if any(kw.lower() in selected_theme.lower() 
                                    for kw in shloka.get('keywords', []))
                            ]
                            
                            if relevant_shlokas:
                                st.markdown("#### 🕉️ Relevant Shlokas")
                                for shloka in relevant_shlokas:
                                    st.markdown(f"**🪶 Shloka {shloka['shloka_number']}**")
                                    display_shloka_content(shloka, chapter['number'])
                                    st.markdown("---")
                        
                        st.markdown("---")
            
            with relationships_tab:
                st.markdown("### 🕸️ Theme Relationships")
                chapter_tabs = st.tabs([f"📖 Chapter {chapter['number']}" for chapter in related_chapters])
                
                for tab, chapter in zip(chapter_tabs, related_chapters):
                    with tab:
                        st.markdown(f"#### {chapter['name']}")
                        nodes, edges = rag.visualize_theme_relationships(selected_theme, [chapter])
                        config = create_agraph_config()
                        agraph(nodes=nodes, edges=edges, config=config)

    elif view_option == "Ontology of Characters":
        rag.display_chapter_insights()

if __name__ == "__main__":
    main()