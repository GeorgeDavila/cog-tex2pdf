# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

def fill_document(doc, text2type):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    text2type = str(text2type)
    
    with doc.create(Section('A section')):
        doc.append(text2type)
        #doc.append(italic(text2type))

        #with doc.create(Subsection('A subsection')):
        #    doc.append('Also some crazy characters: $&#{}')

class Predictor(BasePredictor):
    def setup(self) -> None:
        pass

    def predict(
        self,
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
        fill_document(doc, textInput)

        doc.generate_pdf(clean_tex=False)
        doc.generate_tex()

        output_path = Path(f"{documentName}.pdf")
        return output_path
