import jobs
import config
from utils.various import bound
from utils.colors import mix_colors
from notifiers import notifier
from db.models import StatusColor


class ColorNotifier(notifier.Notifier):
    def _check(self):
        current = self.job.status
        if current.error:
            self.set_color(config.ERROR_COLOR, blink=True)
            return

        self.assign_color(current)

    def assign_color(self, status):
        raise NotImplementedError()

    def set_color(self, color, blink=False, pulse=False):
        db_col = StatusColor.get_or_create(status=self.job.status)[0]
        db_col.color = color
        db_col.blink = blink
        db_col.pulse = pulse
        db_col.save()


class ResponseColorNotifier(ColorNotifier):
    def assign_color(self, status):
        bound_response = bound(
            float(status.value),
            self.job.min_time,
            self.job.max_time
        )

        self.set_color(mix_colors(
            config.RESPONSE_FAST_COLOR,
            config.RESPONSE_SLOW_COLOR,
            (bound_response - self.job.min_time) / self.job.max_time
        ))


class CIColorNotifier(ColorNotifier):
    def assign_color(self, status):
        mapping = {
            str(jobs.ci.STATUS_SUCCESS): config.CI_SUCCESS_COLOR,
            str(jobs.ci.STATUS_FAILURE): config.CI_FAILURE_COLOR,
            str(jobs.ci.STATUS_PENDING): config.CI_PENDING_COLOR
        }

        self.set_color(
            mapping.get(status.value, config.DEFAULT_COLOR),
            pulse=not status.stable
        )


COLOR_NOTIFIER_MAPPING = {
    jobs.response.Response: ResponseColorNotifier,
    jobs.ci.CI: CIColorNotifier
}


def get_notifiers(jobs):
    return notifier.get_notifiers(
        jobs,
        COLOR_NOTIFIER_MAPPING,
        config.CUSTOM_COLOR_NOTIFIERS
    )
