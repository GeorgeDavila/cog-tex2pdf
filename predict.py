# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')

class Predictor(BasePredictor):
    def predict(
        self,
        userFile: Path = Input(
            description="Upload a tex file",
            ),
    ) -> str:
        """Run a single prediction on the model"""

        tqa = pipeline(TASK_CLASS, model=self.model0, tokenizer=self.tokenizer0, device=0) #-1=cpu, gpu=0 or higher
        userFile = str(userFile)
        #if getFileFromURL:
        #    userFile = userFileURL.split("/")[-1]
        #    os.system(f"wget -O {userFile} {userFileURL}")

        if userFileType == "csv":
            data = pd.read_csv(userFile).head(numRows).astype(str)
        if userFileType == "excel":
            data = pd.read_excel(userFile).head(numRows).astype(str)
        if userFileType == "json":
            data = pd.read_json(userFile).head(numRows).astype(str)
        if userFileType == "sql":
            data = pd.read_sql(userFile).head(numRows).astype(str)
        if userFileType == "html":
            data = pd.read_html(userFile).head(numRows).astype(str)

        response = tqa(table=data, query=query)
        print(str(response))

        return response
