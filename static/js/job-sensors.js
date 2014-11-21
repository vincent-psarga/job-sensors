(function ($) {
  function get_job_container(job) {
    if ($('#job-' + job.id).length == 0) {
      $('#jobs').append('<div class="job" id="job-' + job.id + '"><h1></h1><span class="status"></span><span class="author"></span><div class="statusColor"></div></div>')
    }

    return $('#job-' + job.id);
  }

  function update_job_display(job) {
    var container = get_job_container(job),
      color = tinycolor('#' + job.status.color.color);

    container.find('h1').html(job.name);
    container.find('.status').html(job.status.value);
    container.find('.author').html(job.status.author);
    container.find('.statusColor').css({'background-color': color.toRgbString()});

    color.setAlpha(0.1);
    container.css({'background-color': color.toRgbString()});
  }

  function get_jobs_status() {
    $.ajax('/api', {
      error: function () {

      },

      success: function (data) {
        var jobs = data.jobs;

        jobs.forEach(function (job) {
          update_job_display(job);

        });
      }
    })
  }

  get_jobs_status();
  setInterval(get_jobs_status, 15000);
})(jQuery)