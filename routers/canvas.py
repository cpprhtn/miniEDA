from typing import Optional, Literal, Union, List, Set
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from routers.model.nodes import (
    CanvasRequestDto,
    DraftNode,
    LoadFileNode,
    FillWithZeroNode,
    SaveToFileNode,
    TransformerNode,
    PresentationNode,
)
from utils import id_generator

canvasRouter = APIRouter()


class NodeWrapper:
    def __init__(self, node):
        self.done = False
        self.data = None
        self.node = node


def validate_nodes(dto: CanvasRequestDto) -> List[str]:
    return [node.id for node in dto.nodes if not node.validate()]


@canvasRouter.post("/canvas/file")
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_id = id_generator.createId()
    file_path = file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    request.app.state.fileDict[file_id] = file_path

    return JSONResponse({"fileId": file_id})


@canvasRouter.post("/canvas/run")
async def run_canvas(dto: CanvasRequestDto, request: Request):
    error_node_ids = validate_nodes(dto)

    if error_node_ids:
        raise HTTPException(status_code=400, detail={
            "message": "Invalid nodes",
            "errorNodeIds": error_node_ids,
        })

    node_dict = {node.id: NodeWrapper(node) for node in dto.nodes}
    unprocessed_nodes: Set[str] = set(node_dict.keys())

    dependency_dict = {}
    for node in dto.nodes:
        if isinstance(node, (TransformerNode, PresentationNode)):
            dependency_dict.setdefault(node.fromNodeId, []).append(node.id)

    while unprocessed_nodes:
        executable_nodes = [
            node_id for node_id in unprocessed_nodes
            if node_id not in {dep for deps in dependency_dict.values() for dep in deps}
        ]

        if not executable_nodes:
            raise HTTPException(status_code=400, detail="Circular dependency detected")

        for node_id in executable_nodes:
            wrapper = node_dict[node_id]
            node = wrapper.node

            if isinstance(node, LoadFileNode):
                wrapper.data = node.run(request.app.state.fileDict[node.fileId])
            elif isinstance(node, TransformerNode):
                from_node = node_dict[node.fromNodeId]
                wrapper.data = node.run(from_node.data)
            elif isinstance(node, PresentationNode):
                from_node = node_dict[node.fromNodeId]
                node.run(from_node.data)

            wrapper.done = True
            unprocessed_nodes.remove(node_id)
            dependency_dict.pop(node_id, None)

    request.app.state.fileDict = {}
    result = {node.id: str(node_dict[node.id].data) for node in dto.nodes if node_dict[node.id].data is not None}
    
    return JSONResponse(result)


class NodeCreateDto(BaseModel):
    id: str
    name: str
    type: Literal["DRAFT", "DATA", "TRANSFORMER", "PRESENTATION"]
    dataType: Optional[Literal["LOAD_FILE"]] = None
    action: Optional[Literal["FILL_WITH_ZERO", "SAVE_TO_FILE"]] = None
    fileId: Optional[str] = None
    fromNodeId: Optional[str] = None
    filePath: Optional[str] = None


@canvasRouter.post("/canvas/create-node")
async def create_node(dto: NodeCreateDto):
    node = None
    if dto.type == "DRAFT":
        node = DraftNode(id=dto.id, name=dto.name, type=dto.type)
    elif dto.type == "DATA" and dto.dataType == "LOAD_FILE":
        node = LoadFileNode(id=dto.id, name=dto.name, type=dto.type, dataType=dto.dataType, fileId=dto.fileId)
    elif dto.type == "TRANSFORMER" and dto.action == "FILL_WITH_ZERO":
        node = FillWithZeroNode(id=dto.id, name=dto.name, type=dto.type, action=dto.action, fromNodeId=dto.fromNodeId)
    elif dto.type == "PRESENTATION" and dto.action == "SAVE_TO_FILE":
        node = SaveToFileNode(id=dto.id, name=dto.name, type=dto.type, action=dto.action, fromNodeId=dto.fromNodeId, filePath=dto.filePath)
    else:
        raise HTTPException(status_code=400, detail="Invalid node type or action")

    if not node.validate():
        raise HTTPException(status_code=400, detail="Invalid node configuration")

    return JSONResponse(content=node.dict())
