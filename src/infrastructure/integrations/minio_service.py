from typing import List, Optional
from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
from io import BytesIO


class MinioService:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False  # True if https
        )
        self.bucket = bucket

        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    async def upload_file(self, file: UploadFile, folder: Optional[str] = None) -> str:
        file_path = file.filename
        if folder:
            file_path = f"{folder}/{file.filename}"

        content = await file.read()
        file_bytes = BytesIO(content)

        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=file_path,
                data=file_bytes,
                length=len(content),
                content_type=file.content_type
            )
        except S3Error as e:
            raise Exception(f"MinIO upload failed: {e}")

        return f"/{self.bucket}/{file_path}"

    async def upload_files(self, files: List[UploadFile], folder: Optional[str] = None) -> List[str]:
        urls = []
        for file in files:
            url = await self.upload_file(file, folder)
            urls.append(url)
        return urls

    async def delete_file(self, file_path: str) -> None:
        """
        Deletes a file from the bucket.
        `file_path` should include the folder if used, e.g., "avatars/user1.png".
        """
        try:
            self.client.remove_object(self.bucket, file_path)
        except S3Error as e:
            raise Exception(f"Failed to delete file from MinIO: {e}")

    async def delete_files(self, file_paths: List[str]) -> None:
        """
        Deletes multiple files at once.
        """
        errors = []
        for path in file_paths:
            try:
                await self.delete_file(path)
            except Exception as e:
                errors.append(str(e))
        if errors:
            raise Exception(f"Some files could not be deleted: {errors}")
