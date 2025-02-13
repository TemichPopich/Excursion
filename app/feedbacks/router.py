from fastapi import APIRouter, Depends, HTTPException, status

from app.database import Role
from app.feedbacks.dao import FeedbackDAO
from app.feedbacks.models import Feedback, PatchFeedback
from app.users.models import UserSchema
from app.auth.dependencies import get_current_auth_user, validate_rights


router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])


@router.patch("/update/{excursion_id}")
async def update_excursion(
    excursion_id: int,
    feedback: PatchFeedback,
    user: UserSchema = Depends(get_current_auth_user),
) -> Feedback:
    validate_rights(user=user, role=[Role.client])
    check = await FeedbackDAO.update(
        {"client_id": user.id, "exc_id": excursion_id},
        **feedback.model_dump(exclude_none=True),
    )

    if check:
        result = await FeedbackDAO.find_feedback(
            {"client_id": user.id, "exc_id": excursion_id}
        )
        await FeedbackDAO.change_excursion_score(result)
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Excursion {excursion_id} not found!",
    )
