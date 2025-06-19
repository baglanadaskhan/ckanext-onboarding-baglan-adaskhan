ckan.module('pending-review-confirm', function($) {
  return {
    initialize: function() {
      var checkbox = $('#field-private');

      checkbox.change(function() {
        if (!this.checked) {
          const confirmed = confirm("Are you sure? The dataset will be sent for review.");
          if (!confirmed) {
            this.checked = true;
          }
        }
      });
    }
  };
});
