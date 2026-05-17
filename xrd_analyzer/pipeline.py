# SPDX-License-Identifier: MIT
"""Scripting API for headless integration, compatible with Dioptas project files."""

from .model.DioptasModel import DioptasModel


class Pipeline:
    """Headless integration pipeline.

    Load a Dioptas/DIO project file and integrate images without the GUI.

    Example:
        p = Pipeline.from_project("experiment.dio")
        pattern = p.integrate("sample_001.tiff")
        pattern.save("sample_001.xy")
    """

    def __init__(self):
        self.model = DioptasModel()

    @classmethod
    def from_project(cls, project_path: str) -> "Pipeline":
        p = cls()
        p.model.load(project_path)
        return p

    def integrate(self, image_path: str):
        """Integrate a single image and return the Pattern."""
        self.model.img_model.load(image_path)
        return self.model.pattern

    def integrate_batch(self, glob_pattern: str):
        """Batch integrate images matching a glob pattern."""
        import glob as _glob
        patterns = []
        for f in sorted(_glob.glob(glob_pattern)):
            pattern = self.integrate(f)
            patterns.append(pattern)
        return patterns

    def load_mask(self, mask_path: str):
        """Override the mask."""
        self.model.mask_model.load(mask_path)

    @property
    def current_configuration(self):
        return self.model.current_configuration
