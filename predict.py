# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
from pylatex.section import Chapter, Paragraph, Subparagraph

def fill_document(doc, chapterTitleString, text2type):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    text2type = str(text2type)
    chapterTitle = str(chapterTitleString)
    
    with doc.create(Section(chapterTitle)):
        doc.append(text2type)

class Predictor(BasePredictor):
    def setup(self) -> None:
        pass

    def predict(
        self,
        chapterTitleInput: str = Input(
            description="Title", 
            default="Report",
            ),
        textInput: str = Input(
            description="Text to enter into the document.", 
            default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            ),
        #userFile: Path = Input(
        #    description="Upload a tex file",
        #    ),
    ) -> str:
        """Run a single prediction on the model"""

        documentName = "generated"
        doc = Document(documentName)
        fill_document(doc, chapterTitleInput, textInput)

        doc.generate_pdf(clean_tex=False)
        doc.generate_tex()

        output_path = Path(f"{documentName}.pdf")
        return output_path
