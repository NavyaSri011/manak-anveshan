from typing import List, Dict, Any
from app.schemas.analysis import RecommendationCard, StandardsGraphData, StandardsGraphNode, StandardsGraphEdge

class GraphVisualizationService:

    @staticmethod
    def build_graph_data(
        product_title: str,
        primary: List[RecommendationCard],
        supporting: List[RecommendationCard],
        normative: List[RecommendationCard],
        test: List[RecommendationCard],
        safety: List[RecommendationCard],
        installation: List[RecommendationCard],
        certification_summary: List[Dict[str, Any]]
    ) -> StandardsGraphData:
        
        nodes: List[StandardsGraphNode] = []
        edges: List[StandardsGraphEdge] = []
        added_node_ids = set()

        # Root Product Node
        root_id = "node-product-root"
        nodes.append(StandardsGraphNode(
            id=root_id,
            type="product",
            label=f"Product: {product_title}",
            status="ACTIVE",
            category="Procurement Spec"
        ))
        added_node_ids.add(root_id)

        # Function to process standard card group
        def add_group(group: List[RecommendationCard], node_type: str, edge_label: str):
            for card in group[:3]: # top 3 per group for clean layout
                node_id = f"node-{card.id}"
                if node_id not in added_node_ids:
                    nodes.append(StandardsGraphNode(
                        id=node_id,
                        type=node_type,
                        label=f"{card.is_number}\n{card.title[:35]}...",
                        status=card.status,
                        category=card.category
                    ))
                    added_node_ids.add(node_id)
                
                # Connect from root or primary
                source_id = root_id
                if node_type != "primary" and primary:
                    source_id = f"node-{primary[0].id}"
                    if source_id not in added_node_ids:
                        source_id = root_id

                edges.append(StandardsGraphEdge(
                    id=f"edge-{source_id}-{node_id}",
                    source=source_id,
                    target=node_id,
                    label=edge_label,
                    animated=True if node_type in ["primary", "certification"] else False
                ))

        add_group(primary, "primary", "governed_by")
        add_group(supporting, "supporting", "supported_by")
        add_group(test, "test", "tested_by")
        add_group(safety, "safety", "safety_by")
        add_group(installation, "installation", "installation_by")
        add_group(normative, "normative", "references")

        # Certification Nodes
        for idx, cert in enumerate(certification_summary[:2]):
            cert_node_id = f"node-cert-{idx}"
            nodes.append(StandardsGraphNode(
                id=cert_node_id,
                type="certification",
                label=f"Certification / QCO\n{cert['scheme']}",
                status=cert["status"],
                category="Regulatory Mandate"
            ))
            added_node_ids.add(cert_node_id)

            target_std_num = cert["is_number"]
            matching_primary = next((p for p in primary if p.is_number == target_std_num), None)
            source_id = f"node-{matching_primary.id}" if matching_primary else root_id

            edges.append(StandardsGraphEdge(
                id=f"edge-{source_id}-{cert_node_id}",
                source=source_id,
                target=cert_node_id,
                label="mandated_by",
                animated=True
            ))

        return StandardsGraphData(nodes=nodes, edges=edges)
