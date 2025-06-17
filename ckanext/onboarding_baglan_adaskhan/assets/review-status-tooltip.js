ckan.module("review-status-tooltip", function($, _) {
    "use strict";
    return {
        options: {
            review_status: "Unknown",
        },

        initialize: function() {
            const status = this.options.review_status;
            let message = "";

            if (status == "pending") {
                message = this._(
                    "This dataset has to be approved by reviewer",
                );
            } else if (status == "approved") {
                message = this._(
                    "This dataset has been approved by a reviewer",
                );
            } else if (status == "rejected") {
                message = this._(
                    "This dataset has been rejected by a reviewer",
                );
            }

            $(this.el).attr("title", message);
        },
    };
});