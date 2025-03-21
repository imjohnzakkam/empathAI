import networkx as nx
import logging
import os
import json
from pathlib import Path

class TherapeuticKnowledgeGraph:
    """
    A knowledge graph that maps emotions to appropriate therapeutic techniques.
    This graph represents relationships between emotional states and 
    therapeutic interventions based on psychological principles.
    """
    
    def __init__(self, graph_path=None):
        """
        Initialize the therapeutic knowledge graph.
        
        Args:
            graph_path: Path to a pre-built knowledge graph (optional)
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize the knowledge graph
        if graph_path and os.path.exists(graph_path):
            self.load_graph(graph_path)
        else:
            self.graph = self._create_default_graph()
            self.logger.info("Created default therapeutic knowledge graph")
    
    def _create_default_graph(self):
        """
        Create a default knowledge graph with basic emotion-technique relationships.
        In a real implementation, this would be much more comprehensive.
        
        Returns:
            NetworkX graph object
        """
        G = nx.Graph()
        
        # Add emotion nodes
        emotions = [
            "anger", "disgust", "fear", "joy", "sadness", 
            "surprise", "neutral", "anxiety", "stress",
            "grief", "loneliness", "frustration"
        ]
        
        for emotion in emotions:
            G.add_node(emotion, type="emotion")
        
        # Add technique nodes
        techniques = {
            "deep_breathing": {
                "name": "Deep Breathing Exercise",
                "description": "Slow, deep breathing to reduce stress and anxiety",
                "type": "technique"
            },
            "cognitive_reframing": {
                "name": "Cognitive Reframing",
                "description": "Identifying and changing negative thought patterns",
                "type": "technique"
            },
            "mindfulness": {
                "name": "Mindfulness Practice",
                "description": "Focusing on the present moment without judgment",
                "type": "technique"
            },
            "gratitude": {
                "name": "Gratitude Exercise",
                "description": "Reflecting on things to be thankful for",
                "type": "technique"
            },
            "progressive_relaxation": {
                "name": "Progressive Muscle Relaxation",
                "description": "Tensing and relaxing muscle groups to reduce physical tension",
                "type": "technique"
            },
            "journal_writing": {
                "name": "Expressive Journal Writing",
                "description": "Writing about emotions and experiences",
                "type": "technique"
            },
            "positive_affirmation": {
                "name": "Positive Affirmations",
                "description": "Repeating positive statements about oneself",
                "type": "technique"
            },
            "social_connection": {
                "name": "Social Connection Exercise",
                "description": "Reaching out to supportive people",
                "type": "technique"
            },
            "physical_exercise": {
                "name": "Physical Exercise",
                "description": "Engaging in physical activity to improve mood",
                "type": "technique"
            },
            "visualization": {
                "name": "Positive Visualization",
                "description": "Imagining calming or positive scenarios",
                "type": "technique"
            }
        }
        
        for technique_id, attributes in techniques.items():
            G.add_node(technique_id, **attributes)
        
        # Connect emotions to techniques with weighted edges
        # Higher weight = stronger recommendation for that emotion
        connections = [
            ("anger", "deep_breathing", 0.9),
            ("anger", "mindfulness", 0.7),
            ("anger", "progressive_relaxation", 0.8),
            ("anger", "cognitive_reframing", 0.8),
            ("anger", "journal_writing", 0.6),
            
            ("fear", "deep_breathing", 0.9),
            ("fear", "progressive_relaxation", 0.8),
            ("fear", "cognitive_reframing", 0.7),
            ("fear", "visualization", 0.7),
            
            ("anxiety", "deep_breathing", 0.9),
            ("anxiety", "progressive_relaxation", 0.9),
            ("anxiety", "mindfulness", 0.8),
            ("anxiety", "cognitive_reframing", 0.7),
            
            ("sadness", "cognitive_reframing", 0.8),
            ("sadness", "gratitude", 0.7),
            ("sadness", "social_connection", 0.9),
            ("sadness", "physical_exercise", 0.8),
            ("sadness", "journal_writing", 0.7),
            
            ("joy", "gratitude", 0.9),
            ("joy", "social_connection", 0.8),
            ("joy", "positive_affirmation", 0.7),
            
            ("surprise", "mindfulness", 0.7),
            ("surprise", "journal_writing", 0.6),
            
            ("disgust", "cognitive_reframing", 0.8),
            ("disgust", "mindfulness", 0.7),
            
            ("grief", "journal_writing", 0.9),
            ("grief", "social_connection", 0.8),
            ("grief", "mindfulness", 0.7),
            
            ("stress", "deep_breathing", 0.9),
            ("stress", "progressive_relaxation", 0.9),
            ("stress", "physical_exercise", 0.8),
            ("stress", "mindfulness", 0.8),
            
            ("loneliness", "social_connection", 0.9),
            ("loneliness", "gratitude", 0.7),
            ("loneliness", "journal_writing", 0.6),
            
            ("frustration", "deep_breathing", 0.8),
            ("frustration", "cognitive_reframing", 0.8),
            ("frustration", "physical_exercise", 0.7),
            
            ("neutral", "mindfulness", 0.6),
            ("neutral", "gratitude", 0.6),
            ("neutral", "positive_affirmation", 0.6)
        ]
        
        for emotion, technique, weight in connections:
            G.add_edge(emotion, technique, weight=weight)
        
        return G
    
    def load_graph(self, path):
        """
        Load a knowledge graph from a file.
        
        Args:
            path: Path to the knowledge graph file
        """
        try:
            # For JSON format
            if path.endswith('.json'):
                with open(path, 'r') as f:
                    data = json.load(f)
                    
                G = nx.Graph()
                
                # Add nodes
                for node_id, attrs in data.get('nodes', {}).items():
                    G.add_node(node_id, **attrs)
                
                # Add edges
                for source, targets in data.get('edges', {}).items():
                    for target, attrs in targets.items():
                        G.add_edge(source, target, **attrs)
                
                self.graph = G
                self.logger.info(f"Loaded knowledge graph from {path}")
            
            # For NetworkX formats
            else:
                self.graph = nx.read_gpickle(path)
                self.logger.info(f"Loaded knowledge graph from {path}")
                
        except Exception as e:
            self.logger.error(f"Error loading knowledge graph: {str(e)}")
            self.graph = self._create_default_graph()
            self.logger.info("Created default knowledge graph as fallback")
    
    def save_graph(self, path):
        """
        Save the knowledge graph to a file.
        
        Args:
            path: Path to save the knowledge graph
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Save based on file format
            if path.endswith('.json'):
                # Convert to dictionary format
                data = {
                    'nodes': {node: self.graph.nodes[node] for node in self.graph.nodes},
                    'edges': {}
                }
                
                for source, target in self.graph.edges:
                    if source not in data['edges']:
                        data['edges'][source] = {}
                    data['edges'][source][target] = self.graph.edges[source, target]
                
                with open(path, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                # Use NetworkX's pickle format
                nx.write_gpickle(self.graph, path)
                
            self.logger.info(f"Saved knowledge graph to {path}")
            
        except Exception as e:
            self.logger.error(f"Error saving knowledge graph: {str(e)}")
    
    def get_techniques(self, emotions, max_techniques=3):
        """
        Get appropriate therapeutic techniques based on detected emotions.
        
        Args:
            emotions: Dictionary of emotions and their scores
            max_techniques: Maximum number of techniques to return
            
        Returns:
            List of recommended technique IDs
        """
        # Extract top emotions
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        top_emotions = [emotion for emotion, score in sorted_emotions[:3] if score > 0.1]
        
        if not top_emotions:
            # Fallback to neutral if no significant emotions detected
            top_emotions = ["neutral"]
        
        # Collect candidate techniques
        candidate_techniques = {}
        
        for emotion in top_emotions:
            # Find technique nodes connected to this emotion
            if emotion in self.graph:
                for technique_id in self.graph.neighbors(emotion):
                    # Get edge data which contains the relevance score
                    edge_data = self.graph.get_edge_data(emotion, technique_id)
                    relevance = edge_data.get('relevance', 0.5)
                    emotion_score = emotions.get(emotion, 0.5)
                    
                    # Calculate a combined score
                    combined_score = relevance * emotion_score
                    
                    # Update the technique's score
                    if technique_id in candidate_techniques:
                        candidate_techniques[technique_id] += combined_score
                    else:
                        candidate_techniques[technique_id] = combined_score
        
        # Sort techniques by score
        sorted_techniques = sorted(candidate_techniques.items(), key=lambda x: x[1], reverse=True)
        
        # Return the top N techniques
        return [technique_id for technique_id, score in sorted_techniques[:max_techniques]]
    
    def get_techniques_for_emotions(self, emotions, max_techniques=3):
        """
        Get appropriate therapeutic techniques based on detected emotions.
        An alias for get_techniques to maintain compatibility.
        
        Args:
            emotions: Dictionary of emotions and their scores
            max_techniques: Maximum number of techniques to return
            
        Returns:
            List of recommended technique IDs
        """
        return self.get_techniques(emotions, max_techniques)
    
    def get_technique_details(self, technique_id):
        """
        Get details about a specific therapeutic technique.
        
        Args:
            technique_id: ID of the technique
            
        Returns:
            Dictionary of technique details
        """
        if technique_id in self.graph:
            return dict(self.graph.nodes[technique_id])
        return None 