import React, { useState, useEffect } from 'react';
import { DataSet } from 'vis-data/peer/esm/vis-data';
import { Network } from 'vis-network/peer/esm/vis-network';

function NetworkGraph({ data, options }) {
    const [nodes, setNodes] = useState(new DataSet([]));
    const [edges, setEdges] = useState(new DataSet([]));
    const [network, setNetwork] = useState(null);
    const [showOptions, setShowOptions] = useState(false);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        const mappedNodes = data.map((node) => ({
            id: node.id,
            label: node.label,
            group: node.group,
            title: node.scriptName // Add title for node tooltip
        }));

        const mappedEdges = data.flatMap((node) => (
            node.dependencies.map((dep) => ({
                from: dep[1],
                to: node.id,
                // Add title for edge tooltip
            }))
        ));

        setNodes(new DataSet(mappedNodes));
        setEdges(new DataSet(mappedEdges));
    }, [data]);

    useEffect(() => {
        const container = document.getElementById('network');
        const networkInstance = new Network(container, { nodes, edges }, options);

        // Add event listener for node and edge hovering to display tooltips
        networkInstance.on('hoverNode', (event) => {
            const nodeId = event.node;
            const node = nodes.get(nodeId);
            networkInstance.canvas.body.container.title = node.title || '';
        });

        networkInstance.on('hoverEdge', (event) => {
            const edgeId = event.edge;
            const edge = edges.get(edgeId);
            const fromNode = nodes.get(edge.from);
            const toNode = nodes.get(edge.to);

            const local_dep = data.find(node => node.id === toNode.id)?.local_dependent || ["null"];
            networkInstance.canvas.body.container.title = `Imported :${local_dep} `;
        });

        networkInstance.on('click', (event) => {
            if (event.nodes.length > 0) {
                const clickedNodeId = event.nodes;
                const clickedNode = nodes.get(clickedNodeId);

                console.log('clickedNode:', clickedNode);
                // Send clickedNode data to server endpoint
                fetch('http://127.0.0.1:5000/node_clicked', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(clickedNode)
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Server response:', data);
                    })
                    .catch(error => {
                        console.error('Error sending data to server:', error);
                    });
            }
        });

        setNetwork(networkInstance);
        setLoading(false);

        return () => {
            networkInstance.destroy();
        };
    }, [data, options]);

    const handleSearch = (query) => {
        setSearchQuery(query);
        const filteredNodes = data.filter(node => node.label.toLowerCase().includes(query.toLowerCase()));
        const mappedFilteredNodes = filteredNodes.map(node => ({
            id: node.id,
            label: node.label,
            group: node.group,
            title: node.scriptName // Add title for node tooltip
        }));
        setNodes(new DataSet(mappedFilteredNodes));
    };

    return (
        <div style={{ position: 'relative', padding:'60px' }}>
            <div style={{ marginBottom: '10px' }}>
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => handleSearch(e.target.value)}
                    placeholder="Search for nodes..."
                />
            </div>
            {loading && <div className="spinner" />}
            <div id="network" style={{ width: '100%', height: '800px', background: 'white'}} />
        </div>
    );
}

export default NetworkGraph;
