# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import torch
from transformers import TapasTokenizer, TapasForQuestionAnswering, TapasConfig
#from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
from transformers import pipeline
import pandas as pd
import os
    
TASK_CLASS = "table-question-answering"
MODEL_NAME = "google/tapas-large-finetuned-wtq"
MODEL_CACHE = "model-cache"
TOKEN_CACHE = "token-cache"

#tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")
#tsqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-sqa")
#mstqa = pipeline(task="table-question-answering", model="microsoft/tapex-large-finetuned-wikisql")
#mswtqa = pipeline(task="table-question-answering", model="microsoft/tapex-large-finetuned-wtq")

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        self.tokenizer0 = TapasTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            cache_dir=TOKEN_CACHE
        )
        #config = TapasConfig(num_aggregation_labels=3, average_logits_per_cell=True)
        self.model0 = TapasForQuestionAnswering.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            cache_dir=MODEL_CACHE,
            #config=config
        )
        self.model0 = self.model0.to("cuda")

    def predict(
        self,
        query: str = Input(
            description="Your question.", 
            default="What age was Charles Alexander Fortune?",
            ),
        userFileType: str = Input(
            default="csv",
            choices=["csv", "excel", "json"],
            description="File type",
            ),
        userFile: Path = Input(
            description="Upload a file",
            ),
        numRows: int = Input(
            default=35,
            ge=1,
            le=200,
            description="Number of rows to scan - can't handle too many",
            ),
        #getFileFromURL: bool = Input(
        #    description="Uploading from a link?", 
        #    default=False
        #    ),
        #userFileURL: str = Input(
        #    description="link to file", 
        #    default="https://raw.githubusercontent.com/GeorgeDavila/cog-TableQA/main/titanic.csv"
        #    ),
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
