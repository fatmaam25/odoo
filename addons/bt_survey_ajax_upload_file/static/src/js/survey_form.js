odoo.define('banas_survey_upload_files.survey_form', function (require) {
'use strict';

var survey_form = require('survey.form');
var publicWidget = require('web.public.widget');


survey_form.include({

    start: function () {
        var self = this;
        this.fadeInOutDelay = 400;
        return this._super.apply(this, arguments).then(function () {
            $('div.survey-upload-files').each(function () {
                self._initFileWidget($(this));
            });
        });
    },
    _initFileWidget: function (ev) {
        var $result = this.$('.input-file');
        var readonly = this.$('fieldset[disabled="disabled"]').length !== 0;
        if (this.readonly)
            readonly = this.readonly
        if ($result.length) {
            this.surveyFileWidget = new publicWidget.registry.upload_file(ev, {'readonly': readonly});
            this.surveyFileWidget.attachTo(ev);
            $result.fadeIn(this.fadeInOutDelay);
        }
    },
    _onNextScreenDone: function (result, options) {
        var self = this;
        this._super.apply(this, arguments)
        if (result && !result.error) {
            $('div.survey-upload-files').each(function () {
                self._initFileWidget($(this));
            });
        }
    },
    _prepareSubmitValues: function (formData, params) {
        var self = this;
        this._super.apply(this, arguments)
        // Get all question answers by question type
        this.$('[data-question-type="file"]').each(function () {
            switch ($(this).data('questionType')) {
                case 'file':
                    params[this.name] = this.value;
                    break;
            }
        });
    },
})

});