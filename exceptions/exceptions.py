from fastapi import HTTPException

def UserNotFound():
	raise HTTPException(status_code=404, detail=f"User not found")

def UserAlreadyRegistered():
	raise HTTPException(status_code=409, detail=f"User Already Registered")

def PageNotFound():
	raise HTTPException(status_code=409, detail=f"Page Not Found")

#409 always for already present data