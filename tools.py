## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

# Corrected: SerperDevTool is imported directly from crewai_tools in this version
from crewai_tools import BaseTool, SerperDevTool 

from langchain_community.document_loaders import PyPDFLoader

## Creating search tool (standard CrewAI tool)
search_tool = SerperDevTool()

## Creating custom PDF reader tool using BaseTool
class BloodReportReaderTool(BaseTool):
    name: str = "Blood Report Reader" # Name the agent will use
    description: str = "Reads data from a PDF file at a given path. Input is the file path string." # Description for the agent

    def _run(self, file_path: str = 'data/sample.pdf') -> str:
        """
        Reads data from a PDF file at a given path.
        Args:
            file_path (str): Path of the PDF file. Defaults to 'data/sample.pdf'.
        Returns:
            str: Full Blood Test report content as a string.
        """
        try:
            docs = PyPDFLoader(file_path=file_path).load()
        except Exception as e:
            return f"Error loading PDF file: {e}"

        full_report = ""
        for data in docs:
            content = data.page_content
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"
        return full_report

## Creating Nutrition Analysis Tool as a BaseTool
class NutritionAnalysisTool(BaseTool):
    name: str = "Nutrition Analysis Tool"
    description: str = "Analyzes blood report data to provide nutrition recommendations. Input is the blood report text as a string."

    def _run(self, blood_report_data: str) -> str:
        # Process and analyze the blood report data
        processed_data = blood_report_data

        # Simple cleanup (actual analysis logic to be implemented)
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
        
        # TODO: Implement actual nutrition analysis logic here based on processed_data
        # For now, returning a snippet to show it processed something
        return f"Nutrition analysis functionality to be implemented. Processed data snippet: {processed_data[:500]}..."

## Creating Exercise Planning Tool as a BaseTool
class ExercisePlanningTool(BaseTool):
    name: str = "Exercise Planning Tool"
    description: str = "Creates an exercise plan based on blood report data and user needs. Input is the blood report text as a string."

    def _run(self, blood_report_data: str) -> str:
        # TODO: Implement actual exercise planning logic here based on blood_report_data
        # For now, returning a snippet
        return f"Exercise planning functionality to be implemented. Processed data snippet: {blood_report_data[:500]}..."