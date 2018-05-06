from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from ntds_webportal import db
from ntds_webportal.organizer import bp
from ntds_webportal.models import requires_access_level, Team, TeamFinances, Contestant, ContestantInfo, StatusInfo
import ntds_webportal.data as data
from raffle_system.functions import test_func


@bp.route('/registration_overview')
@login_required
@requires_access_level(data.ACCESS['organizer'])
def registration_overview():
    all_dancers = db.session.query(Contestant).join(ContestantInfo).join(StatusInfo)\
        .order_by(ContestantInfo.team_id, ContestantInfo.number).all()
    order = [data.CONFIRMED, data.SELECTED, data.REGISTERED, data.CANCELLED]
    all_dancers = sorted(all_dancers, key=lambda o: (o.contestant_info[0].team_id,
                                                     order.index(o.status_info[0].status)))
    dancers = [{'country': team['country'], 'name': team['name'], 'id': team['name'].replace(' ', '-').replace('`', ''),
               'dancers': [dancer for dancer in all_dancers if dancer.contestant_info[0].team.name == team['name']]}
               for team in data.TEAMS]
    dutch_dancers = [team for team in dancers if team['country'] == data.NETHERLANDS]
    german_dancers = [team for team in dancers if team['country'] == data.GERMANY]
    other_dancers = [team for team in dancers if team['country'] != data.NETHERLANDS and
                     team['country'] != data.GERMANY]
    return render_template('organizer/registration_overview.html', data=data, all_dancers=all_dancers,
                           dutch_dancers=dutch_dancers, german_dancers=german_dancers, other_dancers=other_dancers)


@bp.route('/finances_overview', methods=['GET', 'POST'])
@login_required
@requires_access_level([data.ACCESS['organizer']])
def finances_overview():
    all_dancers = db.session.query(Contestant).join(ContestantInfo).join(StatusInfo)\
        .filter(StatusInfo.payment_required.is_(True)).order_by(ContestantInfo.team_id, ContestantInfo.number).all()
    all_confirmed_dancers = [d for d in all_dancers if d.status_info[0].status == data.CONFIRMED]
    all_cancelled_dancers = [d for d in all_dancers if d.status_info[0].status == data.CANCELLED]
    all_teams = db.session.query(Team).join(TeamFinances).all()
    teams = [{'team': team, 'id': team.name.replace(' ', '-').replace('`', ''),
              'confirmed_dancers': [dancer for dancer in all_confirmed_dancers if
                                    dancer.contestant_info[0].team.name == team.name],
              'cancelled_dancers': [dancer for dancer in all_cancelled_dancers if
                                    dancer.contestant_info[0].team.name == team.name],
              'finances': data.finances_overview([dancer for dancer in all_dancers if
                                                  dancer.contestant_info[0].team.name == team.name])}
             for team in all_teams]
    teams = [team for team in teams if (len(team['confirmed_dancers'])+len(team['cancelled_dancers'])) > 0]
    dutch_teams = [team for team in teams if team['team'].country == data.NETHERLANDS]
    german_teams = [team for team in teams if team['team'].country == data.GERMANY]
    other_teams = [team for team in teams if
                   team['team'].country != data.NETHERLANDS and team['team'].country != data.GERMANY]
    if request.method == 'POST':
        changes = False
        for team in all_teams:
            amount_paid = request.form.get(str(team.team_id))
            if amount_paid != '' and amount_paid is not None:
                amount_paid = int(float(amount_paid)*100)
                if team.finances[0].paid != amount_paid:
                    team.finances[0].paid = amount_paid
                    changes = True
        if changes:
            db.session.commit()
            flash('Changes saved successfully.', 'alert-success')
        else:
            flash('No changes were made to submit.', 'alert-warning')
        return redirect(url_for('organizer.finances_overview'))
    return render_template('organizer/finances_overview.html', teams=teams, data=data,
                           dutch_teams=dutch_teams, german_teams=german_teams, other_teams=other_teams)


@bp.route('/raffle_system', methods=['GET', 'POST'])
@login_required
@requires_access_level([data.ACCESS['organizer']])
def raffle_system():
    if request.method == 'POST':
        test_func()
    return render_template('organizer/raffle_system.html')
