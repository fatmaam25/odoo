odoo.define('banas_survey_upload_files.survey_print', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
var SurveyPrint = require('survey.print');


SurveyPrint.include({
    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            $('div.survey-upload-files').each(function () {
                self._initFileWidget($(this));
            });
        });
    },
    _initFileWidget: function (ev) {
        var $result = this.$('.input-file');
        if ($result.length) {
            this.surveyFileWidget = new publicWidget.registry.upload_file(ev, {'readonly': true});
            this.surveyFileWidget.attachTo(ev);
            $result.fadeIn(this.fadeInOutDelay);
        }
    },
})
})