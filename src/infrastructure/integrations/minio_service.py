import os
import uuid
import asyncio
from typing import List, Optional
from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error


class MinioService:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        self.bucket = bucket

        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    async def upload_file(self, file: UploadFile, folder: Optional[str] = None) -> str:
        _, ext = os.path.splitext(file.filename)
        unique_name = f"{uuid.uuid4().hex}{ext}"

        file_path = f"{folder}/{unique_name}" if folder else unique_name

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        try:
            await asyncio.to_thread(
                self.client.put_object,
                self.bucket,
                file_path,
                file.file,
                file_size,
                file.content_type
            )
        except S3Error as e:
            raise Exception(f"MinIO upload failed: {e}")

        return f"/{self.bucket}/{file_path}"

    async def upload_files(self, files: List[UploadFile], folder: Optional[str] = None) -> List[str]:
        return [await self.upload_file(file, folder) for file in files]

    async def delete_file(self, file_path: str) -> None:
        key = file_path
        if file_path.startswith(f"/{self.bucket}/"):
            key = file_path[len(self.bucket) + 2:]

        try:
            await asyncio.to_thread(self.client.remove_object, self.bucket, key)
        except S3Error as e:
            raise Exception(f"Failed to delete file from MinIO: {e}")

    async def delete_files(self, file_paths: List[str]) -> None:
        errors = []

        for path in file_paths:
            try:
                await self.delete_file(path)
            except Exception as e:
                errors.append(str(e))

        if errors:
            raise Exception(f"Some files could not be deleted: {errors}")
