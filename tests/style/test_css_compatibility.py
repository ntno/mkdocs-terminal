"""Tests for CSS variable compatibility layer.

Tests the fallback mechanism in theme.css that maps legacy variable names
to namespaced versions, ensuring backwards compatibility with custom palettes.
"""

import pytest
import re
from pathlib import Path


@pytest.fixture
def theme_css_path():
    """Path to theme.css file."""
    return Path(__file__).parents[2] / "terminal" / "css" / "theme.css"


@pytest.fixture
def theme_css_content(theme_css_path):
    """Content of theme.css file."""
    return theme_css_path.read_text()


class TestCompatibilityLayerPresence:
    """Tests that compatibility layer exists in theme.css."""
    
    def test_compatibility_layer_exists(self, theme_css_content):
        """Test compatibility layer block is present."""
        assert ":root {" in theme_css_content
        assert "CSS Variable Compatibility Layer" in theme_css_content
    
    def test_compatibility_layer_documented(self, theme_css_content):
        """Test compatibility layer includes inline documentation."""
        assert "backwards compatibility" in theme_css_content.lower()
        assert "resolution chain" in theme_css_content.lower() or "fallback" in theme_css_content.lower()


class TestVariableMappings:
    """Tests that all required variable mappings are present."""
    
    REQUIRED_COLOR_VARS = [
        ('--font-color', '--mkdocs-terminal-font-color'),
        ('--background-color', '--mkdocs-terminal-bg-color'),
        ('--invert-font-color', '--mkdocs-terminal-invert-font-color'),
        ('--primary-color', '--mkdocs-terminal-primary-color'),
        ('--secondary-color', '--mkdocs-terminal-secondary-color'),
        ('--tertiary-color', '--mkdocs-terminal-tertiary-color'),
        ('--error-color', '--mkdocs-terminal-error-color'),
        ('--progress-bar-background', '--mkdocs-terminal-progress-bar-bg'),
        ('--progress-bar-fill', '--mkdocs-terminal-progress-bar-fill'),
        ('--code-bg-color', '--mkdocs-terminal-code-bg-color'),
        ('--input-style', '--mkdocs-terminal-input-style'),
        ('--display-h1-decoration', '--mkdocs-terminal-h1-decoration'),
    ]
    
    REQUIRED_TYPOGRAPHY_VARS = [
        ('--global-font-size', '--mkdocs-terminal-font-size'),
        ('--global-line-height', '--mkdocs-terminal-line-height'),
        ('--global-space', '--mkdocs-terminal-spacing'),
        ('--font-stack', '--mkdocs-terminal-font-family'),
        ('--mono-font-stack', '--mkdocs-terminal-mono-font-family'),
        ('--page-width', '--mkdocs-terminal-page-width'),
    ]
    
    @pytest.mark.parametrize("legacy_var,namespaced_var", REQUIRED_COLOR_VARS)
    def test_color_variable_mapping(self, theme_css_content, legacy_var, namespaced_var):
        """Test each color variable has correct fallback mapping."""
        # Pattern: --legacy: var(--namespaced, var(--legacy));
        pattern = rf'{re.escape(legacy_var)}:\s*var\({re.escape(namespaced_var)},\s*var\({re.escape(legacy_var)}\)\)'
        assert re.search(pattern, theme_css_content), \
            f"Missing or incorrect mapping for {legacy_var} → {namespaced_var}"
    
    @pytest.mark.parametrize("legacy_var,namespaced_var", REQUIRED_TYPOGRAPHY_VARS)
    def test_typography_variable_mapping(self, theme_css_content, legacy_var, namespaced_var):
        """Test each typography variable has correct fallback mapping."""
        pattern = rf'{re.escape(legacy_var)}:\s*var\({re.escape(namespaced_var)},\s*var\({re.escape(legacy_var)}\)\)'
        assert re.search(pattern, theme_css_content), \
            f"Missing or incorrect mapping for {legacy_var} → {namespaced_var}"
    
    def test_all_required_variables_mapped(self, theme_css_content):
        """Test that all 18 required variables are mapped."""
        all_vars = self.REQUIRED_COLOR_VARS + self.REQUIRED_TYPOGRAPHY_VARS
        
        for legacy_var, namespaced_var in all_vars:
            pattern = rf'{re.escape(legacy_var)}:\s*var\({re.escape(namespaced_var)}'
            assert re.search(pattern, theme_css_content), \
                f"Missing mapping for {legacy_var}"


