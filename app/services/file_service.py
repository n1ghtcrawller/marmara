from fastapi.responses import FileResponse
from fastapi import HTTPException
from pathlib import Path

class FileService:
    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir.resolve()

    def get_file_response(self, filename: str) -> FileResponse:
        file_path = (self.upload_dir / filename).resolve()
        if not str(file_path).startswith(str(self.upload_dir)):
            raise HTTPException(status_code=403, detail="Access denied")

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path)
