"""Deterministic architecture reasoning and impact analysis layer grounded in graph evidence."""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

from src.graph.base import BaseGraphClient
from src.graph.mock_graph_client import MockGraphClient
from src.mcp.tools import GraphToolRegistry


class RiskItem(BaseModel):
    """Structured architectural risk evaluation grounded in observable graph topology."""

    risk_title: str = Field(..., description="Short descriptive title of the architectural risk")
    severity: Literal["LOW", "MEDIUM", "HIGH"] = Field(..., description="Assessed severity level")
    evidence: Dict[str, Any] = Field(..., description="Concrete graph evidence: node IDs, edge counts, or cycle paths")
    explanation: str = Field(..., description="Explanation of why this graph pattern may present an architectural concern")
    confidence_level: Literal["LOW", "MEDIUM", "HIGH"] = Field(..., description="Confidence in the assessment")
    assessment_basis: Literal["observed_graph_structure", "inferred_architectural_implication"] = Field(
        ...,
        description="Whether the finding is a direct graph fact or an inferred architectural risk",
    )


class RefactoringRecommendation(BaseModel):
    """Graph-grounded refactoring recommendation addressing identified structural debt."""

    title: str = Field(..., description="Recommendation headline")
    target_components: List[str] = Field(..., description="Exact graph node IDs targeted for remediation")
    supporting_graph_evidence: str = Field(..., description="Specific graph facts supporting this recommendation")
    intended_architectural_benefit: str = Field(..., description="Expected engineering benefit (decoupling, isolation, deployability)")
    action_steps: List[str] = Field(..., description="Step-by-step engineering actions")


class ArchitectureAnalysisResult(BaseModel):
    """Structured output envelope containing comprehensive architecture reasoning findings."""

    analysis_type: str = Field(..., description="Type of analysis performed (e.g. component_impact, global_architecture)")
    graph_source: str = Field(
        default="sample/mock architecture graph (mock_graph_seed.json)",
        description="Explicit disclosure that data originates from the sample/mock graph",
    )
    target_node_id: Optional[str] = Field(None, description="Analyzed component ID if single-component inquiry")
    target_node_name: Optional[str] = Field(None, description="Analyzed component display name")
    target_node_type: Optional[str] = Field(None, description="Analyzed component type")
    summary: str = Field(..., description="High-level narrative summary of findings")
    affected_nodes: Dict[str, Any] = Field(default_factory=dict, description="Downstream affected nodes grouped by type")
    dependency_paths: List[List[str]] = Field(default_factory=list, description="Observed shortest paths from callers to target")
    cycles: List[Dict[str, Any]] = Field(default_factory=list, description="Observed circular dependencies with explanations")
    coupling_metrics: Optional[Dict[str, Any]] = Field(None, description="Afferent, efferent, and instability metrics")
    shared_dependencies: List[Dict[str, Any]] = Field(default_factory=list, description="Shared datastores or modules used by multiple services")
    risks: List[RiskItem] = Field(default_factory=list, description="Evidence-backed architectural risk assessments")
    recommendations: List[RefactoringRecommendation] = Field(default_factory=list, description="Graph-grounded refactoring steps")
    limitations: List[str] = Field(default_factory=list, description="Methodological limitations and sample data disclosures")
    is_valid: bool = Field(True, description="Whether analysis succeeded against valid graph components")
    error_message: Optional[str] = Field(None, description="Error message if analysis failed or node was unknown")


