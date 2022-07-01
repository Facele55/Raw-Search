import logging

from feedback.models import Feedback, Support


logger = logging.getLogger("django")


def check_empty_feedback(res_help, info_out, info_missed, others) -> bool:
    helps = len(res_help)
    out = len(info_out)
    miss = len(info_missed)
    ot = len(others)
    options = [helps, out, miss, ot]
    if sum(options) != 0:
        add_issue_feedback(res_help, info_out, info_missed, others)
        logger.info("Feedback, services.check_empty_feedback; got values from FeedbackView:"
                    "res_help %s, info_out %s, info_missed %s, others %s",
                    res_help, info_out, info_missed, others)
        return True
    else:
        logger.debug("Feedback, services.check_empty_feedback; got empty feedback")
        return False


def add_issue_feedback(res_help,  info_out, info_missed, others):
    try:
        f = Feedback.objects.using('feedback_db').create(results_was_helpful=res_help,
                                                         information_outdated=info_out,
                                                         information_is_missing=info_missed, other_field=others)
        f.save(using='feedback_db')
    except Exception as e:
        logger.error("Feedback, add_issue_feedback; Exception found: %s", str(e))


def add_issue_support(user, subject, message):
    try:
        f = Support.objects.using('feedback_db').create(user=str(user), subject=subject, message=message)
        f.save(using='feedback_db')
    except Exception as e:
        logger.error("Feedback, add_issue_support; Exception found: %s", str(e))
