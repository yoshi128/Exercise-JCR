from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

app = FastAPI(title="Feature Voting API - JCR", version="1.0.0")

# Dev CORS: allow all; tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database setup (SQLite file in backend/) ---
DATABASE_URL = "sqlite:///./feature_voting.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    votes = relationship("Vote", back_populates="feature", cascade="all, delete")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=False)
    feature = relationship("Feature", back_populates="votes")

Base.metadata.create_all(bind=engine)

# --- Pydantic schemas ---
class FeatureCreate(BaseModel):
    title: str
    description: str | None = None

class FeatureOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    votes: int
    class Config:
        from_attributes = True

# --- Routes ---
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/features", response_model=List[FeatureOut])
def list_features():
    db = SessionLocal()
    try:
        rows = (
            db.query(Feature.id, Feature.title, Feature.description, func.count(Vote.id).label("votes"))
              .outerjoin(Vote, Vote.feature_id == Feature.id)
              .group_by(Feature.id)
              .order_by(func.count(Vote.id).desc(), Feature.id.asc())
              .all()
        )
        return [FeatureOut(id=r.id, title=r.title, description=r.description, votes=r.votes) for r in rows]
    finally:
        db.close()

@app.post("/features", response_model=FeatureOut, status_code=201)
def create_feature(payload: FeatureCreate):
    db = SessionLocal()
    try:
        f = Feature(title=payload.title, description=payload.description)
        db.add(f)
        db.commit()
        db.refresh(f)
        return FeatureOut(id=f.id, title=f.title, description=f.description, votes=0)
    finally:
        db.close()

@app.post("/features/{feature_id}/upvote", response_model=FeatureOut)
def upvote_feature(feature_id: int):
    db = SessionLocal()
    try:
        f = db.query(Feature).get(feature_id)
        if not f:
            raise HTTPException(status_code=404, detail="Feature not found")
        db.add(Vote(feature_id=f.id))
        db.commit()
        count = db.query(func.count(Vote.id)).filter(Vote.feature_id == f.id).scalar()
        return FeatureOut(id=f.id, title=f.title, description=f.description, votes=count)
    finally:
        db.close()
