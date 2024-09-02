import firebase_admin
from firebase_admin import credentials, firestore, exceptions

class DatabaseHandler:
    def __init__(self, service_account_path):
        self.cred = credentials.Certificate(service_account_path)
        self.app = None
        self.db = None

    def is_connected(self):
        """Initializes the connection and checks if the connection is successful."""
        try:
            if not self.app:
                self.app = firebase_admin.initialize_app(self.cred)
                self.db = firestore.client()
            return True
        except exceptions.FirebaseError as e:
            print(f"Error connecting to Firebase: {e}")
            return False

    def create(self, collection, document_id, data):
        """Creates a new document in the specified collection."""
        if self.is_connected():
            try:
                self.db.collection(collection).document(document_id).set(data)
                print(f"Document {document_id} created successfully.")
            except Exception as e:
                print(f"Error creating document: {e}")

    def read(self, collection, document_id):
        """Reads a document from the specified collection."""
        if self.is_connected():
            try:
                doc = self.db.collection(collection).document(document_id).get()
                if doc.exists:
                    print(f"Document data: {doc.to_dict()}")
                    return doc.to_dict()
                else:
                    print(f"Document {document_id} not found.")
                    return None
            except Exception as e:
                print(f"Error reading document: {e}")
                return None

    def update(self, collection, document_id, data):
        """Updates an existing document in the specified collection."""
        if self.is_connected():
            try:
                self.db.collection(collection).document(document_id).update(data)
                print(f"Document {document_id} updated successfully.")
            except Exception as e:
                print(f"Error updating document: {e}")

    def delete(self, collection, document_id):
        """Deletes a document from the specified collection."""
        if self.is_connected():
            try:
                self.db.collection(collection).document(document_id).delete()
                print(f"Document {document_id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting document: {e}")

if __name__ == "__main__":
	DatabaseHandler({
	  apiKey: 'AIzaSyB9u95wgfFVnwlr25aed0Rdl3299MJXrZg',
	  authDomain: 'ngl-server.firebaseapp.com',
	  projectId: 'ngl-server',
	  storageBucket: 'ngl-server.appspot.com',
	  messagingSenderId: '50845412761',
	  appId: '1:50845412761:web:c45dcdecd32b472a6eb708',
	  measurementId: 'G-0KNBZG95TT'
	})