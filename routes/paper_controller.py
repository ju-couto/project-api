from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List

from db import get_db, Session

from sql_app import schemas

router = APIRouter()
