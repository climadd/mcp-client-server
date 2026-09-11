from pydantic import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


####################### TOOLS ####################################
## Esempio sintassi x un tool che adda 2 interi
@mcp.tool(
    name="add_ints",
    description="Add two integers together",
)
def tool_fn(
    a: int = Field(description="First number to add"),
    b: int = Field(description="Second number to add"),
) -> int:
    return a+b

# Write a tool to read a doc; input a doc's name, output its contents
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and return it as a string"
)
def read_document(
    doc_id: str = Field(description="Id of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

# Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string"
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace"),
    new_str: str = Field(description="The new text to insert in place of the old text. "),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str,new_str)

# Write a tool to return all doc id's
@mcp.tool(
    name="list_doc_names",
    description="Lists all document names, separated by commas.")
def list_doc_names() ->str:
        return ", ".join(docs.keys())

# Write a tool to return the contents of two docs
@mcp.tool(
    name="compare_documents",
    description=("Reads the contents of two documents and return it as stings, separated by newline"),
)
def compare_documents(
    doc_first_id: str = Field(description="Id of the first document to read"),
    doc_second_id: str = Field(description="Id of the second document to read"),
)-> str:
    if (doc_first_id not in docs):
        raise ValueError(f"Doc with id {doc_first_id} not found")
    if (doc_second_id not in docs):
        raise ValueError(f"Doc with id {doc_second_id} not found")
    return docs[doc_first_id]+"\n"+docs[doc_second_id]

####################### RESOURCES ####################################
# Write a resource to return all docs id's
@mcp.resource(
    "docs://documents",     #static URI
    mime_type="application/json"    #hint to our client about the return type
)
def list_docs() -> list[str]:
    return list(docs.keys())

# Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


####################### PROMPTS ####################################
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
