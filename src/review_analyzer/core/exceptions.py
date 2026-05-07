class ReviewAnalyzerError(Exception):
    """Base exception for domain-level analyzer failures."""


class EmptyReviewError(ReviewAnalyzerError):
    """Raised when a review has no usable text."""