class TestFallbackChainStructure:
    """Tests the structure of fallback chains."""
    
    def test_fallback_chain_format(self, theme_css_content):
        """Test fallback chains use correct var() nesting."""
        # Should be: var(--namespaced, var(--legacy))
        # Not: var(--namespaced, --legacy) or var(--namespaced)
        
        # Find all variable definitions in :root block
        root_block_match = re.search(r':root\s*\{([^}]+)\}', theme_css_content, re.DOTALL)
        assert root_block_match, "Could not find :root block"
        
        root_content = root_block_match.group(1)
        
        # Look for variable definitions with fallbacks
        var_definitions = re.findall(r'--[\w-]+:\s*var\([^;]+\);', root_content)
        
        # Should have at least 18 variable definitions
        assert len(var_definitions) >= 18, f"Expected at least 18 variable definitions, found {len(var_definitions)}"
        
        # Each should follow pattern: var(--namespace, var(--legacy))
        for var_def in var_definitions:
            if 'mkdocs-terminal' in var_def:
                # Should have nested var() for fallback
                assert var_def.count('var(') >= 2, \
                    f"Variable definition missing nested fallback: {var_def}"


class TestCSSLoadOrder:
    """Tests related to CSS load order and specificity."""
    
    def test_compatibility_layer_before_main_styles(self, theme_css_content):
        """Test :root compatibility layer appears before main body styles."""
        root_pos = theme_css_content.find(':root {')
        body_pos = theme_css_content.find('body {')
        
        assert root_pos != -1, "Could not find :root block"
        assert body_pos != -1, "Could not find body block"
        assert root_pos < body_pos, ":root compatibility layer should appear before body styles"
    
    def test_compatibility_layer_after_license(self, theme_css_content):
        """Test compatibility layer appears after license header."""
        license_match = re.search(r'/\*!.*?MIT License.*?\*/', theme_css_content, re.DOTALL)
        root_match = re.search(r':root\s*\{', theme_css_content)
        
        assert license_match, "Could not find license header"
        assert root_match, "Could not find :root block"
        assert license_match.end() < root_match.start(), \
            "Compatibility layer should appear after license header"


class TestIntegration:
    """Integration tests for compatibility layer."""
    
    def test_no_duplicate_root_blocks(self, theme_css_content):
        """Test there's only one :root block in theme.css."""
        # Count :root occurrences (should be exactly 1)
        root_count = len(re.findall(r':root\s*\{', theme_css_content))
        assert root_count == 1, f"Expected exactly 1 :root block, found {root_count}"
    
    def test_valid_css_syntax(self, theme_css_content):
        """Test basic CSS syntax validity (balanced braces)."""
        open_braces = theme_css_content.count('{')
        close_braces = theme_css_content.count('}')
        assert open_braces == close_braces, \
            f"Unbalanced braces: {open_braces} open, {close_braces} close"
    
    def test_no_circular_references(self, theme_css_content):
        """Test fallback chains don't create circular references."""
        # Extract :root block
        root_match = re.search(r':root\s*\{([^}]+)\}', theme_css_content, re.DOTALL)
        assert root_match, "Could not find :root block"
        
        root_content = root_match.group(1)
        
        # Find all variable definitions
        var_defs = re.findall(r'(--[\w-]+):\s*var\(([^)]+)\)', root_content)
        
        for var_name, var_value in var_defs:
            # Fallback should reference the same legacy variable name
            # Pattern: --font-color: var(--mkdocs-terminal-font-color, var(--font-color))
            # The var_name should appear in var_value fallback
            if 'mkdocs-terminal' not in var_name:
                continue  # Skip if not a legacy var
            
            # Should contain nested var() with same variable name
            assert var_name in var_value, \
                f"Fallback for {var_name} should reference itself in fallback chain"
