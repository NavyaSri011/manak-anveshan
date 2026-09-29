import React, { useState, useMemo } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { ReactFlow, Controls, Background, MiniMap, applyNodeChanges, applyEdgeChanges } from '@xyflow/react';
import { Network, FileText, Info, ArrowLeft, RefreshCw, Layers } from 'lucide-react';

const DEFAULT_GRAPH_NODES = [
  { id: 'node-product', data: { label: 'Tender Product:\nCentrifugal Pump' }, position: { x: 250, y: 30 }, style: { background: '#0F172A', color: '#F8FAFC', border: '2px solid #D97706', borderRadius: '8px', padding: '12px', fontWeight: 'bold', width: 220, fontSize: '12px' } },
  { id: 'node-std-1520', data: { label: 'IS 1520:1980 [PRIMARY]\nHorizontal Centrifugal Pumps' }, position: { x: 50, y: 160 }, style: { background: '#1E3A8A', color: '#FFFFFF', border: '1px solid #1E40AF', borderRadius: '8px', padding: '10px', fontSize: '11px', width: 200 } },
  { id: 'node-std-9137', data: { label: 'IS 9137:1978 [TEST]\nClass C Acceptance Tests' }, position: { x: -100, y: 300 }, style: { background: '#065F46', color: '#FFFFFF', border: '1px solid #047857', borderRadius: '8px', padding: '10px', fontSize: '11px', width: 190 } },
  { id: 'node-std-11346', data: { label: 'IS 11346:2002 [INSTALLATION]\nSelection & Installation Code' }, position: { x: 120, y: 300 }, style: { background: '#155E75', color: '#FFFFFF', border: '1px solid #0E7490', borderRadius: '8px', padding: '10px', fontSize: '11px', width: 190 } },
  { id: 'node-std-12615', data: { label: 'IS 12615:2018 [NORMATIVE]\nIE3 Energy Efficient Motors' }, position: { x: 340, y: 300 }, style: { background: '#B45309', color: '#FFFFFF', border: '1px solid #D97706', borderRadius: '8px', padding: '10px', fontSize: '11px', width: 190 } },
  { id: 'node-std-732', data: { label: 'IS 732:2019 [SAFETY]\nElectrical Wiring Safety Code' }, position: { x: 560, y: 300 }, style: { background: '#9F1239', color: '#FFFFFF', border: '1px solid #BE123C', borderRadius: '8px', padding: '10px', fontSize: '11px', width: 190 } },
  { id: 'node-qco-1', data: { label: 'QCO Mandate [CERTIFICATION]\nBIS ISI Mark Required' }, position: { x: 120, y: 440 }, style: { background: '#064E3B', color: '#F0FDF4', border: '2px solid #10B981', borderRadius: '8px', padding: '10px', fontWeight: 'bold', fontSize: '11px', width: 220 } }
];

const DEFAULT_GRAPH_EDGES = [
  { id: 'e1', source: 'node-product', target: 'node-std-1520', label: 'governed_by', animated: true, style: { stroke: '#0F172A', strokeWidth: 2 } },
  { id: 'e2', source: 'node-std-1520', target: 'node-std-9137', label: 'tested_by', animated: false },
  { id: 'e3', source: 'node-std-1520', target: 'node-std-11346', label: 'installation_by', animated: false },
  { id: 'e4', source: 'node-std-1520', target: 'node-std-12615', label: 'references', animated: false },
  { id: 'e5', source: 'node-std-12615', target: 'node-std-732', label: 'safety_by', animated: false },
  { id: 'e6', source: 'node-std-1520', target: 'node-qco-1', label: 'mandated_by', animated: true, style: { stroke: '#059669', strokeWidth: 2 } }
];

export default function StandardsGraph() {
  const location = useLocation();
  const passedGraphData = location.state?.graphData;

  const initialNodes = useMemo(() => {
    if (!passedGraphData || !passedGraphData.nodes) return DEFAULT_GRAPH_NODES;
    
    return passedGraphData.nodes.map((n, i) => {
      let bg = '#1E3A8A';
      if (n.type === 'product') bg = '#0F172A';
      else if (n.type === 'primary') bg = '#1E3A8A';
      else if (n.type === 'test') bg = '#065F46';
      else if (n.type === 'safety') bg = '#9F1239';
      else if (n.type === 'installation') bg = '#155E75';
      else if (n.type === 'normative') bg = '#B45309';
      else if (n.type === 'certification') bg = '#064E3B';

      const xPos = (i % 3) * 260;
      const yPos = Math.floor(i / 3) * 160 + 50;

      return {
        id: n.id,
        data: { label: n.label },
        position: { x: xPos, y: yPos },
        style: {
          background: bg,
          color: '#FFFFFF',
          border: n.type === 'certification' ? '2px solid #10B981' : '1px solid #475569',
          borderRadius: '8px',
          padding: '10px',
          fontSize: '11px',
          width: 200
        }
      };
    });
  }, [passedGraphData]);

  const initialEdges = useMemo(() => {
    if (!passedGraphData || !passedGraphData.edges) return DEFAULT_GRAPH_EDGES;
    return passedGraphData.edges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      label: e.label,
      animated: e.animated || false,
      style: { stroke: '#475569', strokeWidth: 1.5 }
    }));
  }, [passedGraphData]);

  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);

  const onNodesChange = (changes) => setNodes((nds) => applyNodeChanges(changes, nds));
  const onEdgesChange = (changes) => setEdges((eds) => applyEdgeChanges(changes, eds));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Header */}
      <div className="border-b border-slate-300 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-serif flex items-center gap-2">
            <Network className="w-6 h-6 text-amber-600" />
            Normative & Allied Standards Knowledge Graph
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Interactive node-edge graph showing relationship links between product specifications, primary standards, test methods, safety codes, and Quality Control Orders.
          </p>
        </div>

        <Link to="/new-analysis" className="bg-slate-900 text-amber-400 font-bold px-3 py-1.5 rounded text-xs">
          New Analysis
        </Link>
      </div>

      {/* Graph Legend */}
      <div className="bg-slate-900 text-white p-3 rounded-lg flex flex-wrap items-center justify-between gap-4 text-xs font-mono">
        <div className="flex flex-wrap items-center gap-4">
          <span className="font-bold text-amber-400">Node Legend:</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-slate-900 border border-amber-500 rounded"></span> Product Spec</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-blue-900 rounded"></span> Primary Standard</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-emerald-800 rounded"></span> Test Method</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-cyan-800 rounded"></span> Installation</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-amber-700 rounded"></span> Normative Ref</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-rose-800 rounded"></span> Safety Code</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-emerald-900 border border-emerald-400 rounded"></span> QCO Certification</span>
        </div>
        <div className="text-[11px] text-slate-400">
          Drag nodes to arrange • Scroll to zoom
        </div>
      </div>

      {/* React Flow Container */}
      <div className="bg-white border border-slate-300 rounded-lg h-137.5 relative shadow-inner">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
        >
          <Background color="#CBD5E1" gap={16} />
          <Controls />
          <MiniMap nodeStrokeWidth={3} zoomable pannable />
        </ReactFlow>
      </div>

    </div>
  );
}
