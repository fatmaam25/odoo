# -*- coding: utf-8 -*-
# Part of Banastech. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def prepare_result(self, question, current_filters=None):
        current_filters = current_filters if current_filters else []
        result_summary = {}
        input_lines = question.user_input_line_ids.filtered(lambda line: not line.user_input_id.test_entry)

        # Calculate and return statistics for attachment
        if question.question_type == 'file':
            result_summary = []
            for input_line in input_lines:
                if not(current_filters) or input_line.user_input_id.id in current_filters:
                    result_summary.append(input_line)
            return result_summary
        else:
            return super(Survey, self).prepare_result(question, current_filters=current_filters)


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    # Answer
    question_type = fields.Selection(selection_add=[('file', 'Upload File')])
    max_file_size = fields.Integer("Maximum upload file size (MB)", default=5)
    allow_multi_file = fields.Boolean("Allow upload multiple file", default=True)

    def validate_file(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        answer = post[answer_tag].strip()
        # Empty answer to mandatory question
        if self.constr_mandatory and not answer:
            errors.update({answer_tag: self.constr_error_msg})
        return errors


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def save_lines(self, question, answer, comment=None):
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])
        if question.question_type == 'file':
            self.save_line_file(question, old_answers, answer)
        else:
            super(SurveyUserInput, self).save_lines(question, answer, comment=comment)

    @api.model
    def save_line_file(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer, question.question_type)
        attachment_ids = []
        if answer:
            attachment_ids = answer.split(',')
            attachment_ids = [(4, int(a)) for a in attachment_ids]
            vals.update({'attachment_ids': attachment_ids})
        if old_answers:
            old_answers.write(vals)
        else:
            old_answers.create(vals)
        return True


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    value_file = fields.Char("Value File")
    answer_type = fields.Selection(selection_add=[
        ('file', 'Upload file')])
    attachment_ids = fields.Many2many('ir.attachment', 'survey_attachment_user_input_line_rel',
                                      'input_id', 'attachment_id', 'Attachments')

    @api.depends('answer_type', 'attachment_ids')
    def _compute_display_name(self):
        super(SurveyUserInputLine, self)._compute_display_name()
        for line in self:
            if line.answer_type == 'file':
                if len(line.attachment_ids) == 1:
                    line.display_name = _("%s Attachment"%(len(line.attachment_ids)))
                elif len(line.attachment_ids) > 1:
                    line.display_name = _("%s Attachments"%(len(line.attachment_ids)))
                else:
                    line.display_name = _("No Attachment")