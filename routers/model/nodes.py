from typing import Literal, Optional, Union
from pydantic import BaseModel

from utils.data_processing import handle_missing_values
from utils.io_utils import read_file

class BaseNode(BaseModel):
    id: str
    name: str
    type: Literal['DRAFT', 'DATA', 'TRANSFORMER', 'PRESENTATION']

class DraftNode(BaseNode):
    type: Literal['DRAFT']

    def validate(self):
        return True
    
    def run(self):
        pass

class DataNode(BaseNode):
    type: Literal['DATA']
    dataType: Literal['LOAD_FILE']

    def validate(self):
        return True

class LoadFileNode(DataNode):
    dataType: Literal['LOAD_FILE']
    fileId: Optional[str] = None

    def validate(self):
        if not super().validate():
            return False

        if self.fileId is None:
            return False
        
        return True
    
    def run(self, filePath):
        return read_file(filePath, 'csv', header=False)

class TransformerNode(BaseNode):
    type: Literal['TRANSFORMER']
    action: Literal['FILL_WITH_ZERO']
    fromNodeId: Optional[str] = None

    def validate(self):
        if self.fromNodeId is None:
            return False

        return True

class FillWithZeroNode(TransformerNode):
    action: Literal['FILL_WITH_ZERO']

    def validate(self):
        if not super().validate():
            return False

        return True
    
    def run(self, prevNodeData):
        return prevNodeData.fill_null(strategy="zero")

class PresentationNode(BaseNode):
    type: Literal['PRESENTATION']
    action: Literal['SAVE_TO_FILE']
    fromNodeId: Optional[str] = None

    def validate(self):
        if self.fromNodeId is None:
            return False

        return True

class SaveToFileNode(PresentationNode):
    action: Literal['SAVE_TO_FILE']
    filePath: Optional[str] = None

    def validate(self):
        if not super().validate():
            return False

        if self.filePath is None:
            return False

        return True
    
    def run(self, prevNodeData):
        prevNodeData.write_csv(self.filePath, include_header=False)

class CanvasRequestDto(BaseModel):
    nodes: list[Union[DraftNode, LoadFileNode, FillWithZeroNode, SaveToFileNode]]
