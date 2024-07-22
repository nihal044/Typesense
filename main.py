from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import typesense

client = typesense.Client({
    'nodes': [{
        'host': 'zesyao0hmni891d2p-1.a1.typesense.net',
        'port': '443',
        'protocol': 'https'
    }],
    'api_key': 'gFEXTdd67BicSxYxFnbWiJ9bDTccpW2K',
    'connection_timeout_seconds': 10 
})
app = FastAPI()

class SearchQuery(BaseModel):
    query: str

@app.post("/search")
async def search_documents(search_query: SearchQuery):
    try:
        search_parameters = {
            'q': search_query.query,
            'query_by': 'title,author,content',
        }
        search_results = client.collections['documents'].documents.search(search_parameters)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

