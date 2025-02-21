import json
import networkx as nx
from pyvis.network import Network

class Visualizer:
    def __init__(self):
        self.default_options = {
            'height': '600px',
            'width': '100%',
            'bgcolor': '#ffffff',
            'font_color': '#333333',
            'edges': {
                'color': '#666666',
                'width': 2,
                'arrows': {
                    'to': {'enabled': True, 'scaleFactor': 0.5}
                }
            },
            'nodes': {
                'shape': 'dot',
                'size': 25,
                'font': {
                    'size': 14,
                    'face': 'Arial'
                }
            },
            'physics': {
                'enabled': True,
                'solver': 'forceAtlas2Based'
            }
        }

    def create_mind_map(self, concepts, central_topic):
        """Create a radial mind map visualization"""
        net = Network(notebook=False, cdn_resources='remote', directed=True)
        net.set_options(json.dumps(self.default_options))

        # Add central topic
        net.add_node(0, label=central_topic, color='#4CAF50', size=40)

        # Add main branches (concept categories)
        colors = {
            'terms': '#2196F3',
            'entities': '#FFC107',
            'definitions': '#9C27B0',
            'relationships': '#FF5722'
        }

        node_id = 1
        for category, color in colors.items():
            net.add_node(node_id, label=category.title(), color=color, size=30)
            net.add_edge(0, node_id)
            
            # Add concepts under each category
            if category in concepts:
                items = concepts[category]
                if isinstance(items, list):
                    for item in items:
                        node_id += 1
                        if isinstance(item, dict):
                            label = item.get('term', item.get('text', str(item)))
                        else:
                            label = str(item)
                        net.add_node(node_id, label=label, color=color)
                        net.add_edge(node_id - 1, node_id)
                elif isinstance(items, dict):
                    for key, values in items.items():
                        node_id += 1
                        net.add_node(node_id, label=key, color=color)
                        net.add_edge(node_id - 1, node_id)
                        
                        for value in values:
                            node_id += 1
                            if isinstance(value, dict):
                                label = value.get('text', str(value))
                            else:
                                label = str(value)
                            net.add_node(node_id, label=label, color=color)
                            net.add_edge(node_id - 1, node_id)

            node_id += 1

        return net

    def create_knowledge_graph(self, graph):
        """Create a knowledge graph visualization from a NetworkX graph"""
        net = Network(notebook=False, cdn_resources='remote', directed=True)
        net.set_options(json.dumps(self.default_options))

        # Color scheme for different node types
        color_scheme = {
            'term': '#2196F3',
            'definition': '#4CAF50',
            'person': '#FFC107',
            'organization': '#9C27B0',
            'location': '#FF5722',
            'concept': '#607D8B'
        }

        # Add nodes
        for node, data in graph.nodes(data=True):
            node_type = data.get('type', 'concept')
            color = color_scheme.get(node_type, '#607D8B')
            net.add_node(node, label=str(node), color=color, title=f"Type: {node_type}")

        # Add edges
        for source, target, data in graph.edges(data=True):
            relation = data.get('relation', '')
            net.add_edge(source, target, title=relation)

        return net

    def create_concept_map(self, concepts):
        """Create a hierarchical concept map"""
        net = Network(notebook=False, cdn_resources='remote', directed=True)
        
        # Customize options for hierarchical layout
        options = self.default_options.copy()
        options['layout'] = {
            'hierarchical': {
                'enabled': True,
                'direction': 'UD',
                'sortMethod': 'directed',
                'nodeSpacing': 150,
                'levelSeparation': 150
            }
        }
        net.set_options(json.dumps(options))

        # Track nodes to avoid duplicates
        added_nodes = set()
        node_id = 0

        # Add terms and their definitions
        for definition in concepts['definitions']:
            term = definition['term']
            if term not in added_nodes:
                net.add_node(node_id, label=term, color='#2196F3')
                term_id = node_id
                added_nodes.add(term)
                node_id += 1
            
            net.add_node(node_id, label=definition['definition'], color='#4CAF50')
            net.add_edge(term_id, node_id, title='is defined as')
            node_id += 1

        # Add relationships
        for edge in concepts['relationships']['edges']:
            source = edge['source']
            target = edge['target']
            
            # Add source node if not exists
            if source not in added_nodes:
                net.add_node(node_id, label=source, color='#FFC107')
                source_id = node_id
                added_nodes.add(source)
                node_id += 1
            
            # Add target node if not exists
            if target not in added_nodes:
                net.add_node(node_id, label=target, color='#FFC107')
                target_id = node_id
                added_nodes.add(target)
                node_id += 1
            
            net.add_edge(source_id, target_id, title=edge['relation'])

        return net

    def save_visualization(self, visualization, output_path):
        """Save the visualization to an HTML file"""
        visualization.save_graph(output_path)