class ArchitectureReasoner:
    """Deterministic reasoning engine deriving evidence-based architectural insights from graph topology.
    
    Guarantees:
        - Read-only: Never mutates graph state.
        - Grounded: Reuses existing graph algorithms; never invents nodes, routes, or edges.
        - Calibrated: Distinguishes observed graph topology from inferred architectural implications.
        - Transparent: Discloses mock/sample dataset provenance and analytical limitations.
        - Deterministic: Produces consistent, JSON-serializable output for identical inputs.
    """

    GRAPH_SOURCE_LABEL = "sample/mock architecture graph (mock_graph_seed.json)"

    DEFAULT_LIMITATIONS = [
        "Analysis is conducted on a fictional sample architecture graph (mock_graph_seed.json).",
        "Results reflect static dependency topology and do not incorporate runtime traffic metrics, error rates, or request latency.",
        "Inferred risks indicate structural coupling patterns; they should not be treated as confirmed production incidents or guaranteed outages.",
        "Refactoring recommendations address structural graph debt and require validation against organizational domain boundaries.",
    ]

    def __init__(
        self,
        graph_client: Optional[BaseGraphClient] = None,
        tool_registry: Optional[GraphToolRegistry] = None,
    ):
        """Initialize reasoner with graph client and tool registry."""
        self.graph_client = graph_client or MockGraphClient()
        self.tool_registry = tool_registry or GraphToolRegistry(graph_client=self.graph_client)

    def analyze_component(self, node_id: str) -> ArchitectureAnalysisResult:
        """Perform comprehensive, evidence-based impact and risk analysis for a specific component.
        
        Args:
            node_id: Target component ID (e.g. 'legacy-auth-module', 'order-service').
            
        Returns:
            ArchitectureAnalysisResult containing blast radius, risks, and refactoring guidance.
        """
        # Validate existence of target node in graph
        target_node = self.graph_client.get_node(node_id)
        if not target_node:
            return ArchitectureAnalysisResult(
                analysis_type="component_impact",
                graph_source=self.GRAPH_SOURCE_LABEL,
                target_node_id=node_id,
                summary=f"Analysis could not be performed: component '{node_id}' does not exist in the sample graph.",
                limitations=self.DEFAULT_LIMITATIONS,
                is_valid=False,
                error_message=f"Component '{node_id}' not found in {self.GRAPH_SOURCE_LABEL}.",
            )

        target_name = target_node.get("name", node_id)
        target_type = target_node.get("type", "Generic")

        # 1. Blast-radius analysis (reusing verified graph algorithm)
        blast_data = self.graph_client.calculate_blast_radius(node_id)
        total_affected = blast_data.get("total_affected_count", 0)
        direct_callers = blast_data.get("direct_dependents", [])
        indirect_callers = blast_data.get("indirect_dependents", [])
        paths = blast_data.get("traversal_paths", [])

        # Categorize affected nodes strictly based on graph data
        affected_nodes_summary = {
            "total_affected_count": total_affected,
            "starting_node_included": False,
            "affected_microservices": blast_data.get("affected_services", []),
            "affected_api_routes": blast_data.get("affected_api_routes", []),
            "affected_frontend_components": blast_data.get("affected_frontend_components", []),
            "direct_dependents": direct_callers,
            "indirect_dependents": indirect_callers,
            "by_category": blast_data.get("affected_by_category", {}),
        }

        # 2. Coupling metrics (reusing verified coupling calculation)
        coupling = self.graph_client.calculate_coupling_metrics(node_id)

        # 3. Dependency cycles involving or adjacent to the component
        all_cycles = self.graph_client.detect_cycles()
        involved_cycles = [
            {
                "cycle_nodes": c,
                "cycle_length": len(c),
                "involves_target": node_id in c,
                "explanation": (
                    f"Circular dependency observed between {' <-> '.join(c)}. "
                    "In microservice architectures, dependency cycles can prevent independent deployments "
                    "and increase the risk of cascading timeout loops."
                ),
            }
            for c in all_cycles
        ]

        # 4. Shared dependencies used by multiple services
        shared_dependencies = self._find_shared_dependencies(target_id=node_id)

        # 5. Formulate evidence-based risks
        risks = self._evaluate_risks(
            target_id=node_id,
            target_name=target_name,
            target_type=target_type,
            coupling=coupling,
            blast_data=blast_data,
            involved_cycles=involved_cycles,
            shared_dependencies=shared_dependencies,
        )

        # 6. Formulate graph-grounded refactoring recommendations
        recommendations = self._generate_recommendations(
            target_id=node_id,
            target_name=target_name,
            target_type=target_type,
            blast_data=blast_data,
            involved_cycles=involved_cycles,
            shared_dependencies=shared_dependencies,
            risks=risks,
        )

        # Summary narrative
        summary = (
            f"Impact analysis for '{target_name}' (`{node_id}`) based on the sample architecture graph. "
            f"If this component is modified or deprecated, graph traversal reveals {total_affected} downstream "
            f"dependent components (excluding '{node_id}' itself) that may be impacted: "
            f"{len(blast_data.get('affected_services', []))} microservices, "
            f"{len(blast_data.get('affected_api_routes', []))} API routes, and "
            f"{len(blast_data.get('affected_frontend_components', []))} frontend applications. "
            f"Afferent coupling is Ca={coupling.get('afferent_coupling', 0)} and efferent coupling is Ce={coupling.get('efferent_coupling', 0)}."
        )

        return ArchitectureAnalysisResult(
            analysis_type="component_impact",
            graph_source=self.GRAPH_SOURCE_LABEL,
            target_node_id=node_id,
            target_node_name=target_name,
            target_node_type=target_type,
            summary=summary,
            affected_nodes=affected_nodes_summary,
            dependency_paths=paths,
            cycles=involved_cycles,
            coupling_metrics=coupling,
            shared_dependencies=shared_dependencies,
            risks=risks,
            recommendations=recommendations,
            limitations=self.DEFAULT_LIMITATIONS,
            is_valid=True,
        )

    def analyze_global_architecture(self) -> ArchitectureAnalysisResult:
        """Perform system-wide architecture reasoning across all components in the graph."""
        schema = self.graph_client.get_schema()
        all_cycles = self.graph_client.detect_cycles()
        shared_deps = self._find_shared_dependencies()

        cycles_summary = [
            {
                "cycle_nodes": c,
                "cycle_length": len(c),
                "involves_target": False,
                "explanation": (
                    f"Circular dependency observed between {' <-> '.join(c)}. "
                    "Tight coupling between these services complicates failure isolation."
                ),
            }
            for c in all_cycles
        ]

        # Scan for components with high incoming dependencies
        high_ca_components = []
        for n in self.graph_client.get_nodes():
            nid = n["id"]
            m = self.graph_client.calculate_coupling_metrics(nid)
            if m["afferent_coupling"] >= 3:
                high_ca_components.append(m)

        high_ca_components.sort(key=lambda x: x["afferent_coupling"], reverse=True)

        risks: List[RiskItem] = []
        # Cycle risk
        if all_cycles:
            risks.append(
                RiskItem(
                    risk_title="Circular Microservice Dependencies Present",
                    severity="HIGH",
                    evidence={
                        "cycle_count": len(all_cycles),
                        "observed_cycles": all_cycles,
                    },
                    explanation="Circular dependency chains between microservices hinder autonomous service deployments and can lead to cascading call loops.",
                    confidence_level="HIGH",
                    assessment_basis="observed_graph_structure",
                )
            )

        # Shared datastore risk
        shared_stores = [s for s in shared_deps if s.get("type") in ["Database", "Cache"]]
        if shared_stores:
            risks.append(
                RiskItem(
                    risk_title="Shared Datastore Coupling Across Microservices",
                    severity="HIGH",
                    evidence={
                        "shared_stores_count": len(shared_stores),
                        "stores": shared_stores,
                    },
                    explanation="Multiple microservices establish direct connections to the same datastores, violating independent data encapsulation.",
                    confidence_level="HIGH",
                    assessment_basis="observed_graph_structure",
                )
            )

        recommendations = [
            RefactoringRecommendation(
                title="Break Circular Dependency Loops",
                target_components=[n for c in all_cycles for n in c],
                supporting_graph_evidence=f"Observed {len(all_cycles)} dependency cycles in sample graph.",
                intended_architectural_benefit="Restore clean acyclic dependency structure and enable independent service release cycles.",
                action_steps=[
                    "Refactor synchronous RPC dependency into asynchronous domain events.",
                    "Adopt the Saga pattern for multi-service transactions spanning order and inventory.",
                ],
            ),
            RefactoringRecommendation(
                title="Enforce Database-per-Service Boundaries",
                target_components=[s["component_id"] for s in shared_stores],
                supporting_graph_evidence=f"{len(shared_stores)} datastores have multiple accessing microservices in sample graph.",
                intended_architectural_benefit="Encapsulate schema ownership and prevent cross-service database lock contention.",
                action_steps=[
                    "Migrate direct database connections to service-owned REST or gRPC APIs.",
                    "Split shared database tables into dedicated per-service storage instances.",
                ],
            ),
        ]

        summary = (
            f"Global architecture analysis of {self.GRAPH_SOURCE_LABEL}. "
            f"The graph contains {schema.get('total_nodes', 0)} components and {schema.get('total_edges', 0)} connections. "
            f"Identified {len(all_cycles)} circular dependency loops and {len(shared_deps)} shared dependencies."
        )

        return ArchitectureAnalysisResult(
            analysis_type="global_architecture",
            graph_source=self.GRAPH_SOURCE_LABEL,
            summary=summary,
            cycles=cycles_summary,
            shared_dependencies=shared_deps,
            risks=risks,
            recommendations=recommendations,
            limitations=self.DEFAULT_LIMITATIONS,
            is_valid=True,
        )

    def _find_shared_dependencies(self, target_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Identify shared datastores, modules, or services with multiple incoming connections."""
        all_edges = self.graph_client.get_relationships()
        inbound_map: Dict[str, List[str]] = {}

        for edge in all_edges:
            src = edge["source"]
            tgt = edge["target"]
            inbound_map.setdefault(tgt, []).append(src)

        shared_list: List[Dict[str, Any]] = []
        for comp_id, callers in inbound_map.items():
            callers_unique = sorted(list(set(callers)))
            if len(callers_unique) >= 2:
                node = self.graph_client.get_node(comp_id) or {}
                node_type = node.get("type", "Component")
                node_name = node.get("name", comp_id)

                # If target_id specified, include only if target is the shared component or a caller
                if target_id and comp_id != target_id and target_id not in callers_unique:
                    continue

                shared_list.append({
                    "component_id": comp_id,
                    "component_name": node_name,
                    "type": node_type,
                    "accessing_components": callers_unique,
                    "access_count": len(callers_unique),
                })

        shared_list.sort(key=lambda x: x["access_count"], reverse=True)
        return shared_list

    def _evaluate_risks(
        self,
        target_id: str,
        target_name: str,
        target_type: str,
        coupling: Dict[str, Any],
        blast_data: Dict[str, Any],
        involved_cycles: List[Dict[str, Any]],
        shared_dependencies: List[Dict[str, Any]],
    ) -> List[RiskItem]:
        """Construct calibrated, evidence-backed architectural risk assessments."""
        risks: List[RiskItem] = []
        ca = coupling.get("afferent_coupling", 0)
        ce = coupling.get("efferent_coupling", 0)
        direct_callers = blast_data.get("direct_dependents", [])
        affected_services = blast_data.get("affected_services", [])
        total_affected = blast_data.get("total_affected_count", 0)

        # Risk 1: High Inbound Coupling (Blast Radius Severity)
        if ca >= 4:
            risks.append(
                RiskItem(
                    risk_title=f"High Inbound Coupling on '{target_name}'",
                    severity="HIGH",
                    evidence={
                        "target_node_id": target_id,
                        "afferent_coupling_Ca": ca,
                        "direct_dependents": direct_callers,
                        "total_affected_downstream_components": total_affected,
                    },
                    explanation=(
                        f"Component '{target_id}' has {ca} direct incoming dependencies in the sample graph. "
                        f"In an enterprise system, modifying high-afferent components may propagate breaking changes "
                        f"across {total_affected} downstream nodes unless decoupled with isolation layers."
                    ),
                    confidence_level="HIGH",
                    assessment_basis="observed_graph_structure",
                )
            )
        elif ca >= 2:
            risks.append(
                RiskItem(
                    risk_title=f"Moderate Inbound Coupling on '{target_name}'",
                    severity="MEDIUM",
                    evidence={
                        "target_node_id": target_id,
                        "afferent_coupling_Ca": ca,
                        "direct_dependents": direct_callers,
                    },
                    explanation=f"Multiple components ({len(direct_callers)}) depend directly on '{target_id}'.",
                    confidence_level="MEDIUM",
                    assessment_basis="observed_graph_structure",
                )
            )

        # Risk 2: Circular Dependency Involvement
        target_cycles = [c for c in involved_cycles if c.get("involves_target")]
        if target_cycles:
            cycle_nodes = target_cycles[0].get("cycle_nodes", [])
            risks.append(
                RiskItem(
                    risk_title=f"Direct Involvement in Circular Dependency Loop",
                    severity="HIGH",
                    evidence={
                        "participating_cycle": cycle_nodes,
                    },
                    explanation=(
                        f"Component '{target_id}' participates in a circular dependency loop ({' <-> '.join(cycle_nodes)}). "
                        "Circular dependencies impede atomic deployments and create cyclic failure modes."
                    ),
                    confidence_level="HIGH",
                    assessment_basis="observed_graph_structure",
                )
            )

        # Risk 3: Shared Storage Coupling
        target_shared_stores = [s for s in shared_dependencies if s.get("type") in ["Database", "Cache"]]
        if target_shared_stores:
            risks.append(
                RiskItem(
                    risk_title="Shared Datastore Coupling Detected",
                    severity="HIGH" if len(target_shared_stores) >= 2 else "MEDIUM",
                    evidence={
                        "shared_datastores": target_shared_stores,
                    },
                    explanation=(
                        f"Component '{target_id}' shares storage with other services "
                        f"({', '.join([s['component_id'] for s in target_shared_stores])}). "
                        "Shared datastores create hidden database coupling that bypasses service API contracts."
                    ),
                    confidence_level="HIGH",
                    assessment_basis="observed_graph_structure",
                )
            )

        # Risk 4: High Outbound Coupling (High Instability)
        if ce >= 5:
            risks.append(
                RiskItem(
                    risk_title=f"High Outbound Coupling (Instability) on '{target_name}'",
                    severity="MEDIUM",
                    evidence={
                        "target_node_id": target_id,
                        "efferent_coupling_Ce": ce,
                        "instability_index": coupling.get("instability", 0.0),
                    },
                    explanation=(
                        f"Component '{target_id}' depends on {ce} external components. "
                        "Components with high efferent coupling are volatile and susceptible to external changes."
                    ),
                    confidence_level="MEDIUM",
                    assessment_basis="inferred_architectural_implication",
                )
            )

        return risks

    def _generate_recommendations(
        self,
        target_id: str,
        target_name: str,
        target_type: str,
        blast_data: Dict[str, Any],
        involved_cycles: List[Dict[str, Any]],
        shared_dependencies: List[Dict[str, Any]],
        risks: List[RiskItem],
    ) -> List[RefactoringRecommendation]:
        """Produce concrete, graph-grounded refactoring recommendations."""
        recs: List[RefactoringRecommendation] = []
        direct_callers = blast_data.get("direct_dependents", [])
        affected_services = blast_data.get("affected_services", [])
        total_affected = blast_data.get("total_affected_count", 0)

        # Recommendation 1: Decouple direct dependents
        if direct_callers:
            recs.append(
                RefactoringRecommendation(
                    title=f"Introduce Anti-Corruption Layer for '{target_name}'",
                    target_components=direct_callers,
                    supporting_graph_evidence=(
                        f"Observed {len(direct_callers)} direct callers in sample graph: {', '.join(direct_callers[:4])}."
                    ),
                    intended_architectural_benefit=(
                        "Shield upstream callers from breaking changes and permit phased, non-disruptive migration."
                    ),
                    action_steps=[
                        f"Implement an API facade or adapter intercepting calls to '{target_id}'.",
                        "Introduce feature flags to dynamically toggle between legacy and modern implementations.",
                        "Add contract tests to ensure backward compatibility during transitions.",
                    ],
                )
            )

        # Recommendation 2: Break circular dependencies if present
        if involved_cycles:
            first_cycle = involved_cycles[0].get("cycle_nodes", [])
            recs.append(
                RefactoringRecommendation(
                    title="Break Circular Dependencies Using Asynchronous Messaging",
                    target_components=first_cycle,
                    supporting_graph_evidence=(
                        f"Circular dependency path observed in sample graph: {' -> '.join(first_cycle)}."
                    ),
                    intended_architectural_benefit=(
                        "Eliminate cyclical call chains to allow autonomous service scaling and clean build boundaries."
                    ),
                    action_steps=[
                        "Convert synchronous inter-service RPC invocations to asynchronous domain events.",
                        "Apply the Saga orchestration pattern to coordinate multi-service workflows without bidirectional coupling.",
                    ],
                )
            )

        # Recommendation 3: Shared datastore remediation
        shared_stores = [s for s in shared_dependencies if s.get("type") in ["Database", "Cache"]]
        if shared_stores:
            store_ids = [s["component_id"] for s in shared_stores]
            recs.append(
                RefactoringRecommendation(
                    title="Enforce Dedicated Storage Boundaries (Database-per-Service)",
                    target_components=store_ids,
                    supporting_graph_evidence=(
                        f"{len(shared_stores)} datastore(s) are shared across multiple services: {', '.join(store_ids)}."
                    ),
                    intended_architectural_benefit=(
                        "Encapsulate private schema access and prevent concurrent lock contention across service domains."
                    ),
                    action_steps=[
                        "Expose private database queries through an authenticated internal service API.",
                        "Partition shared cache keys into isolated tenant namespaces.",
                    ],
                )
            )

        return recs

