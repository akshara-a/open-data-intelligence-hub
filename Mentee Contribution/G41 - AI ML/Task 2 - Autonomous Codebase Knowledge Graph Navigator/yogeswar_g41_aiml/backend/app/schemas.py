from typing import Optional, List
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900


class MessageResponse(BaseModel):
    message: str


class CreateRepoRequest(BaseModel):
    name: str
    git_url: str
    default_branch: str = "main"


class IngestRequest(BaseModel):
    commit_sha: str


class RepoResponse(BaseModel):
    repo_id: str
    name: str
    git_url: str
    default_branch: str = "main"
    status: str = "ACTIVE"
    created_at: Optional[str] = None


class SnapshotResponse(BaseModel):
    repo_id: str
    commit_sha: str
    created_at: Optional[str] = None


class JobStatusResponse(BaseModel):
    job_id: str
    repo_id: str
    commit_sha: str
    job_type: str
    status: str
    progress: int = 0
    log_output: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    service: str
    database: str
    timestamp: str


# ============================================================================
# Phase 7.3: RBAC & User Management Schemas
# ============================================================================

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: str
    is_active: bool
    created_at: Optional[str] = None


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="Username")
    password: str = Field(..., min_length=6, description="Initial password")
    role: str = Field("viewer", description="Role: admin, reviewer, or viewer")


class UpdateUserStatusRequest(BaseModel):
    is_active: bool


class UpdateUserRoleRequest(BaseModel):
    role: str = Field(..., description="Role: admin, reviewer, or viewer")


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=6, description="New password")


class RepoMemberResponse(BaseModel):
    id: str
    user_id: str
    username: str
    role: str
    created_at: Optional[str] = None


class AddRepoMemberRequest(BaseModel):
    user_id: str
    role: str = Field("reviewer", description="Role: reviewer or viewer")
