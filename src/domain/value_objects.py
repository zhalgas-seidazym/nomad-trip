from src.domain.enums import Status

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]

ALLOWED_STATUS_TRANSITIONS = {
    Status.WAITING: {Status.APPROVED, Status.REJECTED},
    Status.APPROVED: {Status.REJECTED},
    Status.REJECTED: {Status.APPROVED},
}