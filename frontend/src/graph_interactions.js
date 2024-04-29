import React from 'react';
import { useState } from 'react';
import { DataSet } from 'vis-data/peer/esm/vis-data';
import Graph from './graph'

function Interactions({data}){

    const [node, setNodes] = useState(new DataSet(data));
    const uniqueGroups = [...new Set(data.map(node => node.group))];

    // const joincondition=(nodeOptions)=>{
    //     return nodeOptions.group === this.group;
    // }
    const clusterOptions = {
        joinCondition: (nodeOptions, group) => {
            return nodeOptions.group === group;
        },
        ClusterNodeProperties: {
            shape: 'box',
            font: {
                size: 20,
            
            },
            borderWidth: 2,
            color: {
                backgroundColor:'white',
                border: 'black'
            }
        }
    }


    var options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: {
                size: 20,
                color: 'black'
            },
            borderWidth: 2
        },
        edges: {
            arrows: {
                to: { enabled: true, scaleFactor: 1, type: 'arrow' },
            },
        },
        physics: {
            // enabled: true,
            // barnesHut: {
            //     gravitationalConstant: -2000,
            //     centralGravity: 0.3,
            //     springLength: 95,
            //     springConstant: 0.04,
            //     damping: 0.09,
            //     avoidOverlap: 0
            // },
            // maxVelocity: 146,
            // minVelocity: 0.75,
            solver: 'forceAtlas2Based',
            stabilization: {
                enabled: true,
                iterations: 1000,
                updateInterval: 100,
                onlyDynamicEdges: false,
                fit: true
            },
            timestep: 0.5,
            adaptiveTimestep: true
        },
        interaction: {
            hover: true,
        },

    }
    

    return(
        <div>
            <Graph data={data} options={options}  />
        </div>
    )
}
export default Interactions;