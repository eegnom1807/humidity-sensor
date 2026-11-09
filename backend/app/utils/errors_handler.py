
def handle_db_error(e):
    error_msg = str(e.orig).lower()

    if "unique" in error_msg:
        return {"message": "Resource already exists"}, 409
    
    if "foreign key" in error_msg:
        return {"message": "Invalid reference"}, 400
    
    return {"message": "Integrity error"}, 400