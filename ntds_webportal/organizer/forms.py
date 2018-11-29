from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import Email
from ntds_webportal.validators import UniqueEmail


class NameChangeResponse(FlaskForm):
    remark = TextAreaField(label='Remarks for the teamcaptain (optional)',
                           render_kw={"style": "resize:none", "rows": "3", "maxlength": "512"})
    accept = SubmitField(label='Accept')
    reject = SubmitField(label='Reject')


class ChangeEmailForm(FlaskForm):
    email = StringField('E-mail', validators=[Email(), UniqueEmail()])


class FinalizeMerchandiseForm(FlaskForm):
    submit = SubmitField('Finalize orders')
