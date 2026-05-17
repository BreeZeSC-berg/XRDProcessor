# CLAUDE.md

## Project Overview

XRD Analyzer is a GUI program for fast analysis of powder X-ray diffraction images. It provides calibration, masking, pattern integration, phase line overlays, and batch processing capabilities. 

**This project replicates all functionality of Dioptas but with a completely redesigned UI.**

## UI Differences from Dioptas

- **Top tab navigation bar** (blue) instead of left vertical button strip
- **Light theme** (light blue/white) instead of dark orange
- **Integrated toolbar** with project actions below the tab bar
- **Modern card-style panels** with different spacing and typography
- **CSS-based styling** via `resources/style/xrd_analyzer.css`

## Architecture (MVC)

```
xrd_analyzer/
├── model/              # Data layer - pure Python, no Qt (IDENTICAL to Dioptas)
├── controller/         # Controller layer - connects models to widgets
├── widgets/            # View layer - COMPLETELY REDESIGNED UI
├── resources/          # Static resources
└── pipeline.py         # Scripting API
```

## Key differences from Dioptas (widget layer)

- `MainWidget.py` - Top tab bar navigation instead of left sidebar buttons
- `integration/__init__.py` - Modern 3-panel layout with different splitter ratios
- CSS theme: `resources/style/light_blue.xml` + `resources/style/xrd_analyzer.css`
- Settings stored in `~/.XrdAnalyzer` instead of `~/.Dioptas`

## Running

```bash
python run_xrd.py
```

## Controller Compatibility

Widget shortcut names are preserved identically so all controllers work without modification. Only the visual presentation differs.
