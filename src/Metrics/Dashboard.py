import streamlit as st
from pathlib import Path
from typing import Iterable, Literal, Callable, Dict
from Metrics.DashboardGeneralLogs import GeneralData_Window
from Metrics.DashboardAnalysisLogs import Analysis_Window
from Metrics.AnalysisLogs import AnalysisLogs

Mode = Literal["General Data", "Logs Analysis"]
class LogsDashboard:
    MODE_GENERAL: Mode = "General Data"
    MODE_ANALYSIS: Mode = "Logs Analysis"
    MODES = (MODE_GENERAL, MODE_ANALYSIS)
    PAGE_TITLE = "Logs Dashboard"
    PAGE_ICON = "📊"
    PAGE_LAYOUT: Literal["centered", "wide"] = "wide"
    LEVEL_WARNING = "### ⚠️ No JSON files found in the folder."

    def __init__(self, logs_dir: Path | None = None) -> None:
        self._logs_dir: Path = logs_dir or (Path(__file__).parent.parent / "Database" / "Logs")

    def run(self) -> None:
        self.init_page()
        files = self.get_available_json_files()
        mode = self.select_mode()
        self.render_mode(mode, files)

    def init_page(self) -> None:
        st.set_page_config(page_title=self.PAGE_TITLE, page_icon=self.PAGE_ICON, layout=self.PAGE_LAYOUT)

    def get_available_json_files(self) -> list[Path]:
        folder = self._logs_dir
        available_files = list(folder.glob("*.json"))
        if (not folder.exists()) or (not available_files):
            st.warning(f"{self.LEVEL_WARNING} {folder}")
            st.stop()
        return available_files

    def select_mode(self) -> Mode:
        return st.sidebar.selectbox("Select an option:", self.MODES)

    def render_mode(self, mode: Mode, files: Iterable[Path]) -> None:
        handlers: Dict[Mode, Callable[[], None]] = {
            self.MODE_GENERAL: (lambda: GeneralData_Window.show_general_logs_window(files)),
            self.MODE_ANALYSIS: (lambda: Analysis_Window.show_analysis_logs_window(files, AnalysisLogs.analysis_registry)),
        }

        handler = handlers.get(mode)
        if not handler:
            st.subheader(str(mode))
            st.info("This view is not available at the moment.")
            return

        try:
            handler()
        except Exception:
            st.subheader(str(mode))
            st.info("This view is not available at the moment.")

if __name__ == "__main__":
    LogsDashboard().run()
