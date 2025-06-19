from logger import logger

def feedback(user_id: str, rating: int, comment: str):
    logger.info(f'Feedback from {user_id}: {rating} - {comment}')
