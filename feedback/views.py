import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from .forms import FeedbackForm, SupportForm, ContactForm
from .models import Problem, Support
from .services import add_issue_support, check_empty_feedback

logger = logging.getLogger("django")


class FeedbackView(FormView):
    template_name = "feedback/feedback_form.html"
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback:form')

    def form_valid(self, form):
        res_help = form.cleaned_data.get("results_was_helpful")
        info_out = form.cleaned_data.get("information_outdated")
        info_missed = form.cleaned_data.get("information_is_missing")
        others = form.cleaned_data.get("other_field")
        if check_empty_feedback(res_help, info_out, info_missed, others) is True:
            messages.success(self.request, _('Feedback Sent Successfully!'))
            messages.success(self.request, _('Thank You! We use feedback like this to improve Raw Search.'))
            logger.info("Feedback, FeedbackView(FormView); got feedback and passed to services.check_empty_feedback for "
                    "adding to DB Feedback.Feedback")
        else:
            messages.error(self.request, _('Feedback Was Not Sent'), _("Please, Provide information"))

        return HttpResponseRedirect(self.get_success_url())


class SupportView(FormView):
    template_name = 'feedback/support_form.html'
    form_class = SupportForm
    success_url = reverse_lazy('feedback:support')

    def form_valid(self, form):
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        user = self.request.user
        add_issue_support(user, subject, message)
        messages.success(self.request, _('Thank You! We use feedback like this to improve Raw Search.'))
        logger.info("Feedback, SupportView(FormView); got from user: %s, subject: %s, message: %s | \n "
                    "Passed to services.add_issue_support for adding to DB Feedback.Support", user, subject, message)
        return HttpResponseRedirect(self.get_success_url())


class ContactView(FormView):
    template_name = 'feedback/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('feedback:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Thank You! We will contact you shortly.'))
        logger.info("Feedback, ContactView(FormView); received new contact form submission: %s \n ",
                    str(form.cleaned_data))
        return HttpResponseRedirect(self.get_success_url())


def mark_solved(request, pr_id: int):
    try:
        cp = Problem.objects.using('feedback_db').get(id=pr_id)
        cp.status = "solved"
        cp.save(using="feedback_db")
        messages.success(request, _("Solved"))
    except Exception as ex:
        logger.exception("Error deleting from queue, %s", str(ex))
        messages.error(request, _("Error: ") + str(ex))
    return redirect(request.META['HTTP_REFERER'])


def mark_solved_sup(request, pr_id: int):
    try:
        cp = Support.objects.using('feedback_db').get(id=pr_id)
        cp.status = "solved"
        cp.save(using="feedback_db")
        messages.success(request, _("Solved"))
    except Exception as ex:
        logger.exception("Error deleting from queue, %s", str(ex))
        messages.error(request, _("Error: ") + str(ex))
    return redirect(request.META['HTTP_REFERER'])
