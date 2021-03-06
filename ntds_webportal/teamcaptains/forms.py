from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from ntds_webportal import db
from ntds_webportal.data import *
from ntds_webportal.validators import Level, Role, ChoiceMade, UniqueEmail, IsBoolean
from ntds_webportal.models import Contestant, ContestantInfo, StatusInfo, DancingInfo
from wtforms_sqlalchemy.fields import QuerySelectField
import wtforms_sqlalchemy.fields as f
from sqlalchemy import and_, or_
from ntds_webportal.helper_classes import ReactForm


def get_pk_from_identity(obj):
    cls, key = f.identity_key(instance=obj)[:2]
    return ':'.join(f.text_type(x) for x in key)


f.get_pk_from_identity = get_pk_from_identity

# Form text
PARTNER_TEXT = 'No partner / Partner has not signed up yet'
LEAD_TEXT = 'Pick a lead'
FOLLOW_TEXT = 'Pick a follow'
DANCER_TEXT = 'Pick a dancer'


def participating_levels_choices(base_choices=False):
    levels = g.sc.get_participating_levels()
    if base_choices:
        result = [(CHOOSE, 'What level are you dancing?')] + [(level, level) for level in levels] + \
                 [(NO, 'I\'m not dancing')]
    else:
        result = [(level, level) for level in levels]
    return result


def payment_categories_choices():
    if g.sc.phd_student_category:
        return [('', 'Are you a (PhD-)student?'), (STUDENT, "Yes, I am a student"),
                (PHD_STUDENT, "Yes, I am a PhD-student"), (NON_STUDENT, YMN[NO])]
    else:
        return [('', 'Are you a student?'), (STUDENT, YMN[YES]), (NON_STUDENT, YMN[NO])]


class BaseRegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()], render_kw={"placeholder": "First name..."})
    prefixes = StringField('prefix', description="de, van het, etc.")
    last_name = StringField('Last name', validators=[DataRequired()], render_kw={"placeholder": "Last name..."})
    email = StringField('Email', validators=[DataRequired(), Email(), UniqueEmail()],
                        render_kw={"placeholder": "Email address..."})
    sleeping_arrangements = SelectField('Sleeping spot', validators=[IsBoolean()],
                                        choices=[(k, v) for k, v in SLEEPING.items()])
    diet_allergies = StringField('Diet/Allergies', render_kw={"placeholder": "Special diets and/or allergies (if any), "
                                                                             "otherwise leave blank"})


