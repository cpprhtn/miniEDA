from typing import cast
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse

from routers.model.nodes import CanvasRequestDto, LoadFileNode, PresentationNode, TransformerNode
from utils import id_generator

canvasRouter = APIRouter()

class NodeWrapper:
    def __init__(self, node):
        self.done = False
        self.data = None
        self.node = node

def validateNodes(dto: CanvasRequestDto):
    errorNodeIds = set()

    for node in dto.nodes:
        if not node.validate():
            errorNodeIds.add(node.id)
    
    return list(errorNodeIds)

@canvasRouter.post("/canvas/file")
async def upload_file(
    request: Request,
    file: UploadFile = File(...)
):
    fileId = id_generator.createId()
    filePath = f"files/{file.filename}"

    with open(f"files/{file.filename}", "wb") as f:
        f.write(await file.read())

    request.app.state.fileDict[fileId] = filePath

    return JSONResponse({
        "fileId": fileId,
    })

@canvasRouter.post("/canvas/run")
async def run_canvas(dto: CanvasRequestDto, request: Request):
    errorNodeIds = validateNodes(dto)

    if len(errorNodeIds) > 0:
        raise HTTPException(status_code=400, detail={"message": "Invalid nodes", "errorNodeIds": errorNodeIds})
    
    nodeDict = {}
    for node in dto.nodes:
        nodeDict[node.id] = NodeWrapper(node)
    unDoneNodes = set(nodeDict.keys())
    
    dependencyDict = {}
    for node in dto.nodes:
        if isinstance(node, TransformerNode) or isinstance(node, PresentationNode):
            if node.fromNodeId not in dependencyDict:
                dependencyDict[node.fromNodeId] = []
            dependencyDict[node.fromNodeId].append(node.id)

    while len(unDoneNodes) > 0:
        executableNodes = []

        hasDependencyNodeIds = set()
        for nodes in dependencyDict.values():
            for nodeId in nodes:
                hasDependencyNodeIds.add(nodeId)

        for nodeId in unDoneNodes:
            node = nodeDict[nodeId]
            if nodeId not in hasDependencyNodeIds:
                executableNodes.append(nodeId)
        
        if len(executableNodes) == 0:
            raise HTTPException(status_code=400, detail={"message": "Circular dependency detected"})

        for nodeId in executableNodes:
            wrapper = nodeDict[nodeId]
            wrapper.done = True

            if isinstance(wrapper.node, LoadFileNode):
                wrapper.data = wrapper.node.run(request.app.state.fileDict[wrapper.node.fileId])
            elif isinstance(wrapper.node, TransformerNode):
                fromNode = nodeDict[wrapper.node.fromNodeId]
                wrapper.data = wrapper.node.run(fromNode.data)
            elif isinstance(wrapper.node, PresentationNode):
                fromNode = nodeDict[wrapper.node.fromNodeId]
                wrapper.node.run(fromNode.data)

            unDoneNodes.remove(nodeId)
            dependencyDict.pop(nodeId, None)
    
    request.app.state.fileDict = {}

    return {}