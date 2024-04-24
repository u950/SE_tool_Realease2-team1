import React, { useState, useEffect } from 'react';
import { DataSet } from 'vis-data/peer/esm/vis-data';
import { Network } from 'vis-network/peer/esm/vis-network';

function NetworkGraph({ data }) {
    const [nodes, setNodes] = useState(new DataSet([]));
    const [edges, setEdges] = useState([]);
    const [filenameToId, setFilenameToId] = useState({});
    const [searchQuery, setSearchQuery] = useState('');
    const [network, setNetwork] = useState(null);

    useEffect(() => {
        const mappedNodes = data.map((node, index) => ({
            id: index,
            label: node.scriptName
        }));
        const filenameIdDict = {};
        data.forEach((node, index) => {
            filenameIdDict[node.scriptName] = index;
        });
        setFilenameToId(filenameIdDict);

        const mappedEdges = data.flatMap((node) => (
            node.dependencies.map(dep => ({ from: node.id, to: dep[1] }))
        ));
        setNodes(new DataSet(mappedNodes));
        setEdges(mappedEdges);
    }, [data]);

    useEffect(() => {
        const container = document.getElementById('network');
        const options = {
            nodes: {
                shape: 'dot',
                font: {
                    strokeColor: 'black',
                    strokeWidth: 0,
                },
            },
            edges: {
                font: {
                    align: 'middle',
                    background: 'none',
                    strokeWidth: 0,
                    strokeColor: 'none',
                    color: 'gray',
                }
            }
        };
        const networkInstance = new Network(container, { nodes, edges }, options);
        setNetwork(networkInstance);

        return () => {
            networkInstance.destroy();
        };
    }, [nodes, edges]);

    const handleSearch = () => {
        if (!network) return;
        network.unselectAll();
        const nodeId = filenameToId[searchQuery];
        if (nodeId !== undefined) {
            network.selectNodes([nodeId]);
        }
    };

    return (
        <div>
            <div style={{ marginBottom: '10px' }}>
                <input
                    type="text"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    placeholder="Search..."
                />
                <button onClick={handleSearch}>Search</button>
            </div>
            <div id="network" style={{ width: '100%', height: '800px' }} />
        </div>
    );
}

export default NetworkGraph;