class DancingInfoForm(FlaskForm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not g.sc.breitensport_obliged_blind_date:
            self.latin_blind_date.data = str(False)
            self.ballroom_blind_date.data = str(False)

    ballroom_level = SelectField('Level', validators=[Level()])
    ballroom_role = SelectField('Role', validators=[Role('ballroom_level')],
                                choices=[(k, v) for k, v in ROLES.items()])
    ballroom_blind_date = SelectField('Mandatory blind dating', validators=[Role('ballroom_level')],
                                      choices=[(k, v) for k, v in BLIND_DATE.items()])
    ballroom_partner = QuerySelectField(validators=[Role('ballroom_level'), Level()],
                                        allow_blank=True, blank_text=PARTNER_TEXT)

    latin_level = SelectField('Level', validators=[Level()])
    latin_role = SelectField('Role', validators=[Role('latin_level')], choices=[(k, v) for k, v in ROLES.items()])
    latin_blind_date = SelectField('Mandatory blind dating', validators=[Role('latin_level')],
                                   choices=[(k, v) for k, v in BLIND_DATE.items()])
    latin_partner = QuerySelectField(validators=[Role('latin_level'), Level()],
                                     allow_blank=True, blank_text=PARTNER_TEXT)
    
    def custom_validate(self):
        if self.ballroom_level.data == BEGINNERS:
            self.ballroom_blind_date.data = str(False)
        if self.ballroom_level.data == CLOSED or self.ballroom_level.data == OPEN_CLASS:
            self.ballroom_blind_date.data = str(True)
        if self.latin_level.data == BEGINNERS:
            self.latin_blind_date.data = str(False)
        if self.latin_level.data == CLOSED or self.latin_level.data == OPEN_CLASS:
            self.latin_blind_date.data = str(True)
        if self.ballroom_level.data == NO:
            self.ballroom_role.data = NO
            self.ballroom_blind_date.data = str(False)
            self.ballroom_partner.data = None
        if self.latin_level.data == NO:
            self.latin_role.data = NO
            self.latin_blind_date.data = str(False)
            self.latin_partner.data = None


class VolunteerForm(FlaskForm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not g.sc.ask_first_aid:
            self.first_aid.data = NO
        if not g.sc.ask_emergency_response_officer:
            self.emergency_response_officer.data = NO
        if not g.sc.ask_adjudicator_certification:
            self.license_jury_ballroom.data = NO
            self.license_jury_latin.data = NO
        if not g.sc.ask_adjudicator_highest_achieved_level:
            self.level_jury_ballroom.data = BELOW_D
            self.level_jury_latin.data = BELOW_D
        if not g.sc.salsa_competition:
            self.jury_salsa.data = NO
        if not g.sc.polka_competition:
            self.jury_polka.data = NO

    first_aid = SelectField('First Aid', validators=[ChoiceMade()],
                            choices=[(k, v) for k, v in FIRST_AID.items()])
    emergency_response_officer = SelectField('Emergency Response Officer', validators=[ChoiceMade()],
                                             choices=[(k, v) for k, v in EMERGENCY_RESPONSE_OFFICER.items()])
    jury_ballroom = SelectField('Adjudicator Ballroom', validators=[ChoiceMade()],
                                choices=[(k, v) for k, v in JURY_BALLROOM.items()])
    jury_latin = SelectField('Adjudicator Latin', validators=[ChoiceMade()],
                             choices=[(k, v) for k, v in JURY_LATIN.items()])
    license_jury_ballroom = SelectField('License Ballroom', validators=[ChoiceMade()],
                                        choices=[(k, v) for k, v in LICENSE_BALLROOM.items()])
    license_jury_latin = SelectField('License Latin', validators=[ChoiceMade()],
                                     choices=[(k, v) for k, v in LICENSE_LATIN.items()])
    level_jury_ballroom = SelectField('Level Ballroom', validators=[ChoiceMade()],
                                      choices=[(k, v) for k, v in LEVEL_JURY_BALLROOM.items()])
    level_jury_latin = SelectField('Level Latin', validators=[ChoiceMade()],
                                   choices=[(k, v) for k, v in LEVEL_JURY_LATIN.items()])
    jury_salsa = SelectField('Adjudicator Salsa', validators=[ChoiceMade()],
                             choices=[(k, v) for k, v in JURY_SALSA.items()])
    jury_polka = SelectField('Adjudicator Polka', validators=[ChoiceMade()],
                             choices=[(k, v) for k, v in JURY_POLKA.items()])

    def custom_validate(self):
        if self.jury_ballroom.data == NO:
            self.license_jury_ballroom.data = NO
            self.level_jury_ballroom.data = BELOW_D
        if self.jury_latin.data == NO:
            self.license_jury_latin.data = NO
            self.level_jury_latin.data = BELOW_D


class BaseContestantForm(ReactForm, BaseRegistrationForm, DancingInfoForm, VolunteerForm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        first_time = {'': f'Is this your first {g.sc.tournament}?'}
        first_time.update(YN)
        self.first_time.choices = [(k, v) for k, v in first_time.items()]
        adult = {'': f'Will you be 18 years or older at the time of the tournament?'}
        adult.update(YN)
        self.adult.choices = [(k, v) for k, v in adult.items()]
        self.ballroom_partner.label.text = f"Ballroom partner for {g.sc.tournament}"
        self.latin_partner.label.text = f"Latin partner for {g.sc.tournament}"
        self.ballroom_level.choices = participating_levels_choices(base_choices=True)
        self.latin_level.choices = participating_levels_choices(base_choices=True)
        self.student.choices = payment_categories_choices()
        new_id = db.session.query().with_entities(db.func.max(Contestant.contestant_id)).scalar()
        if new_id is None:
            new_id = 1
        else:
            new_id += 1
        self.number.data = new_id

        if not g.sc.ask_volunteer:
            self.volunteer.data = NO
        if not g.sc.first_time_ask:
            self.first_time.data = str(False)

    number = IntegerField('Number', validators=[DataRequired()], render_kw={'disabled': True})

    volunteer = SelectField('Volunteer', validators=[ChoiceMade()], choices=[(k, v) for k, v in VOLUNTEER_FORM.items()])
    student = SelectField('Student', validators=[DataRequired()], default='')
    first_time = SelectField('First time', validators=[IsBoolean()])
    adult = SelectField('Adult at time of tournament', validators=[IsBoolean()])

    def custom_validate(self):
        # noinspection PyCallByClass
        DancingInfoForm.custom_validate(self)
        # noinspection PyCallByClass
        VolunteerForm.custom_validate(self)

        if self.ballroom_level.data == BEGINNERS or self.latin_level.data == BEGINNERS:
            self.first_time.data = str(True)

        if g.sc.ask_volunteer and self.volunteer.data == NO:
            self.first_aid.data = NO
            self.emergency_response_officer.data = NO

        if not g.sc.ask_adult:
            self.adult.data = str(False)

        if self.ballroom_level.data == BEGINNERS or self.ballroom_level.data == BREITENSPORT:
            self.jury_ballroom.data = NO
            self.license_jury_ballroom.data = NO
            self.level_jury_ballroom.data = BELOW_D
        if self.latin_level.data == BEGINNERS or self.latin_level.data == BREITENSPORT:
            self.jury_latin.data = NO
            self.license_jury_latin.data = NO
            self.level_jury_latin.data = BELOW_D
        if self.ballroom_blind_date.data == str(True):
            self.ballroom_partner.data = None
        if self.latin_blind_date.data == str(True):
            self.latin_partner.data = None

        if self.ballroom_level.data == NO:
            self.ballroom_role.data = NO
            self.ballroom_blind_date.data = str(False)
            self.ballroom_partner.data = None
        if self.latin_level.data == NO:
            self.latin_role.data = NO
            self.latin_blind_date.data = str(False)
            self.latin_partner.data = None

    def populate(self, dancer):
        self.number.data = dancer.contestant_info.number

        self.volunteer.data = dancer.volunteer_info.volunteer
        self.student.data = dancer.contestant_info.student
        self.first_time.data = str(dancer.contestant_info.first_time)
        self.diet_allergies.data = dancer.contestant_info.diet_allergies
        self.sleeping_arrangements.data = str(dancer.additional_info.sleeping_arrangements)
        self.adult.data = str(dancer.contestant_info.adult)

        self.first_aid.data = dancer.volunteer_info.first_aid
        self.emergency_response_officer.data = dancer.volunteer_info.emergency_response_officer
        self.jury_ballroom.data = dancer.volunteer_info.jury_ballroom
        self.jury_latin.data = dancer.volunteer_info.jury_latin
        self.license_jury_ballroom.data = dancer.volunteer_info.license_jury_ballroom
        self.license_jury_latin.data = dancer.volunteer_info.license_jury_latin
        self.level_jury_ballroom.data = dancer.volunteer_info.level_ballroom
        self.level_jury_latin.data = dancer.volunteer_info.level_latin
        self.jury_salsa.data = dancer.volunteer_info.jury_salsa
        self.jury_polka.data = dancer.volunteer_info.jury_polka

        self.ballroom_level.data = dancer.competition(BALLROOM).level
        self.ballroom_role.data = dancer.competition(BALLROOM).role
        self.ballroom_blind_date.data = str(dancer.competition(BALLROOM).blind_date)
        self.ballroom_partner.data = Contestant.query.join(ContestantInfo)\
            .filter(Contestant.contestant_id == dancer.competition(BALLROOM).partner).first()

        self.latin_level.data = dancer.competition(LATIN).level
        self.latin_role.data = dancer.competition(LATIN).role
        self.latin_blind_date.data = str(dancer.competition(LATIN).blind_date)
        self.latin_partner.data = Contestant.query.join(ContestantInfo)\
            .filter(Contestant.contestant_id == dancer.competition(LATIN).partner).first()


class RegisterContestantForm(BaseContestantForm):
    submit = SubmitField('Register')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ballroom_partner.query = Contestant.query.join(ContestantInfo, DancingInfo, StatusInfo) \
            .filter(ContestantInfo.team == current_user.team,
                    or_(StatusInfo.status == REGISTERED, StatusInfo.status == NO_GDPR),
                    DancingInfo.partner.is_(None), DancingInfo.competition == BALLROOM,
                    or_(and_(DancingInfo.level == BREITENSPORT,
                             or_(DancingInfo.blind_date.is_(False),
                                 DancingInfo.blind_date.is_(not g.sc.breitensport_obliged_blind_date))),
                        DancingInfo.level == BEGINNERS)).order_by(Contestant.first_name)
        self.latin_partner.query = Contestant.query.join(ContestantInfo, DancingInfo, StatusInfo) \
            .filter(ContestantInfo.team == current_user.team,
                    or_(StatusInfo.status == REGISTERED, StatusInfo.status == NO_GDPR),
                    DancingInfo.partner.is_(None), DancingInfo.competition == LATIN,
                    or_(and_(DancingInfo.level == BREITENSPORT,
                             or_(DancingInfo.blind_date.is_(False),
                                 DancingInfo.blind_date.is_(not g.sc.breitensport_obliged_blind_date))),
                        DancingInfo.level == BEGINNERS)).order_by(Contestant.first_name)

    def custom_validate(self):
        super().custom_validate()

    def populate(self, dancer):
        super().populate(dancer)
        self.first_name.data = dancer.first_name
        self.prefixes.data = dancer.prefixes
        self.last_name.data = dancer.last_name
        self.email.data = dancer.email


class EditContestantForm(BaseContestantForm):
    full_name = StringField('Full name', validators=[DataRequired()], render_kw={'disabled': True})
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save changes')

    def __init__(self, dancer=None, **kwargs):
        super().__init__(**kwargs)
        if dancer is not None:
            ballroom_query = Contestant.query.join(ContestantInfo, DancingInfo, StatusInfo) \
                .filter(DancingInfo.competition == BALLROOM,
                        or_(and_(DancingInfo.level == BREITENSPORT,
                                 or_(DancingInfo.blind_date.is_(False),
                                     DancingInfo.blind_date.is_(not g.sc.breitensport_obliged_blind_date))),
                            DancingInfo.level == BEGINNERS))
            if dancer.competition(BALLROOM).partner is not None:
                ballroom_query.filter(or_(and_(ContestantInfo.team == current_user.team, DancingInfo.partner.is_(None)),
                                          DancingInfo.partner == dancer.contestant_id)).order_by(Contestant.first_name)
            else:
                ballroom_query.filter(ContestantInfo.team == current_user.team, DancingInfo.partner.is_(None))\
                    .order_by(Contestant.first_name)
            self.ballroom_partner.query = ballroom_query

            latin_query = Contestant.query.join(ContestantInfo, DancingInfo, StatusInfo) \
                .filter(DancingInfo.competition == LATIN,
                        or_(and_(DancingInfo.level == BREITENSPORT,
                                 or_(DancingInfo.blind_date.is_(False),
                                     DancingInfo.blind_date.is_(not g.sc.breitensport_obliged_blind_date))),
                            DancingInfo.level == BEGINNERS))
            if dancer.competition(LATIN).partner is not None:
                latin_query.filter(or_(and_(ContestantInfo.team == current_user.team, DancingInfo.partner.is_(None)),
                                       DancingInfo.partner == dancer.contestant_id)).order_by(Contestant.first_name)
            else:
                latin_query.filter(ContestantInfo.team == current_user.team, DancingInfo.partner.is_(None)) \
                    .order_by(Contestant.first_name)
            self.latin_partner.query = latin_query
            self.student.render_kw = {'disabled': dancer.payment_info.entry_paid}

    def custom_validate(self, dancer):
        if dancer.status_info.status == SELECTED or dancer.status_info.status == CONFIRMED:
            self.ballroom_level.data = dancer.competition(BALLROOM).level
            self.ballroom_role.data = dancer.competition(BALLROOM).role
            self.ballroom_blind_date.data = str(dancer.competition(BALLROOM).blind_date)
            self.ballroom_partner.data = db.session.query(Contestant).join(ContestantInfo) \
                .filter(Contestant.contestant_id == dancer.competition(BALLROOM).partner).first()
            self.latin_level.data = dancer.competition(LATIN).level
            self.latin_role.data = dancer.competition(LATIN).role
            self.latin_blind_date.data = str(dancer.competition(LATIN).blind_date)
            self.latin_partner.data = db.session.query(Contestant).join(ContestantInfo) \
                .filter(Contestant.contestant_id == dancer.competition(LATIN).partner).first()
            self.student.data = dancer.contestant_info.student
        super().custom_validate()
        self.full_name.data = dancer.get_full_name()
        if dancer.payment_info.entry_paid:
            self.student.data = dancer.contestant_info.student
    
    def populate(self, dancer):
        super().populate(dancer)
        self.full_name.data = dancer.get_full_name()
        self.email.data = dancer.email

    def organizer_populate(self, dancer):
        self.ballroom_partner.query = Contestant.query
        self.latin_partner.query = Contestant.query
        self.populate(dancer)
        self.full_name.data = dancer.get_full_name()
        self.email.data = dancer.email


class TeamCaptainForm(FlaskForm):
    team_captain_one = QuerySelectField('Teamcaptain', allow_blank=True, blank_text='No teamcaptain')
    team_captain_two = QuerySelectField('Teamcaptain', allow_blank=True, blank_text='No teamcaptain')
    submit = SubmitField('Set teamcaptain')


class CreateCoupleForm(FlaskForm):

    def __init__(self, sc, **kwargs):
        super(CreateCoupleForm, self).__init__(**kwargs)
        choices = [("", "Choose a level")]
        if sc.beginners_level:
            choices += [(BEGINNERS, BEGINNERS)]
        choices += [(BREITENSPORT, BREITENSPORT)]
        self.level.choices = choices

    lead = QuerySelectField('Lead', validators=[DataRequired()], allow_blank=True, blank_text=LEAD_TEXT)
    follow = QuerySelectField('Follow', validators=[DataRequired()], allow_blank=True, blank_text=FOLLOW_TEXT)
    competition = SelectField('Competition', validators=[DataRequired()],
                              choices=[(k, v) for k, v in COMPETITION_CHOICE.items()])
    level = SelectField('Level', validators=[DataRequired()])
    submit = SubmitField('Create couple')


class PartnerRequestForm(FlaskForm):

    def __init__(self, sc, other_choices, **kwargs):
        super(PartnerRequestForm, self).__init__(**kwargs)
        choices = [("", "Choose a level")]
        if sc.beginners_level:
            choices += [(BEGINNERS, BEGINNERS)]
        choices += [(BREITENSPORT, BREITENSPORT)]
        self.level.choices = choices
        self.other.choices = [("", DANCER_TEXT)] + [(str(dancer.contestant_id), dancer.get_full_name() + " - " +
                                                     dancer.contestant_info.team.name) for dancer in other_choices]

    dancer = QuerySelectField('Dancer from my team', validators=[DataRequired()],
                              allow_blank=True, blank_text=DANCER_TEXT, render_kw={'data-role': 'select2'})
    other = SelectField('Dancer from other team', validators=[DataRequired()], render_kw={'data-role': 'select2'})
    competition = SelectField('Competition', validators=[DataRequired()],
                              choices=[(k, v) for k, v in COMPETITION_CHOICE.items()])
    level = SelectField('Level', validators=[DataRequired()])
    remark = TextAreaField('Remarks', render_kw={"style": "resize:none", "rows": "4", "maxlength": "512"})
    submit = SubmitField('Send partner request')


class PartnerRespondForm(FlaskForm):
    remark = TextAreaField(label='Remarks for the other teamcaptain (optional)',
                           render_kw={"style": "resize:none", "rows": "3", "maxlength": "512"})
    accept = SubmitField(label='Accept')
    reject = SubmitField(label='Reject')


class NameChangeRequestForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    prefixes = StringField('Prefixes')
    last_name = StringField('Last name', validators=[DataRequired()])
    submit = SubmitField('Send name change request')


class EditDancingInfoForm(DancingInfoForm):

    def __init__(self, dancer, **kwargs):
        super().__init__(**kwargs)
        self.full_name.data = dancer.get_full_name()
        self.email.data = dancer.email
        self.team.data = dancer.contestant_info.team
        self.ballroom_level.choices = participating_levels_choices(base_choices=True)
        self.latin_level.choices = participating_levels_choices(base_choices=True)
        if not g.sc.breitensport_obliged_blind_date:
            self.latin_blind_date.data = str(False)
            self.ballroom_blind_date.data = str(False)
        self.ballroom_partner.query = Contestant.query.join(ContestantInfo)\
            .filter(Contestant.contestant_id == dancer.competition(BALLROOM).partner)
        self.ballroom_partner.data = self.ballroom_partner.query.first()
        self.latin_partner.query = Contestant.query.join(ContestantInfo) \
            .filter(Contestant.contestant_id == dancer.competition(LATIN).partner)
        self.latin_partner.data = self.latin_partner.query.first()

    full_name = StringField('Full name', validators=[DataRequired()], render_kw={'disabled': True})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'disabled': True})
    team = StringField('Team', validators=[DataRequired()], render_kw={'disabled': True})

    submit = SubmitField('Save changes')

    def populate(self, dancer):
        self.ballroom_level.data = dancer.competition(BALLROOM).level
        self.ballroom_role.data = dancer.competition(BALLROOM).role
        self.ballroom_blind_date.data = str(dancer.competition(BALLROOM).blind_date)

        self.latin_level.data = dancer.competition(LATIN).level
        self.latin_role.data = dancer.competition(LATIN).role
        self.latin_blind_date.data = str(dancer.competition(LATIN).blind_date)

    def custom_validate(self):
        if self.ballroom_level.data == BEGINNERS:
            self.ballroom_blind_date.data = str(False)
        if self.ballroom_level.data == CLOSED or self.ballroom_level.data == OPEN_CLASS:
            self.ballroom_blind_date.data = str(True)
        if self.latin_level.data == BEGINNERS:
            self.latin_blind_date.data = str(False)
        if self.latin_level.data == CLOSED or self.latin_level.data == OPEN_CLASS:
            self.latin_blind_date.data = str(True)
        if self.ballroom_level.data == NO:
            self.ballroom_role.data = NO
            self.ballroom_blind_date.data = str(False)
            self.ballroom_partner.data = None
        if self.latin_level.data == NO:
            self.latin_role.data = NO
            self.latin_blind_date.data = str(False)
            self.latin_partner.data = None

        if self.ballroom_blind_date.data == str(True):
            self.ballroom_partner.data = None
        if self.latin_blind_date.data == str(True):
            self.latin_partner.data = None


class ResendCredentialsForm(FlaskForm):
    email = StringField('E-mail', validators=[Email()])

    def populate(self, dancer):
        self.email.data = dancer.email


class CheckEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), UniqueEmail()])
