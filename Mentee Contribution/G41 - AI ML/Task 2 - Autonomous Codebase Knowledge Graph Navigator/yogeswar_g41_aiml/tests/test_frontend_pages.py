import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_eight_dashboard_pages_specification():
    """Validates AC-1.2: All eight required React dashboard pages exist with Section 3.1 required components"""
    pages_dir = ROOT_DIR / "frontend" / "src" / "pages"
    assert pages_dir.is_dir()

    required_pages = {
        "DashboardPage.tsx": ["RepoCardGrid", "RecentQueriesList", "SystemHealthIndicator"],
        "RepoExplorerPage.tsx": ["VirtualFileTree", "EntityDetailDrawer", "CodeViewerModal"],
        "KnowledgeGraphPage.tsx": ["CytoscapeGraphCanvas", "GraphFilterToolbar", "EvidencePopover"],
        "AssistantPage.tsx": ["ChatTranscript", "PromptInputBox", "CollapsibleEvidenceDrawer"],
        "ImpactAnalysisPage.tsx": ["EntitySelector", "ImpactSubGraphView", "DynamicInferenceMatrix", "ExportActionToolbar"],
        "ReportViewerPage.tsx": ["MarkdownReportRenderer", "EvidenceReferenceTable", "DownloadPdfButton"],
        "EvaluationPage.tsx": ["BenchmarkRunTrigger", "LatencyChart", "MetricScoreTable", "RunHistoryList"],
        "SettingsPage.tsx": ["RepoAccessManager", "TokenExpiryView", "NotificationPreferences"],
    }

    for page_file, required_components in required_pages.items():
        file_path = pages_dir / page_file
        assert file_path.is_file(), f"Page {page_file} must exist in src/pages"
        content = file_path.read_text(encoding="utf-8")
        for comp in required_components:
            assert comp in content, f"Component {comp} must be present in {page_file}"


def test_snapshot_context_binding():
    """Validates AC-1.2: Snapshot context provider and active snapshot binding"""
    ctx_file = ROOT_DIR / "frontend" / "src" / "context" / "SnapshotContext.tsx"
    assert ctx_file.is_file()
    ctx_content = ctx_file.read_text(encoding="utf-8")
    assert "activeRepoId" in ctx_content
    assert "activeCommitSha" in ctx_content
    assert "setActiveSnapshot" in ctx_content

    app_file = ROOT_DIR / "frontend" / "src" / "App.tsx"
    assert app_file.is_file()
    app_content = app_file.read_text(encoding="utf-8")
    assert "useSnapshot" in app_content
    assert "Active Snapshot:" in app_content


def test_frontend_build_artifacts():
    """Validates that Vite build generated production bundle without error"""
    dist_dir = ROOT_DIR / "frontend" / "dist"
    assert dist_dir.is_dir(), "frontend/dist directory must exist after build"
    index_html = dist_dir / "index.html"
    assert index_html.is_file(), "frontend/dist/index.html must exist"
    assets_dir = dist_dir / "assets"
    assert assets_dir.is_dir(), "frontend/dist/assets must exist"
    js_files = list(assets_dir.glob("*.js"))
    assert len(js_files) > 0, "At least one bundled JavaScript asset must be produced"
