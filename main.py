from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud.firestore_v1.base_query import FieldFilter,Or
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
app = FastAPI()


@app.get("/")
async def root():
    return get_all_docs("dbtest1")


@app.get("/specific/{collection}/{document}")
async def say_hello(collection: str, document: str):
    return get_document(collection, document)



def get_all_docs(collectionName):
    docs = (
        db.collection(collectionName)
        .stream()
    )

    documents_list = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id
        doc_data['docData'] = doc._data
        documents_list.append(doc_data)

    for doc_data in documents_list:
        print(f"Document ID: {doc_data['id']}")
        print(f"Document Data: {doc_data['docData']}")
        print()

    return documents_list


def get_document(collection_name, document_id):
    doc_ref = db.collection(collection_name).document(document_id)
    print(doc_ref)
    doc = doc_ref.get()
    print(doc)
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"Document '{document_id}' not found in collection '{collection_name}'")
        return